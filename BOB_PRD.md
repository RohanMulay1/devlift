# DevLift — Full PRD for IBM Bob

> Paste this entire document into IBM Bob as your first session. Bob will use it as the complete context for building the project. Reference specific sections as you work through each task.

---

## HACKATHON CONTEXT (Read This First)

**Event:** IBM Bob Hackathon — "Turn idea into impact faster"

**Challenge Statement:**
> Got an idea for how to work smarter and faster? Create a solution that speeds the way you work every day. Maybe you need to: get up to speed on existing code quickly, generate documentation and tests, or reduce effort spent on repetitive tasks that slow your team down. Use IBM Bob as your development partner to bring your idea to life. Bob understands intent, reads complete repository context, explains logic with clarity, automates complex transformations, and streamlines multi-step work.

**Judging Criteria (in order of importance):**
1. **Application of Technology** — How complete and well thought-out the project is, with a clear application of IBM Bob
2. **Presentation** — Clarity and effectiveness of the project presentation
3. **Business Value** — Impact and practical value; how effectively the solution addresses a high priority issue
4. **Originality** — Uniqueness and creativity of the solution and approach

**Required Submission Materials:**
- Project Title, Short Description, Long Description
- Technology & Category Tags
- Cover Image + Video Presentation + Slide Presentation
- Public GitHub Repository including exported IBM Bob report
- Live Demo Application URL

**Critical Rule:** All submissions must clearly demonstrate how IBM Bob is used in the solution. Projects that do not show meaningful use of Bob may be disqualified.

---

## THE PROBLEM BEING SOLVED

Every software team faces the same invisible tax: onboarding a developer to an unfamiliar codebase takes **1–3 weeks**. During that time they're not shipping. They're reading, guessing, asking questions, and getting lost.

There is no tooling that gives you an instant, structured, intelligent orientation to a new codebase. README files are incomplete. Wiki pages are stale. Asking teammates wastes senior engineer time.

**This is expensive.** Industry estimates put onboarding cost at $15,000–$30,000 per engineer per new project. For enterprises with large codebases and high turnover, this is a multi-million dollar problem per year.

---

## THE SOLUTION: DevLift

**DevLift** is a web application where you paste any public GitHub repository URL and get back a structured **Onboarding Kit** in under 60 seconds — powered by IBM watsonx.ai.

The kit gives developers exactly what they need to become productive fast:

| Kit Section | What it gives you |
|---|---|
| Architecture Overview | What the project does, how it's structured, which layers exist |
| Key Components Map | The 6–8 most important files to understand first, with explanations |
| Complexity Hotspots | Where the hard/tricky code lives, and tips for navigating it |
| Suggested First Tasks | Concrete starting points for a new contributor, with difficulty ratings |
| Common Patterns | Conventions and idioms used throughout — the unwritten rules |
| Setup & Run Guide | Extracted and cleaned up from config files + README |

**Result:** A new developer goes from zero context to informed contributor in minutes, not days.

---

## IBM BOB'S ROLE IN THIS PROJECT

IBM Bob is used in two distinct, demonstrable ways — which directly satisfies the "meaningful use of Bob" judging requirement:

**1. Bob as the development partner (builds this app)**
All code is written using Bob. Every file, every function, every test. The exported Bob report will show 8+ sessions covering: scaffolding, frontend, testing, documentation, debugging, and explanation tasks.

**2. Bob's capabilities are what the app demonstrates**
DevLift shows exactly what Bob does best — read a complete repository context, understand intent, and explain logic with clarity — but makes it available to anyone via a web interface, without needing the Bob IDE.

This dual use is the strongest possible answer to "Application of Technology."

---

## TECH STACK

| Layer | Technology | Why |
|---|---|---|
| Backend | Python 3.11 + FastAPI | Fast to build, production-grade async API |
| AI Engine | IBM watsonx.ai — `ibm/granite-34b-code-instruct` | IBM's code model, appropriate for hackathon |
| Repo Fetching | GitHub REST API via `PyGithub` | No cloning needed, handles auth and pagination |
| Frontend | Next.js 14 (App Router) + TypeScript + Tailwind CSS | Rapid UI development, Vercel deploy |
| Hosting | Vercel (frontend) + Railway (backend) | Both have free tiers, deploy in minutes |

---

## PROJECT STRUCTURE

```
devlift/
├── backend/
│   ├── main.py                    # FastAPI app — /analyze and /health endpoints
│   ├── github_fetcher.py          # GitHub API: smart file selection + content fetching
│   ├── prompt_builder.py          # Constructs the watsonx prompt from repo context
│   ├── bob_client.py              # watsonx.ai wrapper — calls Granite, parses JSON
│   ├── requirements.txt
│   ├── .env.example
│   └── tests/
│       ├── test_github_fetcher.py
│       └── test_prompt_builder.py
├── frontend/
│   ├── app/
│   │   ├── page.tsx               # Main page with all states
│   │   ├── layout.tsx             # Root layout + metadata
│   │   └── globals.css
│   ├── components/
│   │   ├── HeroInput.tsx          # Landing URL input + CTA
│   │   ├── LoadingState.tsx       # Animated progress with step labels
│   │   ├── RepoHeader.tsx         # Repo name, description, stats bar
│   │   ├── KitTabs.tsx            # Tab navigation between kit sections
│   │   ├── sections/
│   │   │   ├── ArchitectureSection.tsx
│   │   │   ├── ComponentsSection.tsx
│   │   │   ├── HotspotsSection.tsx
│   │   │   ├── TasksSection.tsx
│   │   │   ├── PatternsSection.tsx
│   │   │   └── SetupSection.tsx
│   │   └── DownloadButton.tsx     # Export kit as Markdown file
│   ├── lib/
│   │   └── api.ts                 # Backend fetch wrapper
│   ├── types/
│   │   └── kit.ts                 # All TypeScript interfaces
│   └── package.json
├── bob-report/                    # Exported IBM Bob session files go here
└── README.md
```

---

## BACKEND — DETAILED SPECIFICATION

### `requirements.txt`
```
fastapi==0.115.5
uvicorn[standard]==0.32.1
python-dotenv==1.0.1
ibm-watsonx-ai==1.1.7
PyGithub==2.5.0
pydantic==2.9.2
```

### `.env.example`
```bash
# GitHub personal access token — raises API rate limit from 60 to 5,000 req/hr
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# IBM Cloud API key with watsonx.ai service access
WATSONX_API_KEY=xxxxxxxxxxxxxxxxxxxx

# watsonx.ai Project ID (from IBM Cloud > watsonx > Projects)
WATSONX_PROJECT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

# watsonx.ai region endpoint
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

---

### `github_fetcher.py` — Full Specification

**Purpose:** Accept a GitHub URL, intelligently select the most important files, and return repo context as a structured dict.

**Constants to define:**
```python
PRIORITY_FILES = {
    "README.md", "readme.md", "README.rst", "readme.rst",
    "package.json", "pyproject.toml", "setup.py", "setup.cfg",
    "Cargo.toml", "go.mod", "go.sum", "pom.xml", "build.gradle",
    "Makefile", "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    "CONTRIBUTING.md", "ARCHITECTURE.md", "DESIGN.md", "CHANGELOG.md",
    ".env.example", "requirements.txt",
}

SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".next", "out", "target", "vendor", ".cache",
    ".idea", ".vscode", "coverage", ".nyc_output", "eggs", ".eggs",
}

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".webp",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".pdf", ".zip", ".tar", ".gz", ".rar", ".7z",
    ".lock",  # package-lock.json, yarn.lock, Cargo.lock
    ".min.js", ".min.css", ".map",
    ".pyc", ".pyo", ".class", ".o", ".so", ".dll", ".exe",
}

MAX_FILE_CHARS = 4000   # per file
MAX_FILES = 22          # max files to include in context
MAX_TREE_LINES = 100    # max lines in file tree
```

**`parse_github_url(url: str) -> tuple[str, str]`**
- Use regex: `r"https?://github\.com/([^/]+)/([^/\s]+?)(?:\.git)?/?$"`
- Return `(owner, repo_name)`
- Raise `ValueError` with a helpful message if URL doesn't match

**`is_text_file(path: str) -> bool`**
- Return False if `os.path.splitext(path)[1].lower()` is in `SKIP_EXTENSIONS`
- Return True otherwise

**`score_file(path: str, name: str) -> int`**
```
Base score: 0
+ 100 if name in PRIORITY_FILES
+ 30 if name matches: "main.*", "index.*", "app.*", "server.*", "api.*" (case-insensitive)
+ 20 if extension in {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".rs", ".rb", ".swift", ".kt"}
+ 10 if extension in {".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg"}
- 5 × depth (number of "/" in path)
- 20 if "test" in path.lower() or "spec" in path.lower() or "__tests__" in path
- 10 if "example" in path.lower() or "sample" in path.lower() or "fixture" in path.lower()
```

**`fetch_repo_context(repo_url: str, github_token: Optional[str] = None) -> dict`**

Steps:
1. Parse URL with `parse_github_url`
2. Initialize PyGithub with token from arg or `os.getenv("GITHUB_TOKEN")`
3. Get repo with `g.get_repo(f"{owner}/{repo_name}")` — catch `GithubException`, raise `ValueError` with the API message
4. Walk the repo tree recursively (max depth 4), skip `SKIP_DIRS`, collect `(score, path)` for text files
5. Sort by score descending, take top `MAX_FILES`
6. Fetch content for each selected file — decode as UTF-8 (`errors="replace"`), truncate to `MAX_FILE_CHARS`, append a truncation notice if truncated
7. Build file tree: walk top 2 levels only, sorted directories first, limit to `MAX_TREE_LINES` lines
8. Return:
```python
{
    "owner": str,
    "repo": str,
    "description": repo.description or "",
    "language": repo.language or "Unknown",
    "stars": repo.stargazers_count,
    "forks": repo.forks_count,
    "topics": repo.get_topics(),   # list of strings
    "file_tree": str,              # the formatted tree string
    "files": [{"path": str, "content": str}, ...],
}
```

---

### `prompt_builder.py` — Full Specification

**`build_onboarding_prompt(repo_context: dict) -> str`**

The prompt must be structured so the Granite model returns clean JSON. Use this exact structure:

```
You are an expert software architect. A new developer has just joined a team and needs to onboard to an unfamiliar codebase as quickly as possible. Your job is to analyze this repository and produce a structured onboarding kit.

You have access to the repository's file tree and the content of its most important files. Base your analysis strictly on what you can see — do not hallucinate file paths or invent functionality that isn't evidenced in the files.

=== REPOSITORY METADATA ===
Name: {owner}/{repo}
Description: {description}
Primary Language: {language}
Stars: {stars} | Forks: {forks}
Topics: {topics_joined_by_commas}

=== FILE TREE (top 2 levels) ===
{file_tree}

=== SELECTED FILE CONTENTS ===
{for each file: "--- {path} ---\n{content}\n"}

=== OUTPUT INSTRUCTIONS ===
Return a single valid JSON object with exactly these 6 keys. No markdown fences. No explanation before or after. Just the JSON.

{
  "architecture_overview": "Write 2-3 paragraphs explaining: (1) what this project does and who it's for, (2) its main architectural layers and how they interact, (3) the data/request flow from entry point to output. Reference actual file and directory names. Be specific — a vague answer is useless.",

  "key_components": [
    {
      "name": "Human-readable component name",
      "path": "exact/path/from/file/tree.ext",
      "description": "2-3 sentences: what this file/module does, why it matters, and what a new developer should understand about it before touching any code."
    }
  ],

  "complexity_hotspots": [
    {
      "name": "Short label for this area",
      "path": "exact/path/or/directory",
      "reason": "Why this code is complex, tricky, or risky to modify.",
      "tip": "Concrete advice for a developer approaching this area for the first time."
    }
  ],

  "suggested_first_tasks": [
    {
      "title": "Task title (action verb + specific outcome)",
      "description": "What to do, which files to look at, and what success looks like.",
      "difficulty": "easy | medium | hard"
    }
  ],

  "common_patterns": [
    {
      "pattern": "Pattern name (e.g. Repository Pattern, Middleware Chain, Event Sourcing)",
      "description": "How this pattern is specifically used in this codebase — not a generic definition.",
      "example": "File path or short code snippet that illustrates the pattern."
    }
  ],

  "setup_summary": {
    "prerequisites": ["Tool name and version, e.g. Node.js >= 18", "..."],
    "install_steps": ["Step 1 with exact command", "Step 2", "..."],
    "run_command": "The single command to start the application locally",
    "test_command": "The command to run the test suite",
    "notes": "Any important gotchas, environment setup requirements, or things that commonly go wrong during setup."
  }
}

Requirements:
- key_components: 6–8 items
- complexity_hotspots: 3–5 items
- suggested_first_tasks: 4–6 items (include at least 2 easy tasks for beginners)
- common_patterns: 3–5 items
- All file paths must exist in the file tree shown above
- Return ONLY the JSON object
```

---

### `bob_client.py` — Full Specification

**`_get_model() -> ModelInference`**
```python
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
    api_key=os.getenv("WATSONX_API_KEY"),
)
return ModelInference(
    model_id="ibm/granite-34b-code-instruct",
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    params={
        "max_new_tokens": 4096,
        "temperature": 0.1,    # Low temp for structured JSON output
        "top_p": 0.85,
        "repetition_penalty": 1.1,
    },
)
```

**`generate_onboarding_kit(prompt: str) -> dict`**
1. Call `model.generate_text(prompt=prompt)`
2. Strip leading/trailing whitespace
3. If response starts with ` ``` `: strip the fence block (handle `json` variant too)
4. Find the first `{` and last `}` — extract that substring to handle any preamble
5. Parse with `json.loads()`
6. Validate that all 6 required keys are present — raise `ValueError` listing missing keys if not
7. Return the dict

---

### `main.py` — Full Specification

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="DevLift API",
    description="Instant AI-powered onboarding kits for any GitHub repository",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

**`GET /health`**
Returns: `{"status": "ok", "model": "ibm/granite-34b-code-instruct"}`

**`POST /analyze`**

Request body:
```json
{ "repo_url": "https://github.com/owner/repo" }
```

Response (200):
```json
{
  "owner": "string",
  "repo": "string",
  "description": "string",
  "language": "string",
  "stars": 0,
  "forks": 0,
  "topics": ["string"],
  "files_analyzed": 0,
  "kit": { ...all 6 kit sections... }
}
```

Error responses:
- `400` — Invalid URL or GitHub API error (repo not found, private, rate limited)
- `422` — Pydantic validation error
- `500` — watsonx.ai error or JSON parse failure

Include `files_analyzed` count in response so the UI can show "Analyzed 18 files".

**Execution order in the endpoint:**
1. `fetch_repo_context(req.repo_url)` → catch ValueError → 400
2. `build_onboarding_prompt(repo_ctx)` → always succeeds
3. `generate_onboarding_kit(prompt)` → catch Exception → 500
4. Return assembled response

---

## FRONTEND — DETAILED SPECIFICATION

### `types/kit.ts` — All Interfaces

```typescript
export interface KeyComponent {
  name: string;
  path: string;
  description: string;
}

export interface ComplexityHotspot {
  name: string;
  path: string;
  reason: string;
  tip: string;
}

export interface FirstTask {
  title: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

export interface CommonPattern {
  pattern: string;
  description: string;
  example: string;
}

export interface SetupSummary {
  prerequisites: string[];
  install_steps: string[];
  run_command: string;
  test_command: string;
  notes: string;
}

export interface OnboardingKit {
  architecture_overview: string;
  key_components: KeyComponent[];
  complexity_hotspots: ComplexityHotspot[];
  suggested_first_tasks: FirstTask[];
  common_patterns: CommonPattern[];
  setup_summary: SetupSummary;
}

export interface AnalyzeResponse {
  owner: string;
  repo: string;
  description: string;
  language: string;
  stars: number;
  forks: number;
  topics: string[];
  files_analyzed: number;
  kit: OnboardingKit;
}
```

---

### `lib/api.ts`

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function analyzeRepo(repoUrl: string): Promise<AnalyzeResponse> {
  const res = await fetch(`${API_URL}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repo_url: repoUrl }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed with status ${res.status}`);
  }
  return res.json();
}
```

---

### Page States & Design

**Design System:**
- Background: `#0f0f0f` (near-black)
- Surface cards: `#1a1a1a` with `border border-[#2a2a2a]`
- IBM Blue accent: `#0062FF`
- IBM Blue hover: `#0053d6`
- Text primary: `#f4f4f4`
- Text muted: `#8d8d8d`
- Code/monospace: `#a8ff78` on `#161616` background
- Success green: `#24a148`
- Warning yellow: `#f1c21b`
- Error red: `#da1e28`
- Font: `Inter` (import from Google Fonts in layout.tsx)
- Border radius: `rounded-lg` (8px)

**State 1 — Idle (Hero)**

Full-screen centered layout:
```
[DevLift logo — simple wordmark in IBM Blue]
[Tagline: "Understand any codebase in 60 seconds"]
[Sub-tagline: "Paste a GitHub URL. Get an AI-generated onboarding kit. Powered by IBM watsonx.ai."]

[──────────────────────────────────────────] [Generate Kit →]
  https://github.com/owner/repo

[Recent: fastapi/fastapi  •  vercel/next.js  •  ...]   ← from localStorage
```

On submit: validate URL starts with `https://github.com/` — show inline error if not.

**State 2 — Loading**

Show centered progress block:
```
[Animated pulsing IBM blue dots]
Analyzing repository with IBM watsonx.ai...

[Step indicators — each lights up in sequence every 4 seconds]
✓ Fetching repository files
⟳ Reading code with Granite model          ← current step
○ Building your onboarding kit
○ Done
```

Estimated time note: "This usually takes 20–40 seconds"

**State 3 — Result**

Layout:
```
[← Analyze another repo]

╔════════════════════════════════════════════╗
║  owner/repo-name                           ║
║  Description text here                     ║
║  [Python] [★ 12,400] [⑂ 890] [18 files]  ║
║  [topic] [topic] [topic]                   ║
╚════════════════════════════════════════════╝

[Tab bar]
Architecture | Components | Hotspots | First Tasks | Patterns | Setup

[Active tab content rendered below]

[Download as Markdown ↓]
```

**State 4 — Error**

```
[Red bordered box]
⚠ Could not analyze this repository

{error message}

[Try a different repo]  [Retry]
```

---

### Section Components

**`ArchitectureSection.tsx`**
- Render `kit.architecture_overview` as formatted prose
- Split into paragraphs on `\n\n` or `\n`
- Each paragraph in its own `<p>` tag with `mb-4`

**`ComponentsSection.tsx`**
- Grid of cards (2 columns on desktop, 1 on mobile)
- Each card: component name (bold, white) + path (monospace, IBM blue, small) + description (gray)
- Card has subtle left border in IBM blue: `border-l-4 border-[#0062FF]`

**`HotspotsSection.tsx`**
- Each hotspot: yellow warning icon + name (bold) + path (monospace small, muted)
- "Why it's complex:" section with `reason` text
- Yellow callout box: "Tip: {tip}"

**`TasksSection.tsx`**
- Each task: title (bold) + difficulty badge + description
- Difficulty badges:
  - `easy` → green pill: `bg-[#071908] text-[#24a148] border border-[#24a148]`
  - `medium` → yellow pill: `bg-[#1c1500] text-[#f1c21b] border border-[#f1c21b]`
  - `hard` → red pill: `bg-[#160b0b] text-[#da1e28] border border-[#da1e28]`
- Sort so easy tasks appear first

**`PatternsSection.tsx`**
- Each pattern: name (bold, large) + description + example in code block
- Example code block: dark background `#161616`, monospace font, horizontal scroll

**`SetupSection.tsx`**
- Prerequisites: rendered as pill tags (`bg-[#1a1a1a] border border-[#2a2a2a]`)
- Install steps: numbered list with monospace commands highlighted
- Run command: large code block with copy button
- Test command: smaller code block with copy button
- Notes: italic text in muted color

---

### `DownloadButton.tsx`

Convert the full kit to markdown:

```markdown
# DevLift Onboarding Kit: owner/repo
Generated by DevLift powered by IBM watsonx.ai
Date: {ISO date}

## Architecture Overview
{architecture_overview}

## Key Components
{for each component: ### {name}\n**Path:** `{path}`\n{description}}

## Complexity Hotspots
{for each hotspot: ### {name}\n**Path:** `{path}`\n**Why:** {reason}\n**Tip:** {tip}}

## Suggested First Tasks
{for each task: ### [{difficulty}] {title}\n{description}}

## Common Patterns
{for each pattern: ### {pattern}\n{description}\n\n**Example:** {example}}

## Setup & Run
### Prerequisites
{bullet list}
### Installation
{numbered list}
### Run
```{run_command}```
### Tests
```{test_command}```
### Notes
{notes}
```

Trigger download as `devlift-{repo-name}-kit.md`

---

### localStorage — Recent Repos

Store last 5 analyzed repos in `localStorage` key `devlift_recent`:
```json
[
  {"url": "https://github.com/tiangolo/fastapi", "repo": "fastapi", "language": "Python"},
  ...
]
```

Show as clickable chips below the input in the idle state. Clicking a chip populates the input.

---

## TESTS

### `tests/test_github_fetcher.py`

```python
import pytest
from github_fetcher import parse_github_url, is_text_file, score_file

def test_parse_valid_url():
    owner, repo = parse_github_url("https://github.com/tiangolo/fastapi")
    assert owner == "tiangolo"
    assert repo == "fastapi"

def test_parse_url_with_git_suffix():
    owner, repo = parse_github_url("https://github.com/tiangolo/fastapi.git")
    assert repo == "fastapi"

def test_parse_invalid_url_raises():
    with pytest.raises(ValueError):
        parse_github_url("https://gitlab.com/owner/repo")

def test_parse_bare_domain_raises():
    with pytest.raises(ValueError):
        parse_github_url("https://github.com/owner")

def test_is_text_file_py():
    assert is_text_file("src/main.py") is True

def test_is_text_file_png():
    assert is_text_file("assets/logo.png") is False

def test_is_text_file_lock():
    assert is_text_file("package-lock.json") is False  # .lock extension

def test_score_readme_highest():
    readme_score = score_file("README.md", "README.md")
    deep_test_score = score_file("src/tests/unit/helpers/test_util.py", "test_util.py")
    assert readme_score > deep_test_score

def test_score_penalizes_depth():
    shallow = score_file("main.py", "main.py")
    deep = score_file("a/b/c/d/main.py", "main.py")
    assert shallow > deep

def test_score_penalizes_tests():
    normal = score_file("src/utils.py", "utils.py")
    test_file = score_file("src/test_utils.py", "test_utils.py")
    assert normal > test_file
```

### `tests/test_prompt_builder.py`

```python
from prompt_builder import build_onboarding_prompt

MOCK_CONTEXT = {
    "owner": "acme",
    "repo": "widget-service",
    "description": "A widget management service",
    "language": "Python",
    "stars": 42,
    "forks": 7,
    "topics": ["api", "widgets"],
    "file_tree": "README.md\nsrc/\n  main.py",
    "files": [
        {"path": "README.md", "content": "# Widget Service\nInstall and run."},
        {"path": "src/main.py", "content": "def main():\n    pass"},
    ],
}

def test_prompt_contains_repo_name():
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    assert "acme/widget-service" in prompt

def test_prompt_contains_file_tree():
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    assert MOCK_CONTEXT["file_tree"] in prompt

def test_prompt_contains_file_contents():
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    assert "def main():" in prompt

def test_prompt_requests_json_only():
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    assert "Return ONLY the JSON object" in prompt

def test_prompt_contains_all_six_keys():
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    for key in ["architecture_overview", "key_components", "complexity_hotspots",
                "suggested_first_tasks", "common_patterns", "setup_summary"]:
        assert key in prompt

def test_prompt_contains_stars():
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    assert "42" in prompt
```

---

## README.md CONTENT

Ask Bob to write the README. Tell it to follow this structure:

```markdown
# DevLift

> Understand any codebase in 60 seconds. Powered by IBM watsonx.ai.

[One-paragraph description: what it does, who it's for, how it works]

## Demo
[GIF/screenshot placeholder]

## The Problem
[2-3 sentences on onboarding pain and cost]

## Features
- Architecture Overview — understand the big picture immediately
- Key Components Map — know exactly which files matter and why
- Complexity Hotspots — find the tricky code before you touch it
- Suggested First Tasks — know where to start contributing
- Common Patterns — learn the unwritten conventions
- Setup Guide — get running without the guesswork
- Download as Markdown — take your onboarding kit anywhere

## How It Works
GitHub URL → GitHub API (smart file selection) → IBM watsonx.ai Granite model → Structured Onboarding Kit

## Tech Stack
[table]

## Quick Start
### Backend
[steps]

### Frontend
[steps]

## Environment Variables
[table with description of each]

## Built with IBM Bob
This project was entirely developed using IBM Bob as the AI development partner. Bob was used to scaffold all backend modules, generate the frontend components, write tests, produce this README, and debug issues during development. The IBM Bob export report is available in `/bob-report/`.

## License
MIT
```

---

## DEPLOYMENT GUIDE

### Backend → Railway (recommended, free tier)

1. Push repo to GitHub (public)
2. Go to railway.app → New Project → Deploy from GitHub repo
3. Select `devlift` repo → set root directory to `backend`
4. Add environment variables in the Variables tab:
   - `WATSONX_API_KEY`
   - `WATSONX_PROJECT_ID`
   - `WATSONX_URL`
   - `GITHUB_TOKEN`
5. Railway auto-detects Python and creates a start command. Override it to:
   `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Copy the Railway public URL (e.g. `https://devlift-backend.up.railway.app`)

### Frontend → Vercel

1. Go to vercel.com → Add New Project → Import Git Repository
2. Set root directory to `frontend`
3. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-railway-url.up.railway.app`
4. Deploy → copy the Vercel URL for submission

---

## IBM BOB SESSION PLAN

Run these Bob sessions in order. Each one becomes a task in your exported report.

| # | Session Task | Prompt to give Bob |
|---|---|---|
| 1 | Understand watsonx | "Explain how to use `ibm-watsonx-ai` Python SDK to call the `ibm/granite-34b-code-instruct` model. Show me a complete working example with ModelInference." |
| 2 | Build github_fetcher | "Write `github_fetcher.py` according to this spec: [paste the github_fetcher section]" |
| 3 | Build prompt_builder | "Write `prompt_builder.py` according to this spec: [paste the prompt_builder section]" |
| 4 | Build bob_client | "Write `bob_client.py` according to this spec: [paste the bob_client section]" |
| 5 | Build main.py | "Write `main.py` for a FastAPI app with /health and /analyze endpoints according to this spec: [paste]" |
| 6 | Generate tests | "Write `tests/test_github_fetcher.py` and `tests/test_prompt_builder.py` according to these test specs: [paste]" |
| 7 | Build frontend types + API | "Create `types/kit.ts` and `lib/api.ts` for a Next.js app according to this spec: [paste]" |
| 8 | Build main page | "Build `app/page.tsx` with idle, loading, result, and error states for DevLift: [paste design spec]" |
| 9 | Build section components | "Build these 6 React components for the kit sections: [paste section specs]" |
| 10 | Write README | "Write a complete README.md for the DevLift project following this structure: [paste README section]" |
| 11 | Debug any errors | Paste actual error messages → ask Bob to identify root cause and fix |

---

## DEMO SCRIPT (for video recording, 2–3 minutes)

**Opening (15s):** "Onboarding to a new codebase takes days. DevLift fixes that. Let me show you."

**Demo 1 — Fast repo (30s):**
- Paste: `https://github.com/expressjs/express`
- Show loading state (Bob reading repo)
- Walk to Architecture tab: "In seconds, Bob has understood the entire structure."
- Click Components tab: "Here are the 7 files you need to read first."

**Demo 2 — Hotspots (30s):**
- Click Hotspots tab: "This is where it gets powerful. Bob found the complex areas and tells you exactly what to watch out for."
- Show one hotspot with its tip.

**Demo 3 — First Tasks (20s):**
- Click First Tasks tab: "For a new hire, here are concrete things they can actually do on day one."
- Show difficulty badges.

**Demo 4 — Setup (20s):**
- Click Setup tab: "No more reading 3 different files to figure out how to run this. It's all here."
- Show run command with copy button.

**Demo 5 — Download (15s):**
- Click "Download as Markdown": "Take your onboarding kit to Notion, Confluence, wherever your team works."

**Closing (10s):** "DevLift — built with IBM Bob, powered by IBM watsonx.ai. Onboarding in 60 seconds, not 3 weeks."

---

## SLIDE DECK (7 slides)

1. **Title slide** — "DevLift" + tagline + logo + "Built with IBM Bob"
2. **The Problem** — stat: "Average developer onboarding time: 1–3 weeks. Cost: $15k–30k per engineer per new project." Pain point visual.
3. **The Solution** — screenshot of the app + "Paste a URL → Get your onboarding kit in 60 seconds"
4. **How IBM Bob Powers It** — two-part diagram: (left) Bob used to BUILD DevLift, (right) Bob's capabilities EMBEDDED in DevLift via watsonx.ai
5. **Demo** — animated GIF or screenshot of all 6 kit sections
6. **Business Value** — who benefits: engineering managers, new hires, open source contributors, teams in M&A due diligence, devs switching between repos
7. **What's Next** — VS Code extension, GitHub Action, Slack bot that sends kit when a PR is opened from a new contributor

---

## SUBMISSION CHECKLIST

- [ ] Code pushed to **public** GitHub repo
- [ ] IBM Bob report exported and placed in `/bob-report/` folder in repo
- [ ] Backend deployed to Railway with working `/health` endpoint
- [ ] Frontend deployed to Vercel — live URL accessible
- [ ] Demo video recorded (2–3 min, follows script above)
- [ ] Slide deck completed (7 slides)
- [ ] Cover image created (1280×720 recommended)
- [ ] Submission form filled: title, short desc, long desc, tags, all URLs

**Project Title:** DevLift

**Short Description (one line):**
Paste a GitHub URL and get an AI-powered onboarding kit in 60 seconds — built with IBM Bob, powered by IBM watsonx.ai.

**Long Description:**
DevLift solves the costly problem of developer onboarding. Every time an engineer joins a new team or picks up an unfamiliar repository, they spend days just getting oriented — reading stale docs, asking senior engineers, and guessing at architecture. DevLift eliminates this friction. Paste a GitHub repository URL and within 60 seconds, IBM watsonx.ai (Granite model) analyzes the codebase and generates a structured Onboarding Kit: architecture overview, key component map, complexity hotspots, suggested first tasks, common patterns, and a setup guide. IBM Bob was the development partner throughout — used to scaffold every backend module, build the React components, generate tests, and write documentation. The result is a working proof-of-concept that directly demonstrates Bob's core capabilities: reading full repository context, explaining logic with clarity, and streamlining the most repetitive parts of software development.

**Tags:** AI, Developer Tools, IBM watsonx.ai, Productivity, Onboarding, FastAPI, Next.js
