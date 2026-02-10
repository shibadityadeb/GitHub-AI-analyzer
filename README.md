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
│         React + Vite Frontend (Port 5173)       │
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
         │  • OpenAI (optional)│
         └─────────────────────┘
```

## 📊 Scoring System

### Five Weighted Dimensions

1. **Activity & Consistency (25%)**
   - Commit frequency and recent activity
   - Contribution streaks and patterns
   - Account maturity

2. **Documentation & Readability (20%)**
   - README coverage and quality
   - Repository descriptions
   - Documentation features

3. **Project Quality & Originality (25%)**
   - Stars and community engagement
   - Language diversity
   - Original work vs tutorials

4. **Professionalism & Branding (15%)**
   - Profile completeness
   - Professional presentation
   - Online presence

5. **Impact & Collaboration (15%)**
   - Follower count and ratio
   - Repository forks
   - Collaboration indicators

## 🚀 Quick Start

### Prerequisites

- **Backend**: Python 3.10+, pip
- **Frontend**: Node.js 18+, npm
- **Optional**: GitHub token (for higher rate limits), OpenAI API key (for AI feedback)

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
- Frontend: http://localhost:5173
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

# Optional: Enables AI feedback
OPENAI_API_KEY=sk-your-key-here
# OR
OPENROUTER_API_KEY=your-key-here

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

## 🎨 Screenshots

### Dashboard View
- Overall portfolio score with circular progress
- Score breakdown across 5 dimensions
- Language distribution and commit activity charts

### Insights
- Expandable strength cards with evidence
- Weakness cards with actionable suggestions
- Red flag detection with fix instructions

### AI Feedback
- Weekly improvement roadmap (30 days)
- Personalized project suggestions
- Honest recruiter perspective

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

### Docker Deployment

**Backend Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile:**
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

## 🐛 Troubleshooting

### Backend Issues

**Problem**: GitHub API rate limit exceeded
**Solution**: Add `GITHUB_TOKEN` to `.env` file

**Problem**: AI feedback not generating
**Solution**: Add `OPENAI_API_KEY` or `OPENROUTER_API_KEY`

**Problem**: User not found
**Solution**: Verify username exists and profile is public

### Frontend Issues

**Problem**: Can't connect to backend
**Solution**: Ensure backend is running on port 8000

**Problem**: CORS errors
**Solution**: Check `ALLOWED_ORIGINS` in backend `config.py`

**Problem**: Charts not rendering
**Solution**: Verify Recharts is installed: `npm install recharts`

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.115.0
- **HTTP Client**: httpx 0.27.2
- **Validation**: Pydantic 2.9.2
- **AI**: OpenAI 1.54.3 (optional)
- **Server**: Uvicorn 0.32.0

### Frontend
- **Framework**: React 18.3
- **Build Tool**: Vite 5.4
- **Styling**: Tailwind CSS 3.4
- **Charts**: Recharts 2.12
- **Icons**: Lucide React 0.460
- **HTTP**: Axios 1.7.7

## 📝 API Documentation

Interactive API documentation available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoint

**POST /api/analyze/{username}**

Request:
```bash
curl -X POST "http://localhost:8000/api/analyze/octocat?include_ai_feedback=true"
```

Response:
```json
{
  "username": "octocat",
  "analyzed_at": "2026-02-10T12:00:00Z",
  "score_breakdown": {
    "final_score": 78.5,
    "percentile_rank": "Top 15%",
    ...
  },
  "strengths": [...],
  "weaknesses": [...],
  "red_flags": [...],
  "ai_feedback": {...}
}
```

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

## 🙏 Acknowledgments

- GitHub REST API for profile data
- OpenAI for AI-powered insights
- React and FastAPI communities
- All contributors and testers

## 📧 Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

**Built with ❤️ for students and early-career developers** 🎓

**Target Users**: Students preparing for internships and entry-level software engineering roles

**Goal**: Help developers understand and improve their GitHub portfolios from a recruiter's perspective
