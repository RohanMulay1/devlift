"""
Prompt builder for IBM watsonx.ai Granite model.
Constructs structured prompts from repository context to generate onboarding kits.
"""

from typing import Dict


def build_onboarding_prompt(repo_context: Dict) -> str:
    """
    Build a structured prompt for the Granite model to generate an onboarding kit.
    
    Args:
        repo_context: Dictionary containing repository metadata and file contents
        
    Returns:
        Formatted prompt string
    """
    owner = repo_context["owner"]
    repo = repo_context["repo"]
    description = repo_context["description"]
    language = repo_context["language"]
    stars = repo_context["stars"]
    forks = repo_context["forks"]
    topics = repo_context["topics"]
    file_tree = repo_context["file_tree"]
    files = repo_context["files"]
    
    # Format topics
    topics_str = ", ".join(topics) if topics else "None"
    
    # Format file contents
    file_contents = []
    for file_info in files:
        file_contents.append(f"--- {file_info['path']} ---\n{file_info['content']}\n")
    file_contents_str = "\n".join(file_contents)
    
    prompt = f"""You are an expert software architect. A new developer has just joined a team and needs to onboard to an unfamiliar codebase as quickly as possible. Your job is to analyze this repository and produce a structured onboarding kit.

You have access to the repository's file tree and the content of its most important files. Base your analysis strictly on what you can see — do not hallucinate file paths or invent functionality that isn't evidenced in the files.

=== REPOSITORY METADATA ===
Name: {owner}/{repo}
Description: {description}
Primary Language: {language}
Stars: {stars} | Forks: {forks}
Topics: {topics_str}

=== FILE TREE (top 2 levels) ===
{file_tree}

=== SELECTED FILE CONTENTS ===
{file_contents_str}

=== OUTPUT INSTRUCTIONS ===
Return a single valid JSON object with exactly these 6 keys. No markdown fences. No explanation before or after. Just the JSON.

{{
  "architecture_overview": "2 paragraphs max: (1) what this project does and its main layers, (2) the request/data flow from entry point to output. Name actual files/dirs. Be specific and concise.",

  "key_components": [
    {{
      "name": "Component name",
      "path": "exact/path.ext",
      "description": "1-2 sentences: what it does and why a new dev must understand it."
    }}
  ],

  "complexity_hotspots": [
    {{
      "name": "Area label",
      "path": "exact/path",
      "reason": "One sentence: why this is complex or risky.",
      "tip": "One sentence: concrete advice for a first-timer."
    }}
  ],

  "suggested_first_tasks": [
    {{
      "title": "Action verb + outcome",
      "description": "1-2 sentences: what to do and which files to touch.",
      "difficulty": "easy | medium | hard"
    }}
  ],

  "common_patterns": [
    {{
      "pattern": "Pattern name",
      "description": "1-2 sentences: how this pattern appears in this codebase specifically.",
      "example": "File path or single short code line illustrating it."
    }}
  ],

  "setup_summary": {{
    "prerequisites": ["Tool >= version"],
    "install_steps": ["exact command or step"],
    "run_command": "single start command",
    "test_command": "single test command",
    "notes": "One specific, non-obvious gotcha for THIS repo — not generic advice like 'install dependencies'. Something a developer would only learn after hitting a problem."
  }}
}}

Requirements:
- key_components: 5–7 items
- complexity_hotspots: 3–4 items
- suggested_first_tasks: 3–5 items (at least 1 easy)
- common_patterns: 3–4 items
- All paths must exist in the file tree above
- Be concise — every field should be as short as possible while still useful
- Return ONLY the JSON object"""

    return prompt

# Made with Bob
