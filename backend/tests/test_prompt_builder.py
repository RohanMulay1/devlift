"""
Tests for prompt_builder module.
"""

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
    """Test that prompt includes the repository name."""
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    assert "acme/widget-service" in prompt


def test_prompt_contains_file_tree():
    """Test that prompt includes the file tree."""
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    assert MOCK_CONTEXT["file_tree"] in prompt


def test_prompt_contains_file_contents():
    """Test that prompt includes file contents."""
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    assert "def main():" in prompt


def test_prompt_requests_json_only():
    """Test that prompt instructs model to return only JSON."""
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    assert "Return ONLY the JSON object" in prompt


def test_prompt_contains_all_six_keys():
    """Test that prompt specifies all six required keys."""
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    for key in ["architecture_overview", "key_components", "complexity_hotspots",
                "suggested_first_tasks", "common_patterns", "setup_summary"]:
        assert key in prompt


def test_prompt_contains_stars():
    """Test that prompt includes repository stars."""
    prompt = build_onboarding_prompt(MOCK_CONTEXT)
    assert "42" in prompt

# Made with Bob
