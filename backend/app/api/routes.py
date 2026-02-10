
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Optional
import httpx

from app.models.schemas import AnalysisResult, AnalysisRequest, ErrorResponse
from app.services.github_service import GitHubService
from app.services.scoring_engine import ScoringEngine
from app.services.analyzer import AnalyzerService
from app.services.feedback_generator import FeedbackGenerator
from app.core.config import settings


router = APIRouter()


@router.post(
    "/analyze/{username}",
    response_model=AnalysisResult,
    summary="Analyze GitHub Profile",
    description="Analyzes a GitHub user's profile and generates a recruiter scorecard"
)
async def analyze_profile(
    username: str,
    include_ai_feedback: bool = Query(
        default=True,
        description="Generate AI-powered feedback and recommendations"
    )
):
    """
    Analyze a GitHub profile and generate comprehensive recruiter scorecard.
    
    Args:
        username: GitHub username to analyze
        include_ai_feedback: Whether to include AI-generated feedback
        
    Returns:
        Complete analysis with scores, insights, and recommendations
        
    Raises:
        HTTPException: If user not found or API errors occur
    """
    
    try:
        # Initialize services
        github_service = GitHubService()
        scoring_engine = ScoringEngine()
        analyzer_service = AnalyzerService()
        feedback_generator = FeedbackGenerator()
        
        # ===================================================================
        # STEP 1: Fetch GitHub Data
        # ===================================================================
        
        # Fetch user profile
        profile = await github_service.fetch_user_profile(username)
        
        # Fetch repositories
        repos = await github_service.fetch_repositories(username)
        
        if len(repos) < settings.MIN_REPOS_FOR_ANALYSIS:
            raise HTTPException(
                status_code=400,
                detail=f"User must have at least {settings.MIN_REPOS_FOR_ANALYSIS} public repository to analyze"
            )
        
        # Check README presence for each repo
        readme_count = 0
        for repo in repos:
            readme = await github_service.fetch_repo_readme(username, repo.name)
            if readme:
                readme_count += 1
        
        # Fetch commit activity
        commit_activity = await github_service.fetch_commit_activity(username, repos)
        
        # Aggregate language statistics
        language_stats = await github_service.aggregate_language_stats(username, repos)
        
        # ===================================================================
        # STEP 2: Calculate Scores
        # ===================================================================
        
        score_breakdown = await scoring_engine.calculate_score(
            profile=profile,
            repos=repos,
            commit_activity=commit_activity,
            language_stats=language_stats,
            readme_count=readme_count
        )
        
        # ===================================================================
        # STEP 3: Detect Insights (Strengths, Weaknesses, Red Flags)
        # ===================================================================
        
        strengths = analyzer_service.detect_strengths(
            profile=profile,
            repos=repos,
            commit_activity=commit_activity,
            language_stats=language_stats,
            score_breakdown=score_breakdown
        )
        
        weaknesses = analyzer_service.detect_weaknesses(
            profile=profile,
            repos=repos,
            commit_activity=commit_activity,
            language_stats=language_stats,
            readme_count=readme_count,
            score_breakdown=score_breakdown
        )
        
        red_flags = analyzer_service.detect_red_flags(
            profile=profile,
            repos=repos,
            commit_activity=commit_activity,
            readme_count=readme_count
        )
        
        # ===================================================================
        # STEP 4: Generate AI Feedback (Optional)
        # ===================================================================
        
        ai_feedback = None
        if include_ai_feedback and settings.ANTHROPIC_API_KEY:
            ai_feedback = await feedback_generator.generate_feedback(
                profile=profile,
                repos=repos,
                score_breakdown=score_breakdown,
                strengths=strengths,
                weaknesses=weaknesses,
                red_flags=red_flags
            )
        
        # ===================================================================
        # STEP 5: Calculate Additional Metrics
        # ===================================================================
        
        # Profile completeness percentage
        profile_fields = [
            profile.name,
            profile.bio,
            profile.location,
            profile.email,
            profile.company,
            profile.blog,
            profile.twitter_username
        ]
        filled_fields = sum(1 for field in profile_fields if field)
        profile_completeness = (filled_fields / len(profile_fields)) * 100
        
        # GitHub tenure in days
        created_date = datetime.fromisoformat(profile.created_at.replace("Z", "+00:00"))
        github_tenure_days = (datetime.now() - created_date).days
        
        # ===================================================================
        # STEP 6: Build Response
        # ===================================================================
        
        analysis_result = AnalysisResult(
            username=username,
            analyzed_at=datetime.now(),
            analysis_version="1.0.0",
            profile=profile,
            total_repositories=len(repos),
            analyzed_repositories=min(len(repos), settings.MAX_REPOS_TO_ANALYZE),
            language_stats=language_stats,
            commit_activity=commit_activity,
            score_breakdown=score_breakdown,
            strengths=strengths,
            weaknesses=weaknesses,
            red_flags=red_flags,
            ai_feedback=ai_feedback,
            profile_completeness=round(profile_completeness, 1),
            github_tenure_days=github_tenure_days
        )
        
        return analysis_result
        
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"GitHub user '{username}' not found"
            )
        elif e.response.status_code == 403:
            raise HTTPException(
                status_code=429,
                detail="GitHub API rate limit exceeded. Please try again later or configure GITHUB_TOKEN."
            )
        else:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"GitHub API error: {str(e)}"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/health",
    summary="Service Health Check",
    description="Check if the service and external APIs are configured"
)
async def health_check():
    """
    Health check endpoint.
    
    Returns service status and external API configuration status.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "github_api": {
            "configured": bool(settings.GITHUB_TOKEN),
            "base_url": settings.GITHUB_API_BASE_URL
        },
        "ai_service": {
            "anthropic_configured": bool(settings.ANTHROPIC_API_KEY)
        }
    }
