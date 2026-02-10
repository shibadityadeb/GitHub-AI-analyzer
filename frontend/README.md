# 🚀 GitHub Portfolio Analyzer - Frontend

Modern, responsive React frontend for analyzing GitHub profiles from a recruiter's perspective.

## 🎨 Tech Stack

- **Framework**: React 18.3
- **Build Tool**: Vite 5.4
- **Styling**: Tailwind CSS 3.4
- **Charts**: Recharts 2.12
- **Icons**: Lucide React
- **HTTP Client**: Axios

## ✨ Features

### 📊 Interactive Dashboard
- Real-time GitHub profile analysis
- Comprehensive score visualization with circular progress
- Multi-dimensional score breakdown
- Language distribution pie charts
- Commit activity bar charts

### 🎯 Recruiter Insights
- **Strengths**: Positive signals with evidence
- **Weaknesses**: Areas for improvement with actionable suggestions
- **Red Flags**: Warning signals with fix recommendations
- Expandable cards for detailed insights

### 🤖 AI-Powered Feedback
- Recruiter-style summary
- 30-day improvement roadmap (week-by-week view)
- Personalized project suggestions
- Honest recruiter perspective

### 💻 User Experience
- Clean, modern UI with gradient backgrounds
- Smooth animations and transitions
- Mobile-responsive design
- Loading states with progress indicators
- Error handling with helpful suggestions
- Export analysis as JSON
- Shareable results

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn
- Backend server running at `http://localhost:8000`

### Installation

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create environment file (optional):**
```bash
# Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000" > .env
```

4. **Start development server:**
```bash
npm run dev
```

Frontend will start at `http://localhost:3000`

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/        # React components
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── SearchBar.jsx
│   │   ├── LoadingState.jsx
│   │   ├── ErrorDisplay.jsx
│   │   ├── Dashboard.jsx
│   │   ├── ProfileHeader.jsx
│   │   ├── ScoreCard.jsx
│   │   ├── ScoreBreakdown.jsx
│   │   ├── ChartsSection.jsx
│   │   ├── InsightsList.jsx
│   │   └── AIFeedbackSection.jsx
│   ├── services/
│   │   └── api.js         # API client
│   ├── App.jsx            # Main application
│   ├── main.jsx           # Entry point
│   └── index.css          # Global styles
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## 🎨 Component Overview

### Core Components

**App.jsx**
- Main application container
- State management for analysis results
- Handles API calls and error states

**SearchBar.jsx**
- Username input with validation
- AI feedback toggle
- Clean, accessible form design

**Dashboard.jsx**
- Main results view
- Orchestrates all data display components
- Export and share functionality

### Display Components

**ProfileHeader.jsx**
- GitHub user information
- Avatar, bio, location, links
- Repository and follower counts

**ScoreCard.jsx**
- Large circular score visualization
- Percentile ranking
- Color-coded rating system

**ScoreBreakdown.jsx**
- Five score components with progress bars
- Weighted percentages
- Detailed metrics for each dimension

**ChartsSection.jsx**
- Language distribution pie chart
- Score components bar chart
- Commit activity statistics

**InsightsList.jsx**
- Expandable strength/weakness/red flag cards
- Evidence and suggestions
- Color-coded by category

**AIFeedbackSection.jsx**
- AI-generated summary
- Week-by-week roadmap
- Project suggestions with tech stacks
- Recruiter perspective

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000

# Optional: Analytics, feature flags, etc.
```

### Vite Proxy

Development proxy is configured in `vite.config.js`:

```javascript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    }
  }
}
```

## 🎨 Styling

### Tailwind Configuration

Custom colors and utilities in `tailwind.config.js`:

- **Primary colors**: Blue gradient (50-900)
- **GitHub theme colors**: Dark mode compatible
- **Custom components**: Cards, badges, buttons
- **Animations**: Fade in, pulse effects

### Custom CSS Classes

Available utility classes in `index.css`:

```css
.card                 /* White card with shadow */
.card-header          /* Section heading */
.badge               /* Generic badge */
.badge-success       /* Green badge */
.badge-warning       /* Yellow badge */
.badge-danger        /* Red badge */
.badge-info          /* Blue badge */
.btn                 /* Generic button */
.btn-primary         /* Primary action button */
.btn-secondary       /* Secondary button */
.input               /* Form input */
```

## 📊 Data Flow

1. **User Input** → Enter GitHub username
2. **API Call** → POST to `/api/analyze/{username}`
3. **Loading State** → Show progress indicators
4. **Data Received** → Parse and structure data
5. **Render Components** → Display results
6. **User Interaction** → Expand cards, switch views

## 🧪 Development

### Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Code Style

- Component files use `.jsx` extension
- Functional components with hooks
- Props destructuring for clarity
- Tailwind for all styling (no CSS modules)

## 🏭 Production Build

### Build the app:
```bash
npm run build
```

Output will be in `dist/` folder.

### Deploy Options

**Static Hosting (Vercel, Netlify, etc.):**
```bash
# Build
npm run build

# Deploy dist/ folder
```

**Environment Variables:**
Set `VITE_API_BASE_URL` to your production API URL.

### Docker Deployment

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
CMD ["nginx", "-g", "daemon off;"]
```

## 🐛 Troubleshooting

### Backend Connection Issues
**Problem**: Can't connect to backend
**Solution**: 
- Ensure backend is running at `http://localhost:8000`
- Check CORS configuration in backend
- Verify proxy settings in vite.config.js

### Build Errors
**Problem**: npm install fails
**Solution**:
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Check Node.js version (need 18+)

### Chart Not Rendering
**Problem**: Recharts not displaying
**Solution**:
- Ensure data is in correct format
- Check browser console for errors
- Verify Recharts version compatibility

## 📱 Responsive Design

- **Mobile** (< 768px): Single column layout
- **Tablet** (768px - 1024px): Two column grid
- **Desktop** (> 1024px): Full three column layout

## ♿ Accessibility

- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance
- Focus indicators

## 🔗 API Integration

The frontend expects the backend API at:
- **Development**: `http://localhost:8000`
- **Production**: Set via `VITE_API_BASE_URL`

### API Endpoints Used

- `POST /api/analyze/{username}` - Analyze profile
- `GET /api/health` - Health check

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Follow existing code style
2. Use functional components
3. Maintain responsive design
4. Add comments for complex logic
5. Test on multiple screen sizes

---

**Built with ❤️ for students and developers** 🎓
