# GitHub AI Analyzer - Repository Description

## Short Description
AI-powered GitHub portfolio analyzer that provides recruiter-perspective scoring, insights, and personalized recommendations for developers

## Detailed Description

GitHub AI Analyzer is a production-ready web application designed to help students and early-career developers understand how recruiters view their GitHub profiles. The tool analyzes GitHub profiles from a recruiter's perspective and provides:

- **Objective Portfolio Scoring (0-100)**: Multi-dimensional scoring across 5 key metrics including activity, documentation, project quality, professionalism, and impact
- **Recruiter Insights**: Identifies strengths, weaknesses, and potential red flags that recruiters notice
- **AI-Powered Recommendations**: Personalized improvement roadmap and project suggestions using Anthropic Claude
- **Visual Analytics**: Interactive charts showing language distribution, commit activity, and score breakdowns
- **Actionable Advice**: Specific, prioritized improvements to increase chances of landing interviews

## Tech Stack

- **Backend**: FastAPI + Python 3.10+
- **Frontend**: React + Vite + Tailwind CSS
- **APIs**: GitHub REST API, Anthropic Claude (optional)
- **Features**: RESTful API, Interactive UI, Real-time analysis

## Target Users

Students preparing for internships and entry-level software engineering roles who want to optimize their GitHub presence for recruitment.

## Key Features

1. Multi-dimensional portfolio scoring system
2. Pattern-based insight detection
3. AI-generated feedback and recommendations
4. Visual analytics and progress tracking
5. Export and sharing capabilities

## Use Cases

- Prepare your GitHub profile before job applications
- Understand what recruiters look for in developer portfolios
- Get specific, actionable feedback on improving your projects
- Track your GitHub profile improvements over time
- Compare your profile against industry standards

## Quick Start

```bash
# Clone and setup
git clone https://github.com/shibadityadeb/GitHub-AI-analyzer
cd GitHub-AI-analyzer

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

Visit http://localhost:3000 to start analyzing GitHub profiles!
