"""
GitHub repository fetcher with intelligent file selection.
Fetches repository context including metadata, file tree, and important file contents.
"""

import os
import re
from typing import Optional, Tuple, List, Dict
from github import Github, GithubException


# Priority files that should always be included if present
PRIORITY_FILES = {
    "README.md", "readme.md", "README.rst", "readme.rst",
    "package.json", "pyproject.toml", "setup.py", "setup.cfg",
    "Cargo.toml", "go.mod", "go.sum", "pom.xml", "build.gradle",
    "Makefile", "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    "CONTRIBUTING.md", "ARCHITECTURE.md", "DESIGN.md", "CHANGELOG.md",
    ".env.example", "requirements.txt",
}

# Directories to skip during traversal
SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".next", "out", "target", "vendor", ".cache",
    ".idea", ".vscode", "coverage", ".nyc_output", "eggs", ".eggs",
}

# File extensions to skip
SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z",
    ".lock",  # package-lock.json, yarn.lock, Cargo.lock
    ".min.js", ".min.css", ".map",
    ".pyc", ".pyo", ".class", ".o", ".so", ".dll", ".exe",
}

MAX_FILE_CHARS = 1500   # per file
MAX_FILES = 12          # max files to include in context
MAX_TREE_LINES = 60     # max lines in file tree


def parse_github_url(url: str) -> Tuple[str, str]:
    """
    Parse a GitHub URL and extract owner and repository name.
    
    Args:
        url: GitHub repository URL
        
    Returns:
        Tuple of (owner, repo_name)
        
    Raises:
        ValueError: If URL is not a valid GitHub repository URL
    """
    pattern = r"https?://github\.com/([^/]+)/([^/\s]+?)(?:\.git)?/?$"
    match = re.match(pattern, url.strip())
    
    if not match:
        raise ValueError(
            "Invalid GitHub URL. Expected format: https://github.com/owner/repo"
        )
    
    owner, repo = match.groups()
    return owner, repo


def is_text_file(path: str) -> bool:
    """
    Determine if a file is likely a text file based on its extension.
    
    Args:
        path: File path
        
    Returns:
        True if file should be treated as text, False otherwise
    """
    ext = os.path.splitext(path)[1].lower()
    return ext not in SKIP_EXTENSIONS


def score_file(path: str, name: str) -> int:
    """
    Score a file based on its importance for understanding the codebase.
    Higher scores indicate more important files.
    
    Args:
        path: Full file path
        name: File name
        
    Returns:
        Integer score
    """
    score = 0
    path_lower = path.lower()
    name_lower = name.lower()
    
    # Priority files get highest score
    if name in PRIORITY_FILES:
        score += 100
    
    # Main entry point files
    if re.match(r"^(main|index|app|server|api)\.", name_lower):
        score += 30
    
    # Source code files by extension
    ext = os.path.splitext(path)[1].lower()
    if ext in {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".rs", ".rb", ".swift", ".kt"}:
        score += 20
    elif ext in {".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg"}:
        score += 10
    
    # Penalize by depth (number of slashes in path)
    depth = path.count("/")
    score -= 5 * depth
    
    # Penalize test files
    if "test" in path_lower or "spec" in path_lower or "__tests__" in path_lower:
        score -= 20
    
    # Penalize example/sample files
    if "example" in path_lower or "sample" in path_lower or "fixture" in path_lower:
        score -= 10
    
    return score


def fetch_repo_context(repo_url: str, github_token: Optional[str] = None) -> Dict:
    """
    Fetch repository context including metadata, file tree, and important file contents.
    
    Args:
        repo_url: GitHub repository URL
        github_token: Optional GitHub personal access token
        
    Returns:
        Dictionary containing repository context
        
    Raises:
        ValueError: If repository cannot be accessed or URL is invalid
    """
    # Parse URL
    owner, repo_name = parse_github_url(repo_url)
    
    # Initialize GitHub client
    token = github_token or os.getenv("GITHUB_TOKEN")
    g = Github(token) if token else Github()
    
    # Get repository
    try:
        repo = g.get_repo(f"{owner}/{repo_name}")
    except GithubException as e:
        raise ValueError(f"GitHub API error: {e.data.get('message', str(e))}")
    
    # Collect files with scores — single recursive API call
    file_candidates: List[Tuple[int, str]] = []

    try:
        default_branch = repo.default_branch
        full_tree = repo.get_git_tree(default_branch, recursive=True)
    except Exception as e:
        raise ValueError(f"Failed to fetch repository tree: {str(e)}")

    for item in full_tree.tree:
        if item.type != "blob":
            continue
        path = item.path
        # Skip any path that contains a skipped directory segment
        parts = path.split("/")
        if any(p in SKIP_DIRS for p in parts[:-1]):
            continue
        if is_text_file(path):
            file_candidates.append((score_file(path, parts[-1]), path))
    
    # Sort by score and take top files
    file_candidates.sort(reverse=True, key=lambda x: x[0])
    selected_files = [path for _, path in file_candidates[:MAX_FILES]]
    
    # Fetch content for selected files
    files_content = []
    for file_path in selected_files:
        try:
            file_content = repo.get_contents(file_path)
            if hasattr(file_content, 'decoded_content'):
                content = file_content.decoded_content.decode('utf-8', errors='replace')
                
                # Truncate if too long
                if len(content) > MAX_FILE_CHARS:
                    content = content[:MAX_FILE_CHARS]
                    content += f"\n\n... [Content truncated at {MAX_FILE_CHARS} characters]"
                
                files_content.append({
                    "path": file_path,
                    "content": content
                })
        except Exception:
            # Skip files that can't be read
            continue
    
    # Build file tree from already-fetched full_tree (no extra API calls)
    file_tree_lines = []
    seen_dirs: set = set()

    all_paths = sorted(
        [item.path for item in full_tree.tree],
        key=lambda p: (p.count("/"), p)
    )

    for path in all_paths:
        if len(file_tree_lines) >= MAX_TREE_LINES:
            break
        parts = path.split("/")
        depth = len(parts) - 1
        if depth > 2:
            continue
        # Skip paths inside skipped dirs
        if any(p in SKIP_DIRS for p in parts[:-1]):
            continue
        # Add parent dir lines if not already added
        for d in range(depth):
            dir_path = "/".join(parts[:d+1])
            if dir_path not in seen_dirs and parts[d] not in SKIP_DIRS:
                indent = "  " * d
                file_tree_lines.append(f"{indent}{parts[d]}/")
                seen_dirs.add(dir_path)
        indent = "  " * depth
        file_tree_lines.append(f"{indent}{parts[-1]}")

    file_tree = "\n".join(file_tree_lines[:MAX_TREE_LINES])
    
    # Return structured context
    return {
        "owner": owner,
        "repo": repo_name,
        "description": repo.description or "",
        "language": repo.language or "Unknown",
        "stars": repo.stargazers_count,
        "forks": repo.forks_count,
        "topics": repo.get_topics(),
        "file_tree": file_tree,
        "files": files_content,
    }

def calculate_readiness_score(repo_context: dict, kit: dict) -> dict:
    """
    Calculate a Contribution Readiness Score (0-100) for a repository.
    Based on documentation, test coverage signals, CI presence,
    complexity, and community health.
    """
    score = 0
    breakdown = []
    file_paths = [f["path"].lower() for f in repo_context["files"]]
    tree = repo_context["file_tree"].lower()

    # 1. Documentation (25 points)
    doc_score = 0
    if any("readme" in p for p in file_paths):
        doc_score += 12
    if any("contributing" in p for p in file_paths):
        doc_score += 8
    if any("license" in p or "licence" in p for p in file_paths):
        doc_score += 3
    if any("changelog" in p for p in file_paths):
        doc_score += 2
    score += doc_score
    breakdown.append({
        "label": "Documentation",
        "score": doc_score,
        "max": 25,
        "note": "README, CONTRIBUTING, LICENSE, CHANGELOG"
    })

    # 2. Test Coverage Signals (25 points)
    test_score = 0
    has_tests = any("test" in p or "spec" in p for p in file_paths)
    has_test_dir = "test" in tree or "spec" in tree or "__tests__" in tree
    if has_tests or has_test_dir:
        test_score += 15
    if any(p in file_paths for p in ["pytest.ini", "jest.config.js",
       "jest.config.ts", ".mocharc.yml", "phpunit.xml"]):
        test_score += 10
    score += test_score
    breakdown.append({
        "label": "Test Coverage Signals",
        "score": test_score,
        "max": 25,
        "note": "Test files, test config files"
    })

    # 3. CI/CD & Automation (20 points)
    ci_score = 0
    if ".github/workflows" in tree or "github/workflows" in tree:
        ci_score += 15
    elif "makefile" in tree or "dockerfile" in tree:
        ci_score += 8
    if any(".env.example" in p or ".env.sample" in p for p in file_paths):
        ci_score += 5
    score += ci_score
    breakdown.append({
        "label": "CI/CD & Setup Automation",
        "score": ci_score,
        "max": 20,
        "note": "GitHub Actions, Makefile, .env.example"
    })

    # 4. Low Complexity (15 points)
    complexity_score = 0
    hotspots = len(kit.get("complexity_hotspots", []))
    if hotspots == 0:
        complexity_score = 15
    elif hotspots <= 2:
        complexity_score = 12
    elif hotspots <= 4:
        complexity_score = 7
    else:
        complexity_score = 3
    score += complexity_score
    breakdown.append({
        "label": "Codebase Complexity",
        "score": complexity_score,
        "max": 15,
        "note": f"{hotspots} complexity hotspot(s) identified"
    })

    # 5. Community Health (15 points)
    community_score = 0
    if repo_context["stars"] > 1000:
        community_score += 8
    elif repo_context["stars"] > 100:
        community_score += 5
    else:
        community_score += 2
    if repo_context["forks"] > 100:
        community_score += 4
    elif repo_context["forks"] > 10:
        community_score += 2
    if len(repo_context.get("topics", [])) > 0:
        community_score += 3
    score += community_score
    breakdown.append({
        "label": "Community Health",
        "score": community_score,
        "max": 15,
        "note": f"Stars: {repo_context['stars']:,}, Forks: {repo_context['forks']:,}"
    })

    # Determine grade
    if score >= 80:
        grade = "A"
        verdict = "Excellent for new contributors"
        color = "green"
    elif score >= 65:
        grade = "B"
        verdict = "Good starting point"
        color = "blue"
    elif score >= 50:
        grade = "C"
        verdict = "Moderate friction expected"
        color = "yellow"
    else:
        grade = "D"
        verdict = "High ramp-up effort required"
        color = "red"

    return {
        "score": score,
        "grade": grade,
        "verdict": verdict,
        "color": color,
        "breakdown": breakdown,
    }


# Made with Bob
