"""
DevLift FastAPI backend.
Provides endpoints for analyzing GitHub repositories and generating onboarding kits.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from github_fetcher import fetch_repo_context, calculate_readiness_score
from prompt_builder import build_onboarding_prompt
from bob_client import generate_onboarding_kit
from repo_recommender import recommend_repos

# Load environment variables
load_dotenv()

app = FastAPI(
    title="DevLift API",
    description="Instant AI-powered onboarding kits for any GitHub repository",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    """Request model for repository analysis."""
    repo_url: str


class AnalyzeResponse(BaseModel):
    """Response model for repository analysis."""
    owner: str
    repo: str
    description: str
    language: str
    stars: int
    forks: int
    topics: list[str]
    files_analyzed: int
    kit: dict
    readiness: dict


class RecommendRequest(BaseModel):
    """Request model for repository recommendation."""
    requirement: str


class RepoSuggestion(BaseModel):
    """Model for a single repository suggestion."""
    owner: str
    repo: str
    full_name: str
    description: str
    stars: int
    forks: int
    language: str
    url: str
    why: str


class RecommendResponse(BaseModel):
    """Response model for repository recommendations."""
    suggestions: list[RepoSuggestion]


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Status information
    """
    return {
        "status": "ok",
        "model": "meta-llama/llama-3-3-70b-instruct"
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_repository(request: AnalyzeRequest):
    """
    Analyze a GitHub repository and generate an onboarding kit.
    
    Args:
        request: Request containing repository URL
        
    Returns:
        Repository metadata and generated onboarding kit
        
    Raises:
        HTTPException: 400 for invalid URL/GitHub errors, 500 for AI errors
    """
    try:
        # Step 1: Fetch repository context
        repo_context = fetch_repo_context(request.repo_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch repository: {str(e)}")
    
    try:
        # Step 2: Build prompt
        prompt = build_onboarding_prompt(repo_context)
        
        # Step 3: Generate onboarding kit with watsonx.ai
        kit = generate_onboarding_kit(prompt)
        
        # Step 4: Calculate contribution readiness score
        readiness = calculate_readiness_score(repo_context, kit)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate onboarding kit: {str(e)}"
        )
    
    # Step 5: Assemble response
    return AnalyzeResponse(
        owner=repo_context["owner"],
        repo=repo_context["repo"],
        description=repo_context["description"],
        language=repo_context["language"],
        stars=repo_context["stars"],
        forks=repo_context["forks"],
        topics=repo_context["topics"],
        files_analyzed=len(repo_context["files"]),
        kit=kit,
        readiness=readiness
    )


@app.post("/recommend", response_model=RecommendResponse)
async def recommend_repositories(request: RecommendRequest):
    """
    Recommend GitHub repositories based on project requirements.
    
    Args:
        request: Request containing project requirement description
        
    Returns:
        List of recommended repositories with explanations
        
    Raises:
        HTTPException: 400 for invalid input, 500 for recommendation errors
    """
    if len(request.requirement.strip()) < 10:
        raise HTTPException(status_code=400, detail="Requirement too short (minimum 10 characters)")
    
    if len(request.requirement) > 2000:
        raise HTTPException(status_code=400, detail="Requirement too long (maximum 2000 characters)")
    
    try:
        suggestions = recommend_repos(request.requirement)
        return RecommendResponse(suggestions=suggestions)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation failed: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Made with Bob
