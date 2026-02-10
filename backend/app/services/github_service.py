
import asyncio
import math
import time
import logging
import httpx
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta, timezone, date as _date
from app.core.config import settings
from app.models.schemas import (
    GitHubUser,
    Repository,
    CommitActivity,
    ContributionData,
    YearlyMetrics,
    ActivityOverview,
    ValidationResult,
    LanguageStats
)

logger = logging.getLogger(__name__)

# Semaphore to limit concurrent GitHub API requests
_MAX_CONCURRENT_REQUESTS = 5


class _TTLCache:
    """In-memory TTL cache to avoid redundant GraphQL calls."""

    def __init__(self, ttl_seconds: int = 300):
        self._store: Dict[str, Any] = {}
        self._times: Dict[str, float] = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        if key in self._store:
            if time.time() - self._times[key] < self._ttl:
                return self._store[key]
            del self._store[key]
            del self._times[key]
        return None

    def set(self, key: str, value: Any) -> None:
        self._store[key] = value
        self._times[key] = time.time()


_graphql_cache = _TTLCache(ttl_seconds=300)


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
        
        self._semaphore = asyncio.Semaphore(_MAX_CONCURRENT_REQUESTS)
    
    async def _get(self, client: httpx.AsyncClient, url: str, **kwargs) -> httpx.Response:
        """Rate-limited GET request."""
        async with self._semaphore:
            return await client.get(url, headers=self.headers, timeout=10.0, **kwargs)
    
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
            response = await self._get(client, f"{self.base_url}/users/{username}")
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
                response = await self._get(
                    client,
                    f"{self.base_url}/users/{username}/repos",
                    params={
                        "type": "owner",
                        "sort": "updated",
                        "per_page": per_page,
                        "page": page
                    }
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
    
    async def fetch_repo_readme(self, client: httpx.AsyncClient, username: str, repo_name: str) -> bool:
        """
        Check if repository has a README file.
        
        Args:
            client: Shared httpx client
            username: GitHub username
            repo_name: Repository name
            
        Returns:
            True if README exists, False otherwise
        """
        try:
            response = await self._get(
                client,
                f"{self.base_url}/repos/{username}/{repo_name}/readme"
            )
            return response.status_code == 200
        except httpx.HTTPError:
            return False
    
    async def fetch_repo_languages(self, client: httpx.AsyncClient, username: str, repo_name: str) -> Dict[str, int]:
        """
        Fetch language statistics for a repository.
        
        Args:
            client: Shared httpx client
            username: GitHub username
            repo_name: Repository name
            
        Returns:
            Dictionary mapping language names to bytes of code
        """
        try:
            response = await self._get(
                client,
                f"{self.base_url}/repos/{username}/{repo_name}/languages"
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except httpx.HTTPError:
            return {}
    
    async def _fetch_repo_commits(self, client: httpx.AsyncClient, username: str, repo_name: str) -> List[Dict]:
        """Fetch commits for a single repo."""
        try:
            response = await self._get(
                client,
                f"{self.base_url}/repos/{username}/{repo_name}/commits",
                params={"author": username, "per_page": 100}
            )
            if response.status_code == 200:
                return response.json()
            return []
        except httpx.HTTPError:
            return []
    
    async def fetch_commit_activity(
        self,
        client: httpx.AsyncClient,
        username: str,
        repos: List[Repository]
    ) -> CommitActivity:
        """
        Analyze commit activity across repositories concurrently.
        
        Args:
            client: Shared httpx client
            username: GitHub username
            repos: List of repositories to analyze
            
        Returns:
            CommitActivity model with aggregated statistics
        """
        total_commits = 0
        recent_commits = 0
        commit_dates = []
        
        one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
        
        # Fetch commits concurrently for up to 15 repos
        tasks = [
            self._fetch_repo_commits(client, username, repo.name)
            for repo in repos[:15]
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception) or not isinstance(result, list):
                continue
            
            total_commits += len(result)
            for commit in result:
                try:
                    commit_date_str = commit["commit"]["author"]["date"]
                    commit_date = datetime.fromisoformat(
                        commit_date_str.replace("Z", "+00:00")
                    )
                    commit_dates.append(commit_date)
                    if commit_date >= one_year_ago:
                        recent_commits += 1
                except (KeyError, ValueError):
                    continue
        
        # Calculate streaks and frequency
        commit_dates.sort()
        longest_streak = self._calculate_longest_streak(commit_dates)
        current_streak = self._calculate_current_streak(commit_dates)
        active_days = len(set(date.date() for date in commit_dates))
        
        # Calculate contribution years
        if commit_dates:
            first_commit = commit_dates[0]
            contribution_years = (datetime.now(timezone.utc) - first_commit).days // 365 + 1
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
        today = datetime.now(timezone.utc).date()
        
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
    

    # ===================================================================
    # GraphQL API – Centralized Client (Task 1)
    # ===================================================================

    _GRAPHQL_URL = "https://api.github.com/graphql"
    _MAX_GRAPHQL_RETRIES = 3
    _GRAPHQL_RETRY_BACKOFF = 1.0  # seconds, doubled each retry

    _CONTRIBUTION_FRAGMENT = """
fragment ContribFields on ContributionsCollection {
  totalCommitContributions
  totalIssueContributions
  totalPullRequestContributions
  totalPullRequestReviewContributions
  totalRepositoryContributions
  restrictedContributionsCount
  contributionCalendar {
    totalContributions
    weeks {
      contributionDays {
        contributionCount
        date
      }
    }
  }
}"""

    async def _graphql_query(
        self,
        client: httpx.AsyncClient,
        query: str,
        variables: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Centralized GraphQL executor with retry, rate-limit handling, and
        debug logging.

        Retries on 502/503 and when the ``Retry-After`` header is present
        (secondary rate limit).  Bearer authentication is enforced.
        """
        if not settings.GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN is required for the GraphQL API")

        last_exc: Optional[Exception] = None
        backoff = self._GRAPHQL_RETRY_BACKOFF

        for attempt in range(1, self._MAX_GRAPHQL_RETRIES + 1):
            async with self._semaphore:
                try:
                    response = await client.post(
                        self._GRAPHQL_URL,
                        headers={
                            "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
                            "Content-Type": "application/json",
                        },
                        json={"query": query, "variables": variables},
                        timeout=20.0,
                    )

                    # --- rate-limit / transient error handling ---
                    if response.status_code in (502, 503):
                        logger.warning(
                            "GraphQL %d on attempt %d/%d – retrying in %.1fs",
                            response.status_code, attempt,
                            self._MAX_GRAPHQL_RETRIES, backoff,
                        )
                        await asyncio.sleep(backoff)
                        backoff *= 2
                        continue

                    retry_after = response.headers.get("Retry-After")
                    if response.status_code == 403 and retry_after:
                        wait = min(float(retry_after), 60.0)
                        logger.warning(
                            "GraphQL secondary rate limit – waiting %.0fs", wait
                        )
                        await asyncio.sleep(wait)
                        continue

                    response.raise_for_status()
                    payload = response.json()

                    # Log raw response for debugging (truncated)
                    logger.debug(
                        "GraphQL raw response (first 500 chars): %s",
                        str(payload)[:500],
                    )

                    if "errors" in payload:
                        msgs = [
                            e.get("message", "Unknown") for e in payload["errors"]
                        ]
                        raise ValueError(f"GraphQL errors: {'; '.join(msgs)}")

                    return payload["data"]

                except (httpx.ConnectError, httpx.ReadTimeout) as exc:
                    last_exc = exc
                    logger.warning(
                        "GraphQL network error attempt %d/%d: %s",
                        attempt, self._MAX_GRAPHQL_RETRIES, exc,
                    )
                    await asyncio.sleep(backoff)
                    backoff *= 2

        raise last_exc or RuntimeError("GraphQL query failed after retries")

    # ===================================================================
    # Canonical Contribution Fetcher (Task 2 + Task 3)
    # ===================================================================

    @staticmethod
    def _year_boundaries(year: int) -> Tuple[str, str]:
        """Return strict ISO 8601 UTC boundaries for a calendar year.

        from = YYYY-01-01T00:00:00Z
        to   = YYYY-12-31T23:59:59Z   (or current UTC time if year is current)
        """
        start = datetime(year, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        if year == now.year:
            end = now
        else:
            end = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        return (
            start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            end.strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

    async def fetch_contribution_data(
        self,
        client: httpx.AsyncClient,
        username: str,
    ) -> Optional[Dict[str, Any]]:
        """
        Canonical contribution fetcher.

        Retrieves:
        - Last 4 full calendar years
        - Current partial year
        -> 5 aliased ``contributionsCollection`` blocks in one GraphQL call.

        All date boundaries use strict calendar-year UTC (Task 3).
        """
        cache_key = f"contributions_v2:{username}"
        cached = _graphql_cache.get(cache_key)
        if cached is not None:
            return cached

        if not settings.GITHUB_TOKEN:
            logger.warning(
                "No GITHUB_TOKEN – skipping GraphQL contribution fetch"
            )
            return None

        now = datetime.now(timezone.utc)
        current_year = now.year

        # Current partial year + 4 prior full years
        years = list(range(current_year, current_year - 5, -1))

        aliases: List[str] = []
        variables: Dict[str, Any] = {"username": username}
        var_defs = ["$username: String!"]

        for yr in years:
            from_val, to_val = self._year_boundaries(yr)
            from_var = f"from_{yr}"
            to_var = f"to_{yr}"
            var_defs.append(f"${from_var}: DateTime!")
            var_defs.append(f"${to_var}: DateTime!")
            variables[from_var] = from_val
            variables[to_var] = to_val
            aliases.append(
                f"y{yr}: contributionsCollection("
                f"from: ${from_var}, to: ${to_var}"
                ") { ...ContribFields }"
            )

        query = (
            f"query({', '.join(var_defs)}) {{\n"
            f"  user(login: $username) {{\n"
            f"    createdAt\n"
            f"    {'    '.join(aliases)}\n"
            f"  }}\n"
            f"}}\n"
            f"{self._CONTRIBUTION_FRAGMENT}"
        )

        logger.debug(
            "GraphQL contribution query variables: %s", variables
        )

        try:
            data = await self._graphql_query(client, query, variables)
            user_data = data.get("user")
            if not user_data:
                logger.warning(
                    "GraphQL returned null user for %s", username
                )
                return None
            _graphql_cache.set(cache_key, user_data)
            return user_data
        except Exception as exc:
            logger.warning(
                "GraphQL contribution fetch failed for %s: %s",
                username, exc,
            )
            return None

    # ===================================================================
    # Parsing + Cross-Verification + Normalization (Tasks 4-6, 9)
    # ===================================================================

    @staticmethod
    def parse_contributions(
        raw_data: Optional[Dict[str, Any]],
    ) -> Optional[ContributionData]:
        """
        Transform raw GraphQL user payload into a fully validated
        ``ContributionData`` model.

        Pipeline:
        1. Extract per-year data using ``y{YYYY}`` aliases
        2. Cross-verify totalCommitContributions vs calendar day sums
        3. Compute time-normalised rates for every year
        4. Compute activity overview (3-yr MA, momentum, volatility, trend)
        5. Run consistency validator
        """
        if not raw_data:
            return None

        now = datetime.now(timezone.utc)
        current_year = now.year

        years = list(range(current_year, current_year - 5, -1))

        yearly_metrics: List[YearlyMetrics] = []
        all_days: List[Tuple[str, int]] = []
        total_commits = 0
        total_issues = 0
        total_prs = 0
        total_reviews = 0
        total_repos = 0
        total_restricted = 0

        account_created_str = raw_data.get("createdAt", "")
        account_created_year: Optional[int] = None
        if account_created_str:
            try:
                account_created_year = datetime.fromisoformat(
                    account_created_str.replace("Z", "+00:00")
                ).year
            except ValueError:
                pass

        for yr in years:
            key = f"y{yr}"
            year_data = raw_data.get(key)

            if not year_data:
                # Year before account creation -> skip silently (Task 5)
                if account_created_year and yr < account_created_year:
                    continue
                # Otherwise record as explicit zero-contribution year
                ym = YearlyMetrics(
                    year=yr,
                    total=0,
                    is_partial=(yr == current_year),
                    is_reliable=True,
                )
                yearly_metrics.append(ym)
                continue

            # --- typed totals ---
            yr_commits = year_data.get("totalCommitContributions", 0)
            yr_issues = year_data.get("totalIssueContributions", 0)
            yr_prs = year_data.get("totalPullRequestContributions", 0)
            yr_reviews = year_data.get(
                "totalPullRequestReviewContributions", 0
            )
            yr_repos = year_data.get("totalRepositoryContributions", 0)
            yr_restricted = year_data.get(
                "restrictedContributionsCount", 0
            )

            total_commits += yr_commits
            total_issues += yr_issues
            total_prs += yr_prs
            total_reviews += yr_reviews
            total_repos += yr_repos
            total_restricted += yr_restricted

            # --- daily calendar ---
            calendar = year_data.get("contributionCalendar", {})
            yr_days: List[Tuple[str, int]] = []
            for week in calendar.get("weeks", []):
                for day in week.get("contributionDays", []):
                    ds = day.get("date", "")
                    cnt = day.get("contributionCount", 0)
                    if ds:
                        yr_days.append((ds, cnt))
                        all_days.append((ds, cnt))

            calendar_sum = sum(c for _, c in yr_days)
            active_day_count = sum(1 for _, c in yr_days if c > 0)
            reported_total = calendar.get(
                "totalContributions", calendar_sum
            )

            # --- Cross-verification (Task 4) ---
            is_reliable = True
            effective_total = reported_total
            if reported_total > 0:
                mismatch_pct = (
                    abs(calendar_sum - reported_total) / reported_total * 100
                )
                if mismatch_pct > 2:
                    logger.warning(
                        "Year %d cross-verification mismatch: "
                        "calendar_sum=%d, reported=%d (%.1f%%) "
                        "– using calendar data",
                        yr, calendar_sum, reported_total, mismatch_pct,
                    )
                    is_reliable = False
                    effective_total = calendar_sum
            else:
                effective_total = calendar_sum

            # --- Normalised rates (Task 6) ---
            is_partial = yr == current_year
            if is_partial:
                day_of_year = now.timetuple().tm_yday
                elapsed_months = max(day_of_year / 30.44, 1)
                elapsed_weeks = max(day_of_year / 7.0, 1)
            else:
                is_leap = yr % 4 == 0 and (yr % 100 != 0 or yr % 400 == 0)
                total_days_in_year = 366 if is_leap else 365
                elapsed_months = 12.0
                elapsed_weeks = total_days_in_year / 7.0

            per_month = round(effective_total / elapsed_months, 2)
            per_week = round(effective_total / elapsed_weeks, 2)
            active_day_rate = (
                round(effective_total / active_day_count, 2)
                if active_day_count > 0
                else 0.0
            )

            ym = YearlyMetrics(
                year=yr,
                total=effective_total,
                per_month=per_month,
                per_week=per_week,
                active_days=active_day_count,
                active_day_rate=active_day_rate,
                is_partial=is_partial,
                is_reliable=is_reliable,
                calendar_sum=calendar_sum,
                reported_commits=yr_commits,
            )
            yearly_metrics.append(ym)

        # Sort ascending by year
        yearly_metrics.sort(key=lambda m: m.year)

        # --- Aggregate totals ---
        all_days.sort(key=lambda x: x[0])
        total_contributions = sum(m.total for m in yearly_metrics)
        current_year_contribs = next(
            (m.total for m in yearly_metrics if m.year == current_year), 0
        )

        one_year_ago_str = (now - timedelta(days=365)).strftime("%Y-%m-%d")
        last_12_months = sum(c for d, c in all_days if d >= one_year_ago_str)
        total_active_days = sum(1 for _, c in all_days if c > 0)

        weeks_52_ago = (now - timedelta(weeks=52)).strftime("%Y-%m-%d")
        recent_total = sum(c for d, c in all_days if d >= weeks_52_ago)
        weekly_average = (
            round(recent_total / 52.0, 2) if all_days else 0.0
        )

        longest_streak, current_streak = (
            GitHubService._compute_streaks(all_days)
        )

        # --- YoY growth on per_week basis (rate, not raw volume) ---
        full_years = [
            m for m in yearly_metrics if not m.is_partial and m.total > 0
        ]
        growth_rate = 0.0
        is_trending_up = False
        if len(full_years) >= 2:
            prev = full_years[-2].per_week
            curr = full_years[-1].per_week
            if prev > 0:
                growth_rate = round(((curr - prev) / prev) * 100, 1)
                is_trending_up = growth_rate > 0

        # --- Activity overview (Task 7) ---
        activity_overview = GitHubService._calculate_activity_overview(
            yearly_metrics
        )

        # --- Validation (Task 9) ---
        validation = GitHubService._validate_contribution_data(
            yearly_metrics, account_created_year
        )

        return ContributionData(
            yearly_metrics=yearly_metrics,
            total_contributions=total_contributions,
            current_year_contributions=current_year_contribs,
            last_12_months_contributions=last_12_months,
            weekly_average=weekly_average,
            longest_streak=longest_streak,
            current_streak=current_streak,
            active_days=total_active_days,
            contribution_breakdown={
                "commits": total_commits,
                "pull_requests": total_prs,
                "reviews": total_reviews,
                "issues": total_issues,
                "repositories": total_repos,
                "restricted": total_restricted,
            },
            growth_rate=growth_rate,
            is_trending_up=is_trending_up,
            activity_overview=activity_overview,
            validation=validation,
        )

    # ===================================================================
    # Activity Overview (Task 7)
    # ===================================================================

    @staticmethod
    def _calculate_activity_overview(
        yearly_metrics: List[YearlyMetrics],
    ) -> ActivityOverview:
        """
        - 3-year moving average of per_week (excludes current partial year)
        - Momentum index = latest full year per_week / 3-yr average
        - Volatility = coefficient of variation of per_week (full years)
        - Trend signal from growth rate + momentum
        """
        full_years = sorted(
            [m for m in yearly_metrics if not m.is_partial],
            key=lambda m: m.year,
        )

        if not full_years:
            return ActivityOverview(
                trend_signal="insufficient_data",
                trend_details="No full calendar years available for analysis",
            )

        recent_3 = full_years[-3:]
        avg_3yr = sum(m.per_week for m in recent_3) / len(recent_3)

        latest_pw = full_years[-1].per_week
        momentum = round(latest_pw / avg_3yr, 3) if avg_3yr > 0 else 0.0

        # Volatility (coefficient of variation)
        if len(full_years) >= 2:
            mean_pw = sum(m.per_week for m in full_years) / len(full_years)
            if mean_pw > 0:
                variance = sum(
                    (m.per_week - mean_pw) ** 2 for m in full_years
                ) / len(full_years)
                volatility = round(math.sqrt(variance) / mean_pw, 3)
            else:
                volatility = 0.0
        else:
            volatility = 0.0

        # Trend signal
        if len(full_years) >= 2:
            prev_pw = full_years[-2].per_week
            if prev_pw > 0:
                yoy_change = (latest_pw - prev_pw) / prev_pw
            else:
                yoy_change = 1.0 if latest_pw > 0 else 0.0
        else:
            yoy_change = 0.0

        if yoy_change > 0.25:
            signal = "strong_growth"
            details = (
                f"Commits/week rose from {full_years[-2].per_week:.1f} "
                f"to {latest_pw:.1f} (+{yoy_change * 100:.0f}%)"
                if len(full_years) >= 2
                else "Strong activity in the available year"
            )
        elif yoy_change > 0.05:
            signal = "growth"
            details = f"Modest upward trend ({yoy_change * 100:+.0f}% YoY)"
        elif yoy_change >= -0.05:
            signal = "stable"
            details = "Activity levels are holding steady"
        elif yoy_change >= -0.25:
            signal = "decline"
            details = f"Activity slowing ({yoy_change * 100:+.0f}% YoY)"
        else:
            signal = "strong_decline"
            details = (
                f"Commits/week dropped from {full_years[-2].per_week:.1f} "
                f"to {latest_pw:.1f} ({yoy_change * 100:+.0f}%)"
                if len(full_years) >= 2
                else "Significant drop in activity"
            )

        return ActivityOverview(
            moving_average_3yr=round(avg_3yr, 2),
            momentum_index=momentum,
            volatility_score=volatility,
            trend_signal=signal,
            trend_details=details,
        )

    # ===================================================================
    # Consistency Validator (Task 9)
    # ===================================================================

    @staticmethod
    def _validate_contribution_data(
        yearly_metrics: List[YearlyMetrics],
        account_created_year: Optional[int],
    ) -> ValidationResult:
        """
        Detect anomalies, flag incomplete years, mark unreliable segments.
        """
        anomalies: List[str] = []
        incomplete: List[int] = []
        unreliable: List[int] = []

        for m in yearly_metrics:
            if m.is_partial:
                incomplete.append(m.year)
            if not m.is_reliable:
                unreliable.append(m.year)
                anomalies.append(
                    f"Year {m.year}: calendar sum ({m.calendar_sum}) does "
                    f"not match reported total (mismatch > 2%). "
                    f"Using calendar data."
                )

            # Spike detection: >5x the average of neighbours
            if m.total > 0 and not m.is_partial:
                neighbours = [
                    n
                    for n in yearly_metrics
                    if n.year != m.year and not n.is_partial and n.total > 0
                ]
                if neighbours:
                    neighbour_avg = (
                        sum(n.total for n in neighbours) / len(neighbours)
                    )
                    if neighbour_avg > 0 and m.total / neighbour_avg > 5:
                        anomalies.append(
                            f"Year {m.year}: total ({m.total}) is >5x the "
                            f"average of other years ({neighbour_avg:.0f}) "
                            f"– possible bulk import or data anomaly"
                        )

        # New account edge case
        if account_created_year:
            now_year = datetime.now(timezone.utc).year
            if now_year - account_created_year < 1:
                anomalies.append(
                    "Account is less than 1 year old – "
                    "metrics based on limited data"
                )

        is_valid = len(unreliable) == 0 and len(anomalies) == 0
        return ValidationResult(
            is_valid=is_valid,
            anomalies=anomalies,
            incomplete_years=incomplete,
            unreliable_years=unreliable,
        )

    # ===================================================================
    # Backward-Compatibility Helpers
    # ===================================================================

    @staticmethod
    def build_commit_activity_from_contributions(
        contribution_data: ContributionData,
    ) -> CommitActivity:
        """
        Backward-compatible ``CommitActivity`` from the new
        ``ContributionData`` model so the existing frontend commit
        activity overview keeps working.
        """
        commits = contribution_data.contribution_breakdown.get("commits", 0)
        commit_frequency = round(
            contribution_data.last_12_months_contributions / 12.0, 2
        )
        year_count = len(
            [m for m in contribution_data.yearly_metrics if m.total > 0]
        )
        return CommitActivity(
            total_commits=commits,
            recent_commits=contribution_data.last_12_months_contributions,
            commit_frequency=commit_frequency,
            longest_streak=contribution_data.longest_streak,
            current_streak=contribution_data.current_streak,
            active_days=contribution_data.active_days,
            contribution_years=max(year_count, 1),
        )

    # ===================================================================
    # Streak Computation
    # ===================================================================

    @staticmethod
    def _compute_streaks(
        contribution_days: List[Tuple[str, int]],
    ) -> Tuple[int, int]:
        """Return ``(longest_streak, current_streak)`` from day pairs."""
        active_dates = sorted({d for d, c in contribution_days if c > 0})
        if not active_dates:
            return 0, 0

        longest = 1
        run = 1
        for i in range(1, len(active_dates)):
            prev = datetime.strptime(active_dates[i - 1], "%Y-%m-%d").date()
            curr = datetime.strptime(active_dates[i], "%Y-%m-%d").date()
            if (curr - prev).days == 1:
                run += 1
                longest = max(longest, run)
            else:
                run = 1

        today = datetime.now(timezone.utc).date()
        last_active = datetime.strptime(active_dates[-1], "%Y-%m-%d").date()
        if last_active not in (today, today - timedelta(days=1)):
            return longest, 0

        current_streak = 1
        for i in range(len(active_dates) - 1, 0, -1):
            prev_d = datetime.strptime(
                active_dates[i - 1], "%Y-%m-%d"
            ).date()
            curr_d = datetime.strptime(
                active_dates[i], "%Y-%m-%d"
            ).date()
            if (curr_d - prev_d).days == 1:
                current_streak += 1
            else:
                break

        return longest, current_streak


    async def aggregate_language_stats(
        self,
        client: httpx.AsyncClient,
        username: str,
        repos: List[Repository]
    ) -> LanguageStats:
        """
        Aggregate language statistics across repositories concurrently.
        
        Args:
            client: Shared httpx client
            username: GitHub username
            repos: List of repositories
            
        Returns:
            LanguageStats model with aggregated data
        """
        language_totals: Dict[str, int] = {}
        
        # Fetch languages concurrently
        tasks = [
            self.fetch_repo_languages(client, username, repo.name)
            for repo in repos
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception) or not isinstance(result, dict):
                continue
            for lang, bytes_count in result.items():
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
    
    async def count_readmes(self, client: httpx.AsyncClient, username: str, repos: List[Repository]) -> int:
        """Count how many repos have READMEs, concurrently."""
        tasks = [
            self.fetch_repo_readme(client, username, repo.name)
            for repo in repos
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return sum(1 for r in results if r is True)
