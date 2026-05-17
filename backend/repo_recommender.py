"""
Repository recommendation engine.
Uses watsonx.ai to extract search queries and rank GitHub repositories based on user requirements.
"""

import os
import json
import requests
from typing import List, Dict
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference


def _get_model(max_tokens: int = 512) -> ModelInference:
    """Initialize watsonx.ai model with specified token limit."""
    credentials = Credentials(
        url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
        api_key=os.getenv("WATSONX_API_KEY"),
    )
    return ModelInference(
        model_id="meta-llama/llama-3-3-70b-instruct",
        credentials=credentials,
        project_id=os.getenv("WATSONX_PROJECT_ID"),
        params={
            "max_new_tokens": max_tokens,
            "temperature": 0.3,
            "top_p": 0.9,
            "repetition_penalty": 1.1,
        },
    )


def _extract_search_queries(requirement: str) -> List[str]:
    """
    Use watsonx.ai to extract 3-5 GitHub search queries from the requirement.
    
    Args:
        requirement: User's project requirement description
        
    Returns:
        List of search query strings
    """
    prompt = f"""Given this project requirement, extract 3-5 GitHub search queries that would find relevant repositories.
Each query should be a short keyword string suitable for GitHub search (e.g. "express nodejs web framework").

Requirement: {requirement}

Output ONLY valid JSON in this exact format:
{{"queries": ["query1", "query2", "query3"]}}

JSON:"""

    model = _get_model(max_tokens=512)
    response = model.generate_text(prompt=prompt)
    
    # Clean response
    response = response.strip()
    if response.startswith("```"):
        response = response.split("```")[1]
        if response.startswith("json"):
            response = response[4:]
    
    # Extract JSON
    start = response.find("{")
    end = response.rfind("}") + 1
    if start >= 0 and end > start:
        response = response[start:end]
    
    start = response.find("{")
    if start == -1:
        return []
    data, _ = json.JSONDecoder().raw_decode(response, start)
    return data.get("queries", [])


def _search_github(query: str, per_page: int = 5) -> List[Dict]:
    """
    Search GitHub repositories using the GitHub API.
    
    Args:
        query: Search query string
        per_page: Number of results per query
        
    Returns:
        List of repository data dicts
    """
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": per_page
    }
    
    headers = {}
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except Exception as e:
        print(f"GitHub search error for query '{query}': {e}")
        return []


def _rank_candidates(requirement: str, candidates: List[Dict]) -> List[Dict]:
    """
    Use watsonx.ai to rank and select the best 3-5 repositories from candidates.
    
    Args:
        requirement: Original user requirement
        candidates: List of candidate repository dicts
        
    Returns:
        List of selected repositories with 'why' explanations
    """
    # Format candidates for the prompt
    candidates_text = ""
    for i, repo in enumerate(candidates, 1):
        candidates_text += f"{i}. {repo['full_name']}\n"
        candidates_text += f"   Description: {repo.get('description', 'No description')}\n"
        candidates_text += f"   Stars: {repo['stargazers_count']:,} | Language: {repo.get('language', 'Unknown')}\n\n"
    
    prompt = f"""Given this project requirement and list of GitHub repositories, select the best 3-5 repositories that match the requirement.
For each selected repository, explain in 1-2 sentences why it's a good match.

Requirement: {requirement}

Candidate Repositories:
{candidates_text}

Output ONLY valid JSON in this exact format:
[
  {{"full_name": "owner/repo", "why": "Explanation of why this repo matches"}},
  {{"full_name": "owner/repo", "why": "Explanation of why this repo matches"}}
]

Select 3-5 repositories. Order them by relevance (best match first).

JSON:"""

    model = _get_model(max_tokens=2048)
    response = model.generate_text(prompt=prompt)
    
    # Clean response
    response = response.strip()
    if response.startswith("```"):
        response = response.split("```")[1]
        if response.startswith("json"):
            response = response[4:]
    
    # Extract JSON array
    start = response.find("[")
    end = response.rfind("]") + 1
    if start >= 0 and end > start:
        response = response[start:end]
    
    start = response.find("[")
    if start == -1:
        return []
    selections, _ = json.JSONDecoder().raw_decode(response, start)
    return selections


def recommend_repos(requirement: str) -> List[Dict]:
    """
    Main recommendation function: extract queries, search GitHub, rank results.
    
    Args:
        requirement: User's project requirement description
        
    Returns:
        List of repository suggestion dicts matching RepoSuggestion schema
    """
    # Step 1: Extract search queries
    queries = _extract_search_queries(requirement)
    if not queries:
        raise ValueError("Failed to extract search queries from requirement")
    
    # Step 2: Search GitHub for each query and collect candidates
    all_candidates = []
    seen_full_names = set()
    
    for query in queries[:5]:  # Limit to 5 queries max
        results = _search_github(query, per_page=5)
        for repo in results:
            full_name = repo["full_name"]
            if full_name not in seen_full_names:
                seen_full_names.add(full_name)
                all_candidates.append(repo)
    
    if not all_candidates:
        raise ValueError("No repositories found matching the requirement")
    
    # Keep top 10 candidates by stars
    all_candidates.sort(key=lambda r: r["stargazers_count"], reverse=True)
    top_candidates = all_candidates[:10]
    
    # Step 3: Use AI to rank and select best matches
    selections = _rank_candidates(requirement, top_candidates)
    
    # Step 4: Match selections back to GitHub data
    suggestions = []
    for selection in selections[:5]:  # Max 5 suggestions
        full_name = selection["full_name"]
        why = selection["why"]
        
        # Find matching candidate
        repo_data = next((r for r in top_candidates if r["full_name"] == full_name), None)
        if repo_data:
            suggestions.append({
                "owner": repo_data["owner"]["login"],
                "repo": repo_data["name"],
                "full_name": repo_data["full_name"],
                "description": repo_data.get("description", "No description available"),
                "stars": repo_data["stargazers_count"],
                "forks": repo_data["forks_count"],
                "language": repo_data.get("language", "Unknown"),
                "url": repo_data["html_url"],
                "why": why
            })
    
    return suggestions


# Made with Bob