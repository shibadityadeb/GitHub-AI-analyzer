"""
AI Feedback Generator using OpenAI or OpenRouter.

Generates recruiter-style feedback and actionable improvement roadmap.
"""

import json
from typing import List, Optional
import httpx

from app.models.schemas import (
    GitHubUser,
    Repository,
    ScoreBreakdown,
    Strength,
    Weakness,
    RedFlag,
    AIFeedback,
    ImprovementAction,
    ProjectSuggestion
)
from app.core.config import settings


class FeedbackGenerator:
    """Service for generating AI-powered feedback and recommendations."""
    
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        self.openrouter_api_key = settings.OPENROUTER_API_KEY
        self.model = settings.AI_MODEL
        self.temperature = settings.AI_TEMPERATURE
        self.max_tokens = settings.AI_MAX_TOKENS
    
    async def generate_feedback(
        self,
        profile: GitHubUser,
        repos: List[Repository],
        score_breakdown: ScoreBreakdown,
        strengths: List[Strength],
        weaknesses: List[Weakness],
        red_flags: List[RedFlag]
    ) -> Optional[AIFeedback]:
        """
        Generate AI-powered feedback and recommendations.
        
        Args:
            profile: GitHub user profile
            repos: List of repositories
            score_breakdown: Calculated scores
            strengths: Detected strengths
            weaknesses: Detected weaknesses
            red_flags: Detected red flags
            
        Returns:
            AIFeedback with summary, roadmap, and project suggestions
        """
        
        # If no API key configured, return None
        if not self.openai_api_key and not self.openrouter_api_key:
            return None
        
        try:
            # Build the prompt for the AI
            prompt = self._build_prompt(
                profile, repos, score_breakdown, strengths, weaknesses, red_flags
            )
            
            # Call the appropriate AI service
            if self.openai_api_key:
                response_text = await self._call_openai(prompt)
            else:
                response_text = await self._call_openrouter(prompt)
            
            # Parse the response
            ai_feedback = self._parse_response(response_text)
            
            return ai_feedback
            
        except Exception as e:
            # If AI generation fails, return None rather than breaking the entire response
            print(f"AI feedback generation failed: {str(e)}")
            return None
    
    def _build_prompt(
        self,
        profile: GitHubUser,
        repos: List[Repository],
        score_breakdown: ScoreBreakdown,
        strengths: List[Strength],
        weaknesses: List[Weakness],
        red_flags: List[RedFlag]
    ) -> str:
        """Build the prompt for AI feedback generation."""
        
        # Summarize key metrics
        total_stars = sum(repo.stargazers_count for repo in repos)
        total_forks = sum(repo.forks_count for repo in repos)
        primary_language = score_breakdown.project_quality_and_originality.details.get(
            "language_diversity", {}
        ).get("primary_language", "Not specified")
        
        prompt = f"""You are a senior technical recruiter reviewing GitHub portfolios for entry-level software engineering positions.

CANDIDATE PROFILE:
- Username: {profile.login}
- Name: {profile.name or "Not provided"}
- Bio: {profile.bio or "Not provided"}
- Location: {profile.location or "Not provided"}
- Hireable: {"Yes" if profile.hireable else "No"}
- Public Repos: {profile.public_repos}
- Followers: {profile.followers} | Following: {profile.following}
- Total Stars: {total_stars} | Total Forks: {total_forks}
- Primary Language: {primary_language}

GITHUB PORTFOLIO SCORE: {score_breakdown.final_score}/100 ({score_breakdown.percentile_rank})

SCORE BREAKDOWN:
- Activity & Consistency: {score_breakdown.activity_and_consistency.score}/100
- Documentation & Readability: {score_breakdown.documentation_and_readability.score}/100
- Project Quality & Originality: {score_breakdown.project_quality_and_originality.score}/100
- Professionalism & Branding: {score_breakdown.professionalism_and_branding.score}/100
- Impact & Collaboration: {score_breakdown.impact_and_collaboration.score}/100

IDENTIFIED STRENGTHS ({len(strengths)}):
{self._format_items(strengths, 'title', 'description')}

IDENTIFIED WEAKNESSES ({len(weaknesses)}):
{self._format_items(weaknesses, 'title', 'description')}

RED FLAGS ({len(red_flags)}):
{self._format_items(red_flags, 'title', 'description')}

YOUR TASK:
Generate a comprehensive recruiter report in JSON format with the following structure:

{{
    "summary": "A 2-3 sentence overall assessment of this candidate's GitHub profile from a recruiter's perspective",
    "key_takeaways": [
        "3-5 bullet points highlighting the most important insights (both positive and negative)",
        "Be specific and actionable",
        "Focus on what matters most to entry-level hiring"
    ],
    "roadmap_30_days": [
        {{
            "week": 1,
            "priority": "High|Medium|Low",
            "action": "Specific actionable task for the candidate",
            "expected_impact": "How this improves their profile",
            "time_estimate": "Estimated hours/days"
        }},
        // Include 6-8 actions spread across 4 weeks
    ],
    "project_suggestions": [
        {{
            "title": "Project Name",
            "description": "What to build and why",
            "tech_stack": ["Technology 1", "Technology 2", ...],
            "difficulty": "Beginner|Intermediate|Advanced",
            "why_it_matters": "Why this project strengthens the portfolio",
            "estimated_time": "Time to complete"
        }},
        // Include 3-4 project suggestions
    ],
    "recruiter_perspective": "A frank, honest paragraph from a recruiter's POV: Would you interview this candidate? What concerns you? What excites you? Be brutally honest but constructive."
}}

GUIDELINES:
- Be honest but constructive
- Focus on actionable advice
- Prioritize high-impact improvements
- Consider the entry-level context
- Be specific with project suggestions
- Make the roadmap realistic for 30 days
- Output ONLY valid JSON, no markdown formatting

Generate the JSON report:"""

        return prompt
    
    def _format_items(self, items: List, title_key: str, desc_key: str) -> str:
        """Format a list of items for the prompt."""
        if not items:
            return "None"
        
        formatted = []
        for item in items[:5]:  # Limit to top 5 to keep prompt concise
            title = getattr(item, title_key, "")
            desc = getattr(item, desc_key, "")
            formatted.append(f"- {title}: {desc}")
        
        if len(items) > 5:
            formatted.append(f"... and {len(items) - 5} more")
        
        return "\n".join(formatted)
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior technical recruiter specializing in entry-level software engineering hiring. You provide honest, actionable feedback."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    async def _call_openrouter(self, prompt: str) -> str:
        """Call OpenRouter API."""
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/yourusername/github-analyzer",  # Update with your repo
            "X-Title": "GitHub Portfolio Analyzer"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior technical recruiter specializing in entry-level software engineering hiring. You provide honest, actionable feedback."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    def _parse_response(self, response_text: str) -> AIFeedback:
        """Parse AI response into AIFeedback model."""
        
        # Clean up response (remove markdown code blocks if present)
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            # If parsing fails, create a fallback response
            return AIFeedback(
                summary="Unable to generate detailed AI feedback at this time.",
                key_takeaways=["AI feedback generation encountered an error"],
                roadmap_30_days=[],
                project_suggestions=[],
                recruiter_perspective="AI feedback temporarily unavailable."
            )
        
        # Convert roadmap items to ImprovementAction models
        roadmap = [
            ImprovementAction(
                week=item.get("week", 1),
                priority=item.get("priority", "Medium"),
                action=item.get("action", ""),
                expected_impact=item.get("expected_impact", ""),
                time_estimate=item.get("time_estimate", "")
            )
            for item in data.get("roadmap_30_days", [])
        ]
        
        # Convert project suggestions to ProjectSuggestion models
        projects = [
            ProjectSuggestion(
                title=item.get("title", ""),
                description=item.get("description", ""),
                tech_stack=item.get("tech_stack", []),
                difficulty=item.get("difficulty", "Intermediate"),
                why_it_matters=item.get("why_it_matters", ""),
                estimated_time=item.get("estimated_time", "")
            )
            for item in data.get("project_suggestions", [])
        ]
        
        return AIFeedback(
            summary=data.get("summary", ""),
            key_takeaways=data.get("key_takeaways", []),
            roadmap_30_days=roadmap,
            project_suggestions=projects,
            recruiter_perspective=data.get("recruiter_perspective", "")
        )
