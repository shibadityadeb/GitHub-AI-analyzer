
import httpx
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from app.core.config import settings
from app.models.schemas import (
    GitHubUser,
    Repository,
    CommitActivity,
    LanguageStats
)


class GitHubService:
    """Service for fetching data from GitHub API."""
    
    def __init__(self):
        self.base_url = settings.GITHUB_API_BASE_URL
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": settings.GITHUB_API_VERSION,
        }
        
        # Add authentication if token is provided
        if settings.GITHUB_TOKEN:
            self.headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"
    
    async def fetch_user_profile(self, username: str) -> GitHubUser:
        """
        Fetch GitHub user profile information.
        
        Args:
            username: GitHub username
            
        Returns:
            GitHubUser model with profile data
            
        Raises:
            httpx.HTTPStatusError: If user not found or API error
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/users/{username}",
                headers=self.headers,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            return GitHubUser(**data)
    
    async def fetch_repositories(self, username: str) -> List[Repository]:
        """
        Fetch all public repositories for a user.
        
        Args:
            username: GitHub username
            
        Returns:
            List of Repository models
        """
        repos = []
        page = 1
        per_page = 100
        
        async with httpx.AsyncClient() as client:
            while len(repos) < settings.MAX_REPOS_TO_ANALYZE:
                response = await client.get(
                    f"{self.base_url}/users/{username}/repos",
                    headers=self.headers,
                    params={
                        "type": "owner",
                        "sort": "updated",
                        "per_page": per_page,
                        "page": page
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                data = response.json()
                
                if not data:
                    break
                
                repos.extend([Repository(**repo) for repo in data])
                
                if len(data) < per_page:
                    break
                
                page += 1
        
        return repos[:settings.MAX_REPOS_TO_ANALYZE]
    
    async def fetch_repo_readme(self, username: str, repo_name: str) -> Optional[Dict[str, Any]]:
        """
        Check if repository has a README file.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            
        Returns:
            README metadata if exists, None otherwise
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/repos/{username}/{repo_name}/readme",
                    headers=self.headers,
                    timeout=10.0
                )
                if response.status_code == 200:
                    return response.json()
                return None
            except httpx.HTTPError:
                return None
    
    async def fetch_repo_languages(self, username: str, repo_name: str) -> Dict[str, int]:
        """
        Fetch language statistics for a repository.
        
        Args:
            username: GitHub username
            repo_name: Repository name
            
        Returns:
            Dictionary mapping language names to bytes of code
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/repos/{username}/{repo_name}/languages",
                    headers=self.headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return {}
    
    async def fetch_commit_activity(
        self,
        username: str,
        repos: List[Repository]
    ) -> CommitActivity:
        """
        Analyze commit activity across all repositories.
        
        Args:
            username: GitHub username
            repos: List of repositories to analyze
            
        Returns:
            CommitActivity model with aggregated statistics
        """
        total_commits = 0
        recent_commits = 0
        commit_dates = []
        
        one_year_ago = datetime.now() - timedelta(days=365)
        
        async with httpx.AsyncClient() as client:
            for repo in repos[:20]:  # Limit to avoid rate limits
                try:
                    # Fetch commits for the repository
                    response = await client.get(
                        f"{self.base_url}/repos/{username}/{repo.name}/commits",
                        headers=self.headers,
                        params={
                            "author": username,
                            "per_page": 100
                        },
                        timeout=10.0
                    )
                    
                    if response.status_code == 200:
                        commits = response.json()
                        total_commits += len(commits)
                        
                        for commit in commits:
                            commit_date_str = commit["commit"]["author"]["date"]
                            commit_date = datetime.fromisoformat(
                                commit_date_str.replace("Z", "+00:00")
                            )
                            commit_dates.append(commit_date)
                            
                            if commit_date >= one_year_ago:
                                recent_commits += 1
                
                except httpx.HTTPError:
                    continue
        
        # Calculate streaks and frequency
        commit_dates.sort()
        longest_streak = self._calculate_longest_streak(commit_dates)
        current_streak = self._calculate_current_streak(commit_dates)
        active_days = len(set(date.date() for date in commit_dates))
        
        # Calculate contribution years
        if commit_dates:
            first_commit = commit_dates[0]
            contribution_years = (datetime.now() - first_commit).days // 365 + 1
        else:
            contribution_years = 0
        
        # Calculate commit frequency (commits per month)
        if commit_dates and len(commit_dates) > 1:
            days_active = (commit_dates[-1] - commit_dates[0]).days + 1
            months_active = max(days_active / 30, 1)
            commit_frequency = total_commits / months_active
        else:
            commit_frequency = 0.0
        
        return CommitActivity(
            total_commits=total_commits,
            recent_commits=recent_commits,
            commit_frequency=round(commit_frequency, 2),
            longest_streak=longest_streak,
            current_streak=current_streak,
            active_days=active_days,
            contribution_years=contribution_years
        )
    
    def _calculate_longest_streak(self, commit_dates: List[datetime]) -> int:
        """Calculate the longest consecutive day streak."""
        if not commit_dates:
            return 0
        
        dates = sorted(set(date.date() for date in commit_dates))
        longest = 1
        current = 1
        
        for i in range(1, len(dates)):
            if (dates[i] - dates[i-1]).days == 1:
                current += 1
                longest = max(longest, current)
            else:
                current = 1
        
        return longest
    
    def _calculate_current_streak(self, commit_dates: List[datetime]) -> int:
        """Calculate current consecutive day streak (including today/yesterday)."""
        if not commit_dates:
            return 0
        
        dates = sorted(set(date.date() for date in commit_dates), reverse=True)
        today = datetime.now().date()
        
        # Check if most recent commit is today or yesterday
        if dates[0] not in [today, today - timedelta(days=1)]:
            return 0
        
        streak = 1
        for i in range(1, len(dates)):
            if (dates[i-1] - dates[i]).days == 1:
                streak += 1
            else:
                break
        
        return streak
    
    async def aggregate_language_stats(
        self,
        username: str,
        repos: List[Repository]
    ) -> LanguageStats:
        """
        Aggregate language statistics across all repositories.
        
        Args:
            username: GitHub username
            repos: List of repositories
            
        Returns:
            LanguageStats model with aggregated data
        """
        language_totals: Dict[str, int] = {}
        
        for repo in repos:
            languages = await self.fetch_repo_languages(username, repo.name)
            for lang, bytes_count in languages.items():
                language_totals[lang] = language_totals.get(lang, 0) + bytes_count
        
        # Determine primary language (most bytes)
        primary_language = None
        if language_totals:
            primary_language = max(language_totals, key=language_totals.get)
        
        return LanguageStats(
            languages=language_totals,
            primary_language=primary_language,
            language_diversity=len(language_totals)
        )
