

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


# ============================================================================
# GitHub Data Models
# ============================================================================

class GitHubUser(BaseModel):
    """GitHub user profile information."""
    login: str
    name: Optional[str] = None
    bio: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    hireable: Optional[bool] = None
    blog: Optional[str] = None
    twitter_username: Optional[str] = None
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str
    updated_at: str
    avatar_url: str


class Repository(BaseModel):
    """GitHub repository information."""
    name: str
    full_name: str
    description: Optional[str] = None
    private: bool
    html_url: str
    created_at: str
    updated_at: str
    pushed_at: str
    size: int
    stargazers_count: int
    watchers_count: int
    forks_count: int
    open_issues_count: int
    language: Optional[str] = None
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    archived: bool
    disabled: bool
    topics: List[str] = []
    license: Optional[Dict[str, Any]] = None


class CommitActivity(BaseModel):
    """Commit activity metrics."""
    total_commits: int
    recent_commits: int  # Last 365 days
    commit_frequency: float  # Commits per month
    longest_streak: int  # Days
    current_streak: int  # Days
    active_days: int
    contribution_years: int


class LanguageStats(BaseModel):
    """Programming language statistics."""
    languages: Dict[str, int]  # {language: bytes}
    primary_language: Optional[str] = None
    language_diversity: int  # Number of unique languages


# ============================================================================
# Contribution Data Models (GraphQL-sourced)
# ============================================================================

class YearlyMetrics(BaseModel):
    """Normalized contribution metrics for a single calendar year."""
    year: int
    total: int = 0
    per_month: float = 0.0
    per_week: float = 0.0
    active_days: int = 0
    active_day_rate: float = Field(
        0.0, description="Average contributions per active day"
    )
    is_partial: bool = Field(
        False, description="True when the year has not ended or has incomplete data"
    )
    is_reliable: bool = Field(
        True, description="False when cross-verification detected a mismatch > 2%"
    )
    calendar_sum: int = Field(
        0, description="Sum of contributionCalendar day counts for cross-check"
    )
    reported_commits: int = Field(
        0, description="totalCommitContributions reported by GraphQL"
    )


class ActivityOverview(BaseModel):
    """High-level activity signals derived from multi-year contribution data."""
    moving_average_3yr: float = Field(
        0.0, description="3-year moving average of commits/week"
    )
    momentum_index: float = Field(
        0.0,
        description=(
            "Ratio of latest-year per_week to 3-year average. "
            ">1 = accelerating, <1 = decelerating"
        ),
    )
    volatility_score: float = Field(
        0.0,
        description="Coefficient of variation of per_week across years (0-1 scale, lower = more stable)",
    )
    trend_signal: str = Field(
        "stable",
        description="One of: strong_growth, growth, stable, decline, strong_decline",
    )
    trend_details: str = ""


class ValidationResult(BaseModel):
    """Output of the consistency validator."""
    is_valid: bool = True
    anomalies: List[str] = Field(default_factory=list)
    incomplete_years: List[int] = Field(default_factory=list)
    unreliable_years: List[int] = Field(default_factory=list)


class ContributionData(BaseModel):
    """Accurate contribution data sourced from GitHub GraphQL API v4.

    All date boundaries use strict calendar-year UTC.
    All rate metrics are time-normalized (per_week, per_month, per_active_day).
    Cross-verification is performed between totalCommitContributions and
    contributionCalendar day sums for every year.
    """
    yearly_metrics: List[YearlyMetrics] = Field(default_factory=list)
    total_contributions: int = 0
    current_year_contributions: int = 0
    last_12_months_contributions: int = 0
    weekly_average: float = 0.0
    longest_streak: int = 0
    current_streak: int = 0
    active_days: int = 0
    contribution_breakdown: Dict[str, int] = Field(
        default_factory=dict,
        description="Breakdown by type: commits, pull_requests, reviews, issues, repositories",
    )
    growth_rate: float = Field(0.0, description="Year-over-year growth percentage (per_week basis)")
    is_trending_up: bool = False
    activity_overview: Optional[ActivityOverview] = None
    validation: Optional[ValidationResult] = None


# ============================================================================
# Scoring Models
# ============================================================================

class ScoreComponent(BaseModel):
    """Individual score component with breakdown."""
    score: float = Field(..., ge=0, le=100, description="Score out of 100")
    weight: float = Field(..., ge=0, le=100, description="Weight in final score")
    weighted_score: float = Field(..., description="score * weight / 100")
    details: Dict[str, Any] = Field(default_factory=dict)


class ScoreBreakdown(BaseModel):
    """Complete score breakdown with all components."""
    activity_and_consistency: ScoreComponent
    documentation_and_readability: ScoreComponent
    project_quality_and_originality: ScoreComponent
    professionalism_and_branding: ScoreComponent
    impact_and_collaboration: ScoreComponent
    final_score: float = Field(..., ge=0, le=100)
    percentile_rank: Optional[str] = None  # "Top 10%", "Top 25%", etc.


# ============================================================================
# Analysis Results Models
# ============================================================================

class Strength(BaseModel):
    """Identified strength with evidence."""
    category: str
    title: str
    description: str
    evidence: List[str] = []
    impact: str = Field(..., description="High, Medium, or Low")


class Weakness(BaseModel):
    """Identified weakness with suggestions."""
    category: str
    title: str
    description: str
    severity: str = Field(..., description="Critical, Moderate, or Minor")
    suggestion: str


class RedFlag(BaseModel):
    """Detected red flag with explanation."""
    flag_type: str
    title: str
    description: str
    recruiter_perspective: str
    how_to_fix: str


class ImprovementAction(BaseModel):
    """Actionable improvement item."""
    week: int = Field(..., ge=1, le=4)
    priority: str = Field(..., description="High, Medium, or Low")
    action: str
    expected_impact: str
    time_estimate: str


class ProjectSuggestion(BaseModel):
    """Suggested project to build."""
    title: str
    description: str
    tech_stack: List[str]
    difficulty: str = Field(..., description="Beginner, Intermediate, or Advanced")
    why_it_matters: str
    estimated_time: str


class AIFeedback(BaseModel):
    """AI-generated feedback and recommendations."""
    summary: str
    key_takeaways: List[str]
    roadmap_30_days: List[ImprovementAction]
    project_suggestions: List[ProjectSuggestion]
    recruiter_perspective: str


# ============================================================================
# Main Analysis Response
# ============================================================================

class AnalysisResult(BaseModel):
    """Complete analysis result."""
    
    # Metadata
    username: str
    analyzed_at: datetime
    analysis_version: str = "1.0.0"
    
    # GitHub Data Summary
    profile: GitHubUser
    total_repositories: int
    analyzed_repositories: int
    language_stats: LanguageStats
    commit_activity: CommitActivity
    contribution_data: Optional[ContributionData] = None
    
    # Scoring
    score_breakdown: ScoreBreakdown
    
    # Analysis Insights
    strengths: List[Strength]
    weaknesses: List[Weakness]
    red_flags: List[RedFlag]
    
    # AI-Enhanced Feedback (optional)
    ai_feedback: Optional[AIFeedback] = None
    
    # Additional Metrics
    profile_completeness: float = Field(..., ge=0, le=100)
    github_tenure_days: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "octocat",
                "analyzed_at": "2026-02-10T12:00:00Z",
                "analysis_version": "1.0.0",
                "profile": {
                    "login": "octocat",
                    "name": "The Octocat",
                    "bio": "GitHub's mascot",
                    "public_repos": 8,
                    "followers": 1000,
                    "following": 10,
                    "created_at": "2011-01-25T18:44:36Z"
                },
                "score_breakdown": {
                    "final_score": 78.5,
                    "percentile_rank": "Top 15%"
                }
            }
        }


# ============================================================================
# API Request/Response Models
# ============================================================================

class AnalysisRequest(BaseModel):
    """Request to analyze a GitHub profile."""
    username: str = Field(..., min_length=1, max_length=39, description="GitHub username")
    include_ai_feedback: bool = Field(default=True, description="Generate AI feedback")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
    status_code: int
