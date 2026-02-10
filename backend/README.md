# 🎯 GitHub Portfolio Analyzer - Backend

Production-ready FastAPI backend for analyzing GitHub profiles from a recruiter's perspective.

## 🏗️ Architecture

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configuration & environment variables
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic data models
│   └── services/
│       ├── __init__.py
│       ├── github_service.py   # GitHub API integration
│       ├── scoring_engine.py   # Portfolio scoring logic
│       ├── analyzer.py         # Insights detection
│       └── feedback_generator.py  # AI feedback generation
├── requirements.txt
├── .env.example
└── README.md
```

## ✨ Features

### 1. **GitHub Data Collection**
- Fetch user profile, repositories, commits, and metadata
- Aggregate language statistics
- Check README presence
- Handle rate limiting and errors gracefully

### 2. **Multi-Dimensional Scoring (0-100)**
- **Activity & Consistency (25%)**: Commit frequency, streaks, recency
- **Documentation & Readability (20%)**: READMEs, descriptions, wikis
- **Project Quality & Originality (25%)**: Stars, forks, language diversity
- **Professionalism & Branding (15%)**: Profile completeness, bio, links
- **Impact & Collaboration (15%)**: Followers, community engagement

### 3. **Recruiter Signal Detection**
- **Strengths**: Positive signals that impress recruiters
- **Weaknesses**: Areas needing improvement with actionable suggestions
- **Red Flags**: Warning signals that concern recruiters

### 4. **AI-Powered Feedback** (Optional)
- Recruiter-style summary and assessment
- 30-day improvement roadmap
- Personalized project suggestions
- Brutally honest recruiter perspective

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or poetry

### Installation

1. **Clone and navigate to backend:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the server:**
```bash
uvicorn app.main:app --reload --port 8000
```

Server will start at `http://localhost:8000`

## 🔑 Environment Variables

### Required
None! The app works without any API keys.

### Optional (Recommended)

**GitHub Token** - Increases rate limit from 60 to 5000 requests/hour
```bash
GITHUB_TOKEN=ghp_your_token_here
```
Get token at: https://github.com/settings/tokens (needs `public_repo` scope)

**AI Feedback** - Enables AI-powered insights using Anthropic Claude
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```
Get key at: https://console.anthropic.com/settings/keys

## 📡 API Endpoints

### `POST /api/analyze/{username}`
Analyze a GitHub profile and generate comprehensive report.

**Parameters:**
- `username` (path): GitHub username to analyze
- `include_ai_feedback` (query, optional): Generate AI feedback (default: true)

**Response:**
```json
{
  "username": "octocat",
  "analyzed_at": "2026-02-10T12:00:00Z",
  "score_breakdown": {
    "final_score": 78.5,
    "percentile_rank": "Top 15%",
    "activity_and_consistency": {...},
    "documentation_and_readability": {...},
    "project_quality_and_originality": {...},
    "professionalism_and_branding": {...},
    "impact_and_collaboration": {...}
  },
  "strengths": [...],
  "weaknesses": [...],
  "red_flags": [...],
  "ai_feedback": {...},
  "profile": {...},
  "language_stats": {...},
  "commit_activity": {...}
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/analyze/octocat?include_ai_feedback=true"
```

### `GET /api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-10T12:00:00Z",
  "github_api": {
    "configured": true,
    "base_url": "https://api.github.com"
  },
  "ai_service": {
    "anthropic_configured": false
  }
}
```

### `GET /`
Root endpoint with API information.

### `GET /docs`
Interactive API documentation (Swagger UI).

### `GET /redoc`
Alternative API documentation (ReDoc).

## 🧪 Testing

### Test the API
```bash
# Health check
curl http://localhost:8000/health

# Analyze a profile
curl http://localhost:8000/api/analyze/octocat

# Without AI feedback
curl "http://localhost:8000/api/analyze/octocat?include_ai_feedback=false"
```

### Run Tests (when implemented)
```bash
pytest tests/
```

## 🏭 Production Deployment

### Environment Variables for Production
```bash
# Add production frontend URLs
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Use production-grade API keys
GITHUB_TOKEN=ghp_production_token
ANTHROPIC_API_KEY=sk-ant-production-key
```

### Run with Gunicorn
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Configuration

### Scoring Weights
Adjust in `.env` (must sum to 100):
```bash
WEIGHT_ACTIVITY=25.0
WEIGHT_DOCUMENTATION=20.0
WEIGHT_QUALITY=25.0
WEIGHT_PROFESSIONALISM=15.0
WEIGHT_IMPACT=15.0
```

### Analysis Parameters
```bash
MIN_REPOS_FOR_ANALYSIS=1    # Minimum repos required
MAX_REPOS_TO_ANALYZE=50     # Maximum repos to analyze
RECENT_ACTIVITY_DAYS=365    # Days to consider for recent activity
```

## 📊 Scoring Logic

### Activity & Consistency (25%)
- Commit frequency: 15+ commits/month = excellent
- Recent commits: 100+ in last year = excellent
- Longest streak: 30+ days = excellent
- Account maturity: 2+ years = bonus

### Documentation & Readability (20%)
- README coverage: 80%+ repos = excellent
- Descriptions: 70%+ repos = good
- Wiki/Pages/Issues enabled = bonus

### Project Quality & Originality (25%)
- Engagement: 50+ stars+forks = excellent
- Language diversity: 5+ languages = excellent
- Project freshness: 50%+ updated in 6 months = good
- Originality: detecting tutorials vs original work

### Professionalism & Branding (15%)
- Profile completeness: name, bio, location, email, company
- Hireable flag enabled
- Personal website/blog
- Social media links

### Impact & Collaboration (15%)
- Followers: 50+ = excellent
- Forks: 20+ total = excellent
- Follower/following ratio > 0.5 = engaged
- Active collaboration indicators

## 🐛 Troubleshooting

### Rate Limit Errors
- Add `GITHUB_TOKEN` to `.env`
- Reduces rate from 60 to 5000 requests/hour

### AI Feedback Not Generating
- Check `ANTHROPIC_API_KEY` is set
- Verify API key is valid
- Check AI service status

### CORS Errors
- Add frontend URL to `ALLOWED_ORIGINS` in config.py
- Restart server after changes

## 📚 Tech Stack

- **Framework**: FastAPI 0.115.0
- **HTTP Client**: httpx 0.27.2
- **Validation**: Pydantic 2.9.2
- **AI**: Anthropic Claude 0.39.0 (optional)
- **Server**: Uvicorn 0.32.0

## 🤝 Contributing

1. Follow existing code structure
2. Maintain separation of concerns
3. Add docstrings to all functions
4. Use type hints
5. Test thoroughly before committing

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Related

- Frontend: `../frontend/`
- API Documentation: `http://localhost:8000/docs`

---

**Built for students and early-career developers** 🎓
