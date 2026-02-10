"""
Analyzer Service for detecting strengths, weaknesses, and red flags.

This service applies rule-based pattern matching to identify
recruiter-relevant signals in a GitHub portfolio.
"""

from typing import List
from datetime import datetime, timedelta, timezone

from app.models.schemas import (
    GitHubUser,
    Repository,
    CommitActivity,
    LanguageStats,
    ScoreBreakdown,
    Strength,
    Weakness,
    RedFlag
)


class AnalyzerService:
    """Service for analyzing GitHub portfolios and detecting insights."""
    
    def detect_strengths(
        self,
        profile: GitHubUser,
        repos: List[Repository],
        commit_activity: CommitActivity,
        language_stats: LanguageStats,
        score_breakdown: ScoreBreakdown
    ) -> List[Strength]:
        """
        Detect strengths in the GitHub portfolio.
        
        Strengths are positive signals that recruiters look for.
        """
        strengths = []
        
        # ===================================================================
        # ACTIVITY STRENGTHS
        # ===================================================================
        
        # High commit frequency
        if commit_activity.commit_frequency >= 15:
            strengths.append(Strength(
                category="Activity",
                title="Consistent Code Contributor",
                description=f"Maintains an impressive commit frequency of {commit_activity.commit_frequency:.1f} commits per month",
                evidence=[
                    f"{commit_activity.total_commits} total commits",
                    f"{commit_activity.recent_commits} commits in the last year",
                    f"{commit_activity.active_days} active days"
                ],
                impact="High"
            ))
        
        # Long streak
        if commit_activity.longest_streak >= 30:
            strengths.append(Strength(
                category="Activity",
                title="Dedicated Developer",
                description=f"Achieved a {commit_activity.longest_streak}-day coding streak, demonstrating commitment and discipline",
                evidence=[
                    f"Longest streak: {commit_activity.longest_streak} days",
                    f"Current streak: {commit_activity.current_streak} days"
                ],
                impact="High"
            ))
        
        # Recent activity
        if commit_activity.recent_commits >= 50:
            strengths.append(Strength(
                category="Activity",
                title="Currently Active Developer",
                description="Shows strong recent activity with consistent contributions in the past year",
                evidence=[
                    f"{commit_activity.recent_commits} commits in last 365 days",
                    "Demonstrates ongoing learning and development"
                ],
                impact="High"
            ))
        
        # ===================================================================
        # DOCUMENTATION STRENGTHS
        # ===================================================================
        
        readme_ratio = 0
        if repos:
            readme_count = score_breakdown.documentation_and_readability.details.get(
                "readme_coverage", {}
            ).get("repos_with_readme", 0)
            readme_ratio = readme_count / len(repos)
        
        if readme_ratio >= 0.8:
            strengths.append(Strength(
                category="Documentation",
                title="Strong Documentation Culture",
                description=f"Maintains READMEs in {readme_ratio*100:.0f}% of repositories",
                evidence=[
                    "Understands importance of project documentation",
                    "Makes projects accessible to collaborators",
                    "Professional presentation of work"
                ],
                impact="High"
            ))
        
        # Good descriptions
        repos_with_description = sum(1 for repo in repos if repo.description)
        if repos and repos_with_description / len(repos) >= 0.7:
            strengths.append(Strength(
                category="Documentation",
                title="Clear Communicator",
                description="Provides clear descriptions for projects, showing good communication skills",
                evidence=[
                    f"{repos_with_description} out of {len(repos)} repos have descriptions"
                ],
                impact="Medium"
            ))
        
        # ===================================================================
        # QUALITY STRENGTHS
        # ===================================================================
        
        # High engagement (stars + forks)
        total_stars = sum(repo.stargazers_count for repo in repos)
        total_forks = sum(repo.forks_count for repo in repos)
        
        if total_stars >= 20:
            strengths.append(Strength(
                category="Quality",
                title="Community-Validated Projects",
                description=f"Projects have earned {total_stars} stars from the community",
                evidence=[
                    f"{total_stars} total stars",
                    f"{total_forks} total forks",
                    "Work recognized by other developers"
                ],
                impact="High"
            ))
        
        # Language diversity
        if language_stats.language_diversity >= 5:
            strengths.append(Strength(
                category="Quality",
                title="Polyglot Developer",
                description=f"Proficient in {language_stats.language_diversity} programming languages",
                evidence=[
                    f"Primary language: {language_stats.primary_language or 'Not specified'}",
                    f"Total languages: {language_stats.language_diversity}",
                    "Demonstrates adaptability and breadth of knowledge"
                ],
                impact="High"
            ))
        
        # Recent project updates
        six_months_ago = datetime.now(timezone.utc) - timedelta(days=180)
        recent_updates = sum(
            1 for repo in repos
            if datetime.fromisoformat(repo.updated_at.replace("Z", "+00:00")) >= six_months_ago
        )
        if repos and recent_updates / len(repos) >= 0.5:
            strengths.append(Strength(
                category="Quality",
                title="Active Project Maintenance",
                description="Regularly updates and maintains projects",
                evidence=[
                    f"{recent_updates} repos updated in last 6 months",
                    "Shows ongoing commitment to existing work"
                ],
                impact="Medium"
            ))
        
        # ===================================================================
        # PROFESSIONALISM STRENGTHS
        # ===================================================================
        
        # Complete profile
        completeness_score = score_breakdown.professionalism_and_branding.details.get(
            "profile_completeness", {}
        ).get("percentage", 0)
        
        if completeness_score >= 80:
            strengths.append(Strength(
                category="Professionalism",
                title="Polished Professional Profile",
                description=f"Profile is {completeness_score:.0f}% complete with comprehensive information",
                evidence=[
                    "Name, bio, and location provided",
                    "Contact information available",
                    "Shows attention to personal branding"
                ],
                impact="Medium"
            ))
        
        # Hireable
        if profile.hireable:
            strengths.append(Strength(
                category="Professionalism",
                title="Actively Seeking Opportunities",
                description="Marked as available for hire, showing proactive job search approach",
                evidence=["Hireable flag enabled"],
                impact="Medium"
            ))
        
        # Has website/blog
        if profile.blog:
            strengths.append(Strength(
                category="Professionalism",
                title="Online Presence Beyond GitHub",
                description="Maintains a personal website or blog",
                evidence=[
                    f"Website: {profile.blog}",
                    "Demonstrates professional branding"
                ],
                impact="Medium"
            ))
        
        # ===================================================================
        # IMPACT STRENGTHS
        # ===================================================================
        
        # High followers
        if profile.followers >= 50:
            strengths.append(Strength(
                category="Impact",
                title="Recognized in Developer Community",
                description=f"Has {profile.followers} followers, indicating community recognition",
                evidence=[
                    f"{profile.followers} followers",
                    "Work visible to broader developer community"
                ],
                impact="High"
            ))
        
        # Good follower ratio
        if profile.followers > 0 and profile.following > 0:
            ratio = profile.followers / profile.following
            if ratio >= 1.5:
                strengths.append(Strength(
                    category="Impact",
                    title="Influential Developer",
                    description="Strong follower-to-following ratio indicates influence",
                    evidence=[
                        f"{profile.followers} followers vs {profile.following} following",
                        f"Ratio: {ratio:.1f}:1"
                    ],
                    impact="Medium"
                ))
        
        # Projects with forks
        if total_forks >= 10:
            strengths.append(Strength(
                category="Impact",
                title="Collaborative Codebase",
                description=f"Projects have been forked {total_forks} times by other developers",
                evidence=[
                    f"{total_forks} total forks",
                    "Code is being used and extended by others"
                ],
                impact="High"
            ))
        
        return strengths
    
    def detect_weaknesses(
        self,
        profile: GitHubUser,
        repos: List[Repository],
        commit_activity: CommitActivity,
        language_stats: LanguageStats,
        readme_count: int,
        score_breakdown: ScoreBreakdown
    ) -> List[Weakness]:
        """
        Detect weaknesses in the GitHub portfolio.
        
        Weaknesses are areas that need improvement from a recruiter's perspective.
        """
        weaknesses = []
        
        # ===================================================================
        # ACTIVITY WEAKNESSES
        # ===================================================================
        
        # Low recent activity
        if commit_activity.recent_commits < 20:
            weaknesses.append(Weakness(
                category="Activity",
                title="Limited Recent Activity",
                description=f"Only {commit_activity.recent_commits} commits in the last year",
                severity="Moderate",
                suggestion="Aim for consistent contributions with at least 3-5 commits per week to show active development"
            ))
        
        # No current streak
        if commit_activity.current_streak == 0:
            weaknesses.append(Weakness(
                category="Activity",
                title="Broken Contribution Streak",
                description="No recent commits in the last 2 days",
                severity="Minor",
                suggestion="Build a habit of daily or weekly contributions to maintain momentum and visibility"
            ))
        
        # Low commit frequency
        if commit_activity.commit_frequency < 5:
            weaknesses.append(Weakness(
                category="Activity",
                title="Inconsistent Contribution Pattern",
                description=f"Low commit frequency of {commit_activity.commit_frequency:.1f} commits/month",
                severity="Moderate",
                suggestion="Establish a regular coding schedule and commit more frequently, even for small changes"
            ))
        
        # ===================================================================
        # DOCUMENTATION WEAKNESSES
        # ===================================================================
        
        # Missing READMEs
        if repos:
            readme_ratio = readme_count / len(repos)
            if readme_ratio < 0.5:
                weaknesses.append(Weakness(
                    category="Documentation",
                    title="Poor README Coverage",
                    description=f"Only {readme_ratio*100:.0f}% of repositories have README files",
                    severity="Moderate",
                    suggestion="Add comprehensive READMEs with project description, setup instructions, and usage examples"
                ))
        
        # Missing descriptions
        repos_with_description = sum(1 for repo in repos if repo.description)
        if repos and repos_with_description / len(repos) < 0.5:
            weaknesses.append(Weakness(
                category="Documentation",
                title="Missing Project Descriptions",
                description=f"Only {repos_with_description}/{len(repos)} repositories have descriptions",
                severity="Minor",
                suggestion="Add clear, concise descriptions to all repositories explaining what they do and why they matter"
            ))
        
        # ===================================================================
        # QUALITY WEAKNESSES
        # ===================================================================
        
        # Low engagement
        total_stars = sum(repo.stargazers_count for repo in repos)
        if total_stars < 5 and len(repos) > 3:
            weaknesses.append(Weakness(
                category="Quality",
                title="Low Project Visibility",
                description=f"Projects have earned only {total_stars} stars",
                severity="Minor",
                suggestion="Share projects on social media, Reddit, or dev.to to increase visibility and gather feedback"
            ))
        
        # Limited language diversity
        if language_stats.language_diversity < 3:
            weaknesses.append(Weakness(
                category="Quality",
                title="Limited Technology Stack",
                description=f"Only {language_stats.language_diversity} programming languages used",
                severity="Moderate",
                suggestion="Learn and build projects in diverse technologies to show versatility (aim for 4-5 languages)"
            ))
        
        # Old projects
        six_months_ago = datetime.now(timezone.utc) - timedelta(days=180)
        recent_updates = sum(
            1 for repo in repos
            if datetime.fromisoformat(repo.updated_at.replace("Z", "+00:00")) >= six_months_ago
        )
        if repos and recent_updates / len(repos) < 0.3:
            weaknesses.append(Weakness(
                category="Quality",
                title="Stale Project Portfolio",
                description="Most repositories haven't been updated recently",
                severity="Moderate",
                suggestion="Regularly maintain existing projects, add features, fix bugs, or archive outdated ones"
            ))
        
        # ===================================================================
        # PROFESSIONALISM WEAKNESSES
        # ===================================================================
        
        # Incomplete profile
        completeness = score_breakdown.professionalism_and_branding.details.get(
            "profile_completeness", {}
        ).get("percentage", 0)
        
        if completeness < 60:
            missing_fields = []
            if not profile.name:
                missing_fields.append("name")
            if not profile.bio:
                missing_fields.append("bio")
            if not profile.location:
                missing_fields.append("location")
            if not profile.blog:
                missing_fields.append("website")
            
            weaknesses.append(Weakness(
                category="Professionalism",
                title="Incomplete Profile",
                description=f"Profile is only {completeness:.0f}% complete",
                severity="Moderate",
                suggestion=f"Add missing information: {', '.join(missing_fields)} to present a complete professional image"
            ))
        
        # No bio
        if not profile.bio or len(profile.bio) < 20:
            weaknesses.append(Weakness(
                category="Professionalism",
                title="Missing or Weak Bio",
                description="Bio is missing or too brief",
                severity="Minor",
                suggestion="Write a 2-3 sentence bio highlighting your skills, interests, and what you're working on"
            ))
        
        # Not marked hireable
        if not profile.hireable:
            weaknesses.append(Weakness(
                category="Professionalism",
                title="Not Marked as Hireable",
                description="Profile not flagged as open to opportunities",
                severity="Minor",
                suggestion="Enable the 'Available for hire' checkbox if you're seeking opportunities"
            ))
        
        # ===================================================================
        # IMPACT WEAKNESSES
        # ===================================================================
        
        # Low followers
        if profile.followers < 10:
            weaknesses.append(Weakness(
                category="Impact",
                title="Limited Network",
                description=f"Only {profile.followers} followers",
                severity="Minor",
                suggestion="Engage with the developer community, contribute to open source, and share your work"
            ))
        
        # No forks
        total_forks = sum(repo.forks_count for repo in repos)
        if total_forks == 0 and len(repos) > 3:
            weaknesses.append(Weakness(
                category="Impact",
                title="No Project Adoption",
                description="Projects haven't been forked by others",
                severity="Minor",
                suggestion="Build useful tools or libraries that others might want to use and contribute to"
            ))
        
        return weaknesses
    
    def detect_red_flags(
        self,
        profile: GitHubUser,
        repos: List[Repository],
        commit_activity: CommitActivity,
        readme_count: int
    ) -> List[RedFlag]:
        """
        Detect red flags that might concern recruiters.
        
        Red flags are warning signals that may negatively impact hiring decisions.
        """
        red_flags = []
        
        # ===================================================================
        # CRITICAL RED FLAGS
        # ===================================================================
        
        # Account completely inactive
        one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)
        last_updated = max(
            (datetime.fromisoformat(repo.updated_at.replace("Z", "+00:00")) for repo in repos),
            default=datetime.min
        )
        
        if last_updated < one_year_ago:
            red_flags.append(RedFlag(
                flag_type="Critical",
                title="Abandoned Account",
                description="No activity in over a year",
                recruiter_perspective="Indicates lack of current technical engagement or interest in programming",
                how_to_fix="Start contributing regularly, even with small projects or open source contributions"
            ))
        
        # Almost no commits
        if commit_activity.total_commits < 20 and len(repos) > 5:
            red_flags.append(RedFlag(
                flag_type="Critical",
                title="Superficial Repository Activity",
                description="Many repositories but very few commits",
                recruiter_perspective="Suggests repositories may be forks, templates, or incomplete projects rather than original work",
                how_to_fix="Focus on completing projects with meaningful commit history showing development process"
            ))
        
        # No original work (all tutorials)
        tutorial_keywords = ["tutorial", "practice", "learning", "course", "homework", "assignment", "test", "demo"]
        tutorial_repos = sum(
            1 for repo in repos
            if any(keyword in repo.name.lower() for keyword in tutorial_keywords)
            or any(keyword in (repo.description or "").lower() for keyword in tutorial_keywords)
        )
        
        if repos and tutorial_repos / len(repos) > 0.7:
            red_flags.append(RedFlag(
                flag_type="Critical",
                title="No Original Projects",
                description=f"{tutorial_repos}/{len(repos)} repositories appear to be tutorials or coursework",
                recruiter_perspective="Lack of original work raises questions about ability to build from scratch",
                how_to_fix="Build 2-3 original projects that solve real problems or showcase unique ideas"
            ))
        
        # ===================================================================
        # MODERATE RED FLAGS
        # ===================================================================
        
        # Very few READMEs
        if repos and readme_count / len(repos) < 0.2:
            red_flags.append(RedFlag(
                flag_type="Moderate",
                title="Poor Documentation Practices",
                description=f"Only {readme_count}/{len(repos)} repositories have READMEs",
                recruiter_perspective="Suggests poor communication skills and lack of professional development practices",
                how_to_fix="Add comprehensive READMEs to all public projects explaining purpose, setup, and usage"
            ))
        
        # Empty profile
        if not profile.name and not profile.bio and not profile.location:
            red_flags.append(RedFlag(
                flag_type="Moderate",
                title="Blank Profile",
                description="No name, bio, or location provided",
                recruiter_perspective="Appears unprofessional and raises questions about seriousness of job search",
                how_to_fix="Fill out basic profile information to make a professional first impression"
            ))
        
        # All repos private or very few public
        if profile.public_repos < 3:
            red_flags.append(RedFlag(
                flag_type="Moderate",
                title="Minimal Public Work",
                description=f"Only {profile.public_repos} public repositories",
                recruiter_perspective="Difficult to assess technical skills without visible code samples",
                how_to_fix="Make 3-5 of your best projects public to showcase your capabilities"
            ))
        
        # Account very new with many repos
        created_date = datetime.fromisoformat(profile.created_at.replace("Z", "+00:00"))
        account_age_days = (datetime.now(timezone.utc) - created_date).days
        
        if account_age_days < 90 and len(repos) > 20:
            red_flags.append(RedFlag(
                flag_type="Moderate",
                title="Suspicious Repository Pattern",
                description=f"Account created {account_age_days} days ago with {len(repos)} repositories",
                recruiter_perspective="May indicate bulk uploading of old projects or inflated repository count",
                how_to_fix="Focus on quality over quantity; maintain steady, authentic contribution pattern"
            ))
        
        # ===================================================================
        # MINOR RED FLAGS
        # ===================================================================
        
        # No activity in last 3 months
        three_months_ago = datetime.now(timezone.utc) - timedelta(days=90)
        if commit_activity.recent_commits > 0 and last_updated < three_months_ago:
            red_flags.append(RedFlag(
                flag_type="Minor",
                title="Recent Inactivity",
                description="No commits in the last 3 months",
                recruiter_perspective="May signal loss of interest or current engagement in private projects",
                how_to_fix="Make at least weekly commits to maintain an active profile"
            ))
        
        # Very low engagement despite many repos
        total_stars = sum(repo.stargazers_count for repo in repos)
        if len(repos) > 10 and total_stars == 0:
            red_flags.append(RedFlag(
                flag_type="Minor",
                title="No Community Engagement",
                description=f"{len(repos)} repositories with zero stars",
                recruiter_perspective="Projects may be low quality or not shared with community",
                how_to_fix="Share projects, engage with other developers, and build projects others find useful"
            ))
        
        return red_flags
