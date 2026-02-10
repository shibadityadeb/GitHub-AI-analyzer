

from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.models.schemas import (
    GitHubUser,
    Repository,
    CommitActivity,
    LanguageStats,
    ScoreComponent,
    ScoreBreakdown
)
from app.core.config import settings


class ScoringEngine:
    """
    Calculates a comprehensive GitHub Portfolio Score.
    
    Scoring Components:
    - Activity & Consistency (25%): Commit frequency, streaks, recency
    - Documentation & Readability (20%): READMEs, descriptions, code comments
    - Project Quality & Originality (25%): Stars, uniqueness, complexity
    - Professionalism & Branding (15%): Profile completeness, bio, links
    - Impact & Collaboration (15%): Followers, forks, contributions
    """
    
    def __init__(self):
        self.weights = {
            "activity": settings.WEIGHT_ACTIVITY,
            "documentation": settings.WEIGHT_DOCUMENTATION,
            "quality": settings.WEIGHT_QUALITY,
            "professionalism": settings.WEIGHT_PROFESSIONALISM,
            "impact": settings.WEIGHT_IMPACT
        }
    
    async def calculate_score(
        self,
        profile: GitHubUser,
        repos: List[Repository],
        commit_activity: CommitActivity,
        language_stats: LanguageStats,
        readme_count: int
    ) -> ScoreBreakdown:
        """
        Calculate comprehensive portfolio score.
        
        Args:
            profile: GitHub user profile
            repos: List of repositories
            commit_activity: Commit statistics
            language_stats: Language usage statistics
            readme_count: Number of repos with README
            
        Returns:
            ScoreBreakdown with all components
        """
        
        # Calculate each component
        activity_score = self._calculate_activity_score(
            commit_activity, profile, repos
        )
        
        documentation_score = self._calculate_documentation_score(
            repos, readme_count
        )
        
        quality_score = self._calculate_quality_score(
            repos, language_stats
        )
        
        professionalism_score = self._calculate_professionalism_score(
            profile
        )
        
        impact_score = self._calculate_impact_score(
            profile, repos
        )
        
        # Calculate weighted final score
        final_score = (
            (activity_score.score * self.weights["activity"]) +
            (documentation_score.score * self.weights["documentation"]) +
            (quality_score.score * self.weights["quality"]) +
            (professionalism_score.score * self.weights["professionalism"]) +
            (impact_score.score * self.weights["impact"])
        ) / 100.0
        
        # Determine percentile rank
        percentile_rank = self._get_percentile_rank(final_score)
        
        return ScoreBreakdown(
            activity_and_consistency=activity_score,
            documentation_and_readability=documentation_score,
            project_quality_and_originality=quality_score,
            professionalism_and_branding=professionalism_score,
            impact_and_collaboration=impact_score,
            final_score=round(final_score, 1),
            percentile_rank=percentile_rank
        )
    
    def _calculate_activity_score(
        self,
        commit_activity: CommitActivity,
        profile: GitHubUser,
        repos: List[Repository]
    ) -> ScoreComponent:
        """
        Calculate Activity & Consistency Score (0-100).
        
        Factors:
        - Commit frequency (40%)
        - Recent activity (30%)
        - Consistency/streaks (20%)
        - Account age consideration (10%)
        """
        score = 0.0
        details = {}
        
        # 1. Commit frequency (40 points)
        # Good benchmark: 15+ commits/month = excellent
        frequency_score = min(commit_activity.commit_frequency / 15 * 40, 40)
        score += frequency_score
        details["commit_frequency"] = {
            "value": commit_activity.commit_frequency,
            "score": round(frequency_score, 1)
        }
        
        # 2. Recent activity (30 points)
        # Recent commits in last year
        recent_score = min(commit_activity.recent_commits / 100 * 30, 30)
        score += recent_score
        details["recent_activity"] = {
            "commits_last_year": commit_activity.recent_commits,
            "score": round(recent_score, 1)
        }
        
        # 3. Consistency - longest streak (20 points)
        # 30+ day streak = excellent
        streak_score = min(commit_activity.longest_streak / 30 * 20, 20)
        score += streak_score
        details["consistency"] = {
            "longest_streak_days": commit_activity.longest_streak,
            "current_streak_days": commit_activity.current_streak,
            "score": round(streak_score, 1)
        }
        
        # 4. Account maturity bonus (10 points)
        created_date = datetime.fromisoformat(
            profile.created_at.replace("Z", "+00:00")
        )
        account_age_years = (datetime.now() - created_date).days / 365
        maturity_score = min(account_age_years / 2 * 10, 10)  # 2 years = full points
        score += maturity_score
        details["account_maturity"] = {
            "years": round(account_age_years, 1),
            "score": round(maturity_score, 1)
        }
        
        weighted_score = (score * self.weights["activity"]) / 100
        
        return ScoreComponent(
            score=round(score, 1),
            weight=self.weights["activity"],
            weighted_score=round(weighted_score, 1),
            details=details
        )
    
    def _calculate_documentation_score(
        self,
        repos: List[Repository],
        readme_count: int
    ) -> ScoreComponent:
        """
        Calculate Documentation & Readability Score (0-100).
        
        Factors:
        - README presence (50%)
        - Repository descriptions (30%)
        - Project documentation features (20%)
        """
        score = 0.0
        details = {}
        
        if not repos:
            return ScoreComponent(
                score=0.0,
                weight=self.weights["documentation"],
                weighted_score=0.0,
                details={"error": "No repositories found"}
            )
        
        # 1. README coverage (50 points)
        readme_ratio = readme_count / len(repos)
        readme_score = readme_ratio * 50
        score += readme_score
        details["readme_coverage"] = {
            "repos_with_readme": readme_count,
            "total_repos": len(repos),
            "percentage": round(readme_ratio * 100, 1),
            "score": round(readme_score, 1)
        }
        
        # 2. Repository descriptions (30 points)
        repos_with_description = sum(1 for repo in repos if repo.description)
        description_ratio = repos_with_description / len(repos)
        description_score = description_ratio * 30
        score += description_score
        details["description_coverage"] = {
            "repos_with_description": repos_with_description,
            "percentage": round(description_ratio * 100, 1),
            "score": round(description_score, 1)
        }
        
        # 3. Documentation features (20 points)
        # Wiki, GitHub Pages, Issues enabled
        wiki_count = sum(1 for repo in repos if repo.has_wiki)
        pages_count = sum(1 for repo in repos if repo.has_pages)
        issues_count = sum(1 for repo in repos if repo.has_issues)
        
        feature_score = (
            (wiki_count / len(repos)) * 7 +
            (pages_count / len(repos)) * 7 +
            (issues_count / len(repos)) * 6
        )
        score += feature_score
        details["documentation_features"] = {
            "wikis_enabled": wiki_count,
            "pages_enabled": pages_count,
            "issues_enabled": issues_count,
            "score": round(feature_score, 1)
        }
        
        weighted_score = (score * self.weights["documentation"]) / 100
        
        return ScoreComponent(
            score=round(score, 1),
            weight=self.weights["documentation"],
            weighted_score=round(weighted_score, 1),
            details=details
        )
    
    def _calculate_quality_score(
        self,
        repos: List[Repository],
        language_stats: LanguageStats
    ) -> ScoreComponent:
        """
        Calculate Project Quality & Originality Score (0-100).
        
        Factors:
        - Stars and engagement (35%)
        - Language diversity (25%)
        - Project freshness (20%)
        - Original projects vs forks (20%)
        """
        score = 0.0
        details = {}
        
        if not repos:
            return ScoreComponent(
                score=0.0,
                weight=self.weights["quality"],
                weighted_score=0.0,
                details={"error": "No repositories found"}
            )
        
        # 1. Stars and engagement (35 points)
        total_stars = sum(repo.stargazers_count for repo in repos)
        total_forks = sum(repo.forks_count for repo in repos)
        engagement = total_stars + (total_forks * 2)  # Forks weighted higher
        
        # Benchmark: 50+ engagement = excellent for students
        engagement_score = min(engagement / 50 * 35, 35)
        score += engagement_score
        details["engagement"] = {
            "total_stars": total_stars,
            "total_forks": total_forks,
            "engagement_score_value": engagement,
            "score": round(engagement_score, 1)
        }
        
        # 2. Language diversity (25 points)
        diversity_score = min(language_stats.language_diversity / 5 * 25, 25)
        score += diversity_score
        details["language_diversity"] = {
            "unique_languages": language_stats.language_diversity,
            "primary_language": language_stats.primary_language,
            "score": round(diversity_score, 1)
        }
        
        # 3. Project freshness (20 points)
        # Check how many repos updated in last 6 months
        six_months_ago = datetime.now() - timedelta(days=180)
        recent_updates = sum(
            1 for repo in repos
            if datetime.fromisoformat(
                repo.updated_at.replace("Z", "+00:00")
            ) >= six_months_ago
        )
        freshness_ratio = recent_updates / len(repos)
        freshness_score = freshness_ratio * 20
        score += freshness_score
        details["project_freshness"] = {
            "recently_updated": recent_updates,
            "percentage": round(freshness_ratio * 100, 1),
            "score": round(freshness_score, 1)
        }
        
        # 4. Original projects vs tutorials (20 points)
        # Heuristic: repos with unique names, descriptions, good size
        original_projects = sum(
            1 for repo in repos
            if not any(
                keyword in repo.name.lower()
                for keyword in ["tutorial", "practice", "learning", "course", "homework"]
            )
            and repo.size > 100  # At least 100KB
        )
        originality_ratio = original_projects / len(repos)
        originality_score = originality_ratio * 20
        score += originality_score
        details["originality"] = {
            "original_projects": original_projects,
            "percentage": round(originality_ratio * 100, 1),
            "score": round(originality_score, 1)
        }
        
        weighted_score = (score * self.weights["quality"]) / 100
        
        return ScoreComponent(
            score=round(score, 1),
            weight=self.weights["quality"],
            weighted_score=round(weighted_score, 1),
            details=details
        )
    
    def _calculate_professionalism_score(
        self,
        profile: GitHubUser
    ) -> ScoreComponent:
        """
        Calculate Professionalism & Branding Score (0-100).
        
        Factors:
        - Profile completeness (40%)
        - Professional presentation (30%)
        - Online presence links (30%)
        """
        score = 0.0
        details = {}
        
        # 1. Profile completeness (40 points)
        completeness_fields = {
            "name": profile.name,
            "bio": profile.bio,
            "location": profile.location,
            "email": profile.email,
            "company": profile.company
        }
        
        filled_fields = sum(1 for value in completeness_fields.values() if value)
        completeness_ratio = filled_fields / len(completeness_fields)
        completeness_score = completeness_ratio * 40
        score += completeness_score
        details["profile_completeness"] = {
            "filled_fields": filled_fields,
            "total_fields": len(completeness_fields),
            "percentage": round(completeness_ratio * 100, 1),
            "score": round(completeness_score, 1)
        }
        
        # 2. Professional presentation (30 points)
        presentation_score = 0.0
        
        # Has a meaningful bio (15 points)
        if profile.bio and len(profile.bio) > 20:
            presentation_score += 15
        
        # Marked as hireable (10 points)
        if profile.hireable:
            presentation_score += 10
        
        # Has pinned repos (5 points - inferred from high repo count)
        if profile.public_repos >= 5:
            presentation_score += 5
        
        score += presentation_score
        details["presentation"] = {
            "has_bio": bool(profile.bio),
            "bio_length": len(profile.bio) if profile.bio else 0,
            "hireable": profile.hireable or False,
            "score": round(presentation_score, 1)
        }
        
        # 3. Online presence (30 points)
        presence_score = 0.0
        
        # Personal website/blog (15 points)
        if profile.blog:
            presence_score += 15
        
        # Twitter/social (10 points)
        if profile.twitter_username:
            presence_score += 10
        
        # Company affiliation (5 points)
        if profile.company:
            presence_score += 5
        
        score += presence_score
        details["online_presence"] = {
            "has_website": bool(profile.blog),
            "has_twitter": bool(profile.twitter_username),
            "has_company": bool(profile.company),
            "score": round(presence_score, 1)
        }
        
        weighted_score = (score * self.weights["professionalism"]) / 100
        
        return ScoreComponent(
            score=round(score, 1),
            weight=self.weights["professionalism"],
            weighted_score=round(weighted_score, 1),
            details=details
        )
    
    def _calculate_impact_score(
        self,
        profile: GitHubUser,
        repos: List[Repository]
    ) -> ScoreComponent:
        """
        Calculate Impact & Collaboration Score (0-100).
        
        Factors:
        - Follower count (40%)
        - Repository forks (30%)
        - Contribution indicators (30%)
        """
        score = 0.0
        details = {}
        
        # 1. Followers (40 points)
        # Benchmark: 50+ followers = excellent for students
        follower_score = min(profile.followers / 50 * 40, 40)
        score += follower_score
        details["followers"] = {
            "count": profile.followers,
            "score": round(follower_score, 1)
        }
        
        # 2. Repository forks (30 points)
        total_forks = sum(repo.forks_count for repo in repos)
        # Benchmark: 20+ forks = excellent
        fork_score = min(total_forks / 20 * 30, 30)
        score += fork_score
        details["forks"] = {
            "total_forks": total_forks,
            "score": round(fork_score, 1)
        }
        
        # 3. Collaboration indicators (30 points)
        collab_score = 0.0
        
        # Has repos with contributors (10 points)
        repos_with_forks = sum(1 for repo in repos if repo.forks_count > 0)
        if repos_with_forks > 0:
            collab_score += 10
        
        # Active in open source (has forks from others) (10 points)
        if total_forks > 5:
            collab_score += 10
        
        # Good following/follower ratio (10 points)
        if profile.followers > 0 and profile.following > 0:
            ratio = profile.followers / profile.following
            if ratio >= 0.5:  # Not just following everyone
                collab_score += 10
        
        score += collab_score
        details["collaboration"] = {
            "repos_with_forks": repos_with_forks,
            "following": profile.following,
            "follower_ratio": round(
                profile.followers / max(profile.following, 1), 2
            ),
            "score": round(collab_score, 1)
        }
        
        weighted_score = (score * self.weights["impact"]) / 100
        
        return ScoreComponent(
            score=round(score, 1),
            weight=self.weights["impact"],
            weighted_score=round(weighted_score, 1),
            details=details
        )
    
    def _get_percentile_rank(self, score: float) -> str:
        """Convert score to percentile rank."""
        if score >= 90:
            return "Top 5%"
        elif score >= 80:
            return "Top 15%"
        elif score >= 70:
            return "Top 30%"
        elif score >= 60:
            return "Top 50%"
        else:
            return "Below Average"
