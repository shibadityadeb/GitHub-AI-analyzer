# ⚡ Quick Start Guide

## 🚀 Get Running in 5 Minutes

### Prerequisites Check
```bash
python --version  # Need 3.10+
node --version    # Need 18+
```

---

## 🔧 Setup

### 1. Backend Setup (Terminal 1)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Create environment file (optional but recommended)
cp .env.example .env

# Edit .env and add your GitHub token (optional)
# GITHUB_TOKEN=ghp_your_token_here
# Get token at: https://github.com/settings/tokens

# Start backend server
uvicorn app.main:app --reload --port 8000
```

**Backend will start at:** http://localhost:8000

✅ Verify: Visit http://localhost:8000/docs

---

### 2. Frontend Setup (Terminal 2)

```bash
# Navigate to frontend (open new terminal)
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend will start at:** http://localhost:3000

✅ Verify: Open http://localhost:3000 in your browser

---

## 🎮 Usage

1. **Enter a GitHub username** (try: `octocat`, `torvalds`, `gaearon`)
2. **Keep AI feedback enabled** (or disable for faster results)
3. **Click "Analyze Profile"**
4. **Wait 10-30 seconds**
5. **Explore your results!**

---

## 🐛 Troubleshooting

### Backend won't start?

**Problem**: "Module not found"
```bash
# Solution: Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Problem**: "Port 8000 already in use"
```bash
# Solution: Use a different port
uvicorn app.main:app --reload --port 8001

# Then update frontend .env:
# VITE_API_BASE_URL=http://localhost:8001
```

### Frontend won't start?

**Problem**: "Cannot find module"
```bash
# Solution: Delete and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem**: "CORS error" or "Network error"
```bash
# Solution: Ensure backend is running on port 8000
# Check: http://localhost:8000/health
```

### Analysis fails?

**Problem**: "GitHub API rate limit exceeded"
```bash
# Solution: Add GitHub token to backend/.env
# GITHUB_TOKEN=ghp_your_token_here
# Get token at: https://github.com/settings/tokens
```

**Problem**: "User not found"
```bash
# Verify username exists and profile is public
```

---

## 🎯 Next Steps

### Enhance Your Setup

1. **Add GitHub Token** (increases rate limit 60 → 5000/hr)
   ```bash
   # In backend/.env
   GITHUB_TOKEN=ghp_your_token_here
   ```

2. **Enable AI Feedback** (optional)
   ```bash
   # In backend/.env
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. **Customize Scoring Weights**
   ```bash
   # In backend/.env (must sum to 100)
   WEIGHT_ACTIVITY=25.0
   WEIGHT_DOCUMENTATION=20.0
   WEIGHT_QUALITY=25.0
   WEIGHT_PROFESSIONALISM=15.0
   WEIGHT_IMPACT=15.0
   ```

---

## 📖 Full Documentation

- **Main README**: [`/README.md`](README.md)
- **Backend Guide**: [`/backend/README.md`](backend/README.md)
- **Frontend Guide**: [`/frontend/README.md`](frontend/README.md)
- **Implementation Details**: [`/IMPLEMENTATION_GUIDE.md`](IMPLEMENTATION_GUIDE.md)

---

## 🎨 Project Structure

```
GIthub analyzer/
├── backend/              # FastAPI server
│   ├── app/
│   │   ├── api/         # Routes
│   │   ├── services/    # Business logic
│   │   ├── models/      # Data models
│   │   ├── core/        # Config
│   │   └── main.py      # Entry point
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/            # React app
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── services/    # API client
│   │   └── App.jsx
│   ├── package.json
│   └── .env.example
│
└── README.md           # Main docs
```

---

## 🌟 Features

- ✅ Portfolio Score (0-100) across 5 dimensions
- ✅ Strengths, Weaknesses, Red Flags detection
- ✅ Interactive charts (languages, scores, commits)
- ✅ AI-powered feedback with 30-day roadmap
- ✅ Project suggestions tailored to you
- ✅ Export results as JSON
- ✅ Mobile-responsive design

---

## 💡 Tips

- **Analyze yourself first** to understand the metrics
- **Compare with successful developers** in your target role
- **Use the roadmap** to prioritize improvements
- **Export results** to track progress over time
- **Share with mentors** to get additional feedback

---

## 🆘 Need Help?

1. Check the troubleshooting section above
2. Review the full README documents
3. Verify both servers are running
4. Check browser console for errors
5. Ensure environment variables are set correctly

---

**Built for students and early-career developers 🎓**

Happy analyzing! 🚀
