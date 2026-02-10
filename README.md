# 🎯 GitHub Portfolio Analyzer & Recruiter Scorecard

A production-ready web application that analyzes GitHub profiles from a recruiter's perspective, providing objective scores, actionable insights, and AI-powered recommendations for students and early-career developers.

![GitHub Analyzer](https://img.shields.io/badge/Status-Production%20Ready-success)
![Tech Stack](https://img.shields.io/badge/Stack-React%20%2B%20FastAPI-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Overview

This tool helps developers understand how recruiters view their GitHub profiles and provides concrete steps to improve their chances of landing interviews and job offers.

### Key Features

- 📊 **Portfolio Score (0-100)**: Multi-dimensional scoring across 5 key metrics
- 🎯 **Recruiter Insights**: Strengths, weaknesses, and red flags detection
- 🤖 **AI Feedback**: Personalized improvement roadmap and project suggestions
- 📈 **Visual Analytics**: Interactive charts and progress tracking
- 🚀 **Actionable Advice**: Specific, prioritized improvements

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│         React + Vite Frontend (Port 3000)        │
│  • Modern UI with Tailwind CSS                  │
│  • Interactive charts with Recharts             │
│  • Responsive, mobile-friendly design           │
└──────────────────┬──────────────────────────────┘
                   │ REST API
                   ▼
┌─────────────────────────────────────────────────┐
│       FastAPI Backend (Port 8000)               │
│  • GitHub API integration                       │
│  • Multi-dimensional scoring engine             │
│  • Pattern-based insight detection              │
│  • Optional AI feedback generation              │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   External APIs     │
         │  • GitHub REST API  │
         │  • Anthropic Claude │
         └─────────────────────┘
```

## 📊 Scoring System & Calculations

The final portfolio score (0–100) is a **weighted sum** of five independent component scores. Each component is scored 0–100 internally, then multiplied by its weight.

$$\text{Final Score} = \sum_{i=1}^{5} \frac{\text{Component}_i \times \text{Weight}_i}{100}$$

### Configurable Weights (default, must sum to 100)

| # | Dimension | Weight | What It Measures |
|---|-----------|--------|------------------|
| 1 | Activity & Consistency | **25%** | How regularly and sustainably you contribute |
| 2 | Documentation & Readability | **20%** | README coverage, descriptions, wiki/pages |
| 3 | Project Quality & Originality | **25%** | Stars, language diversity, freshness, originality |
| 4 | Professionalism & Branding | **15%** | Profile completeness, bio, links, hireable flag |
| 5 | Impact & Collaboration | **15%** | Followers, forks, community engagement |

Weights are configurable via environment variables (`WEIGHT_ACTIVITY`, `WEIGHT_DOCUMENTATION`, etc.).

---

### 1. Activity & Consistency (25 pts) — GraphQL Mode

When GitHub GraphQL contribution data is available (default), the score uses **accurate calendar-year metrics** spanning the last 5 full years plus the current partial year.

| Sub-score | Max Pts | Formula | Benchmark |
|-----------|---------|---------|------------|
| Sustained Weekly Effort | 30 | `min(per_week / 10 × 30, 30)` | 10+ contributions/week → full marks |
| Stability & Consistency | 25 | streak (12) + current bonus (3) + low volatility (10) | 30-day streak → 12 pts; volatility 0.0 → 10 pts |
| Recency & Momentum | 25 | last-12-month volume (10) + trend signal (15) | 400+ contributions/yr → 10 pts; strong growth → 15 pts |
| Contribution Diversity | 20 | commits (8) + PRs (5) + reviews (4) + issues (3) | 200 commits, 20 PRs, 10 reviews, 10 issues → full |

**Streak scoring:**
- Longest streak: `min(longest_streak / 30 × 12, 12)`
- Current streak bonus: `min(current_streak / 14 × 3, 3)`

**Volatility bonus** (lower is better):
- `max(10 × (1 − min(volatility_score, 1.0)), 0)`

**Trend signal mapping:**

| Signal | Points |
|--------|--------|
| `strong_growth` | 15 |
| `growth` | 12 |
| `stable` | 9 |
| `decline` | 5 |
| `strong_decline` | 2 |
| `insufficient_data` | 7.5 |

**Validation penalty:** If cross-verification detects unreliable years, a penalty of `min(unreliable_years × 3, 10)` is subtracted.

#### REST Fallback Mode

When GraphQL data is unavailable, a simpler calculation is used:

| Sub-score | Max Pts | Formula |
|-----------|---------|----------|
| Commit frequency | 40 | `min(commits_per_month / 15 × 40, 40)` |
| Recent activity | 30 | `min(commits_last_year / 100 × 30, 30)` |
| Consistency | 20 | `min(longest_streak / 30 × 20, 20)` |
| Account maturity | 10 | `min(account_age_years / 2 × 10, 10)` |

---

### 2. Documentation & Readability (20 pts)

| Sub-score | Max Pts | Formula |
|-----------|---------|----------|
| README coverage | 50 | `(repos_with_readme / total_repos) × 50` |
| Repo descriptions | 30 | `(repos_with_description / total_repos) × 30` |
| Documentation features | 20 | wiki (7) + GitHub Pages (7) + Issues enabled (6), each ratio-weighted |

---

### 3. Project Quality & Originality (25 pts)

| Sub-score | Max Pts | Formula | Benchmark |
|-----------|---------|---------|------------|
| Stars & engagement | 35 | `min(engagement / 50 × 35, 35)` | engagement = stars + (forks × 2); 50+ → full |
| Language diversity | 25 | `min(unique_languages / 5 × 25, 25)` | 5+ languages → full marks |
| Project freshness | 20 | `(repos_updated_last_6mo / total_repos) × 20` | — |
| Originality | 20 | `(original_repos / total_repos) × 20` | Excludes repos with "tutorial", "practice", etc. in name AND < 100 KB |

---

### 4. Professionalism & Branding (15 pts)

| Sub-score | Max Pts | Formula |
|-----------|---------|----------|
| Profile completeness | 40 | `(filled_fields / 5) × 40` — fields: name, bio, location, email, company |
| Professional presentation | 30 | Meaningful bio > 20 chars (15) + hireable flag (10) + 5+ public repos (5) |
| Online presence | 30 | Personal website (15) + Twitter/social (10) + company affiliation (5) |

---

### 5. Impact & Collaboration (15 pts)

| Sub-score | Max Pts | Formula | Benchmark |
|-----------|---------|---------|------------|
| Followers | 40 | `min(followers / 50 × 40, 40)` | 50+ followers → full marks |
| Repository forks | 30 | `min(total_forks / 20 × 30, 30)` | 20+ forks → full marks |
| Collaboration indicators | 30 | Has forked repos (10) + forks > 5 (10) + follower ratio ≥ 0.5 (10) |

---

### Percentile Rank

| Final Score | Rank |
|-------------|------|
| 90+ | Top 5% |
| 80–89 | Top 15% |
| 70–79 | Top 30% |
| 60–69 | Top 50% |
| < 60 | Below Average |

---

### Example Calculation

```
Activity & Consistency:     72 / 100 × 25 = 18.0
Documentation:              85 / 100 × 20 = 17.0
Project Quality:            60 / 100 × 25 = 15.0
Professionalism:            90 / 100 × 15 = 13.5
Impact & Collaboration:     45 / 100 × 15 =  6.75
                                           ───────
Final Score:                                70.25  →  Top 30%
```

## 🚀 Quick Start

### Prerequisites

- **Backend**: Python 3.10+, pip
- **Frontend**: Node.js 18+, npm
- **Optional**: GitHub token (for higher rate limits), Anthropic API key (for AI feedback)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd "GIthub analyzer"
```

2. **Set up backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys (optional)
```

3. **Set up frontend:**
```bash
cd ../frontend
npm install
cp .env.example .env
# Edit .env if needed (default works for local dev)
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📁 Project Structure

```
GIthub analyzer/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   └── routes.py      # Main analyze endpoint
│   │   ├── core/              # Configuration
│   │   │   └── config.py      # Environment settings
│   │   ├── models/            # Data models
│   │   │   └── schemas.py     # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   │   ├── github_service.py      # GitHub API client
│   │   │   ├── scoring_engine.py      # Score calculation
│   │   │   ├── analyzer.py            # Insight detection
│   │   │   └── feedback_generator.py  # AI feedback
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ScoreCard.jsx
│   │   │   ├── ChartsSection.jsx
│   │   │   └── ...
│   │   ├── services/
│   │   │   └── api.js         # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── README.md
│
└── README.md                   # This file
```

## 🔧 Configuration

### Backend Configuration (.env)

```bash
# Optional: Increases GitHub API rate limit
GITHUB_TOKEN=ghp_your_token_here

# Optional: Enables AI feedback using Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Scoring weights (should sum to 100)
WEIGHT_ACTIVITY=25.0
WEIGHT_DOCUMENTATION=20.0
WEIGHT_QUALITY=25.0
WEIGHT_PROFESSIONALISM=15.0
WEIGHT_IMPACT=15.0
```

### Frontend Configuration (.env)

```bash
VITE_API_BASE_URL=http://localhost:8000
```

## 📖 Usage

1. **Enter GitHub Username**: Type any public GitHub username
2. **Toggle AI Feedback**: Choose whether to include AI-powered recommendations
3. **Analyze**: Click analyze and wait 10-30 seconds
4. **Review Results**: Explore your score, insights, and recommendations
5. **Export/Share**: Download JSON or share results

## 🧪 Testing

### Backend
```bash
cd backend
pytest tests/
```

### Frontend
```bash
cd frontend
npm run lint
npm run test  # (when tests are added)
```

### Manual Testing
```bash
# Check backend health
curl http://localhost:8000/health

# Analyze a profile
curl -X POST http://localhost:8000/api/analyze/octocat
```

## 🚢 Deployment

### Backend Deployment (Example: Railway/Render)

1. Set environment variables in hosting platform
2. Use Gunicorn with Uvicorn workers:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment (Example: Vercel/Netlify)

1. Build the frontend:
```bash
npm run build
```

2. Deploy `dist/` folder

3. Set environment variable:
```bash
VITE_API_BASE_URL=https://your-backend-domain.com
```



## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.115.0
- **HTTP Client**: httpx 0.27.2
- **Validation**: Pydantic 2.9.2
- **AI**: Anthropic Claude 0.39.0 (optional)
- **Server**: Uvicorn 0.32.0

### Frontend
- **Framework**: React 18.3
- **Build Tool**: Vite 5.4
- **Styling**: Tailwind CSS 3.4
- **Charts**: Recharts 2.12
- **Icons**: Lucide React 0.460
- **HTTP**: Axios 1.7.7



## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Follow existing code style
4. Add tests for new features
5. Update documentation
6. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## � Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation

---

**Built with ❤️ for students and early-career developers** 🎓

**Target Users**: Students preparing for internships and entry-level software engineering roles

**Goal**: Help developers understand and improve their GitHub portfolios from a recruiter's perspective
