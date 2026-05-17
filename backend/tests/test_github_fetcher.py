"""
Tests for github_fetcher module.
"""

import pytest
from github_fetcher import parse_github_url, is_text_file, score_file


def test_parse_valid_url():
    """Test parsing a valid GitHub URL."""
    owner, repo = parse_github_url("https://github.com/tiangolo/fastapi")
    assert owner == "tiangolo"
    assert repo == "fastapi"


def test_parse_url_with_git_suffix():
    """Test parsing a URL with .git suffix."""
    owner, repo = parse_github_url("https://github.com/tiangolo/fastapi.git")
    assert repo == "fastapi"


def test_parse_invalid_url_raises():
    """Test that invalid URLs raise ValueError."""
    with pytest.raises(ValueError):
        parse_github_url("https://gitlab.com/owner/repo")


def test_parse_bare_domain_raises():
    """Test that incomplete URLs raise ValueError."""
    with pytest.raises(ValueError):
        parse_github_url("https://github.com/owner")


def test_is_text_file_py():
    """Test that Python files are recognized as text."""
    assert is_text_file("src/main.py") is True


def test_is_text_file_png():
    """Test that image files are not recognized as text."""
    assert is_text_file("assets/logo.png") is False


def test_is_text_file_lock():
    """Test that lock files are not recognized as text."""
    assert is_text_file("yarn.lock") is False  # .lock extension


def test_score_readme_highest():
    """Test that README files get higher scores than test files."""
    readme_score = score_file("README.md", "README.md")
    deep_test_score = score_file("src/tests/unit/helpers/test_util.py", "test_util.py")
    assert readme_score > deep_test_score


def test_score_penalizes_depth():
    """Test that deeper files get lower scores."""
    shallow = score_file("main.py", "main.py")
    deep = score_file("a/b/c/d/main.py", "main.py")
    assert shallow > deep


def test_score_penalizes_tests():
    """Test that test files get lower scores than normal files."""
    normal = score_file("src/utils.py", "utils.py")
    test_file = score_file("src/test_utils.py", "test_utils.py")
    assert normal > test_file

# Made with Bob
