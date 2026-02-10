import { useState } from 'react';
import { BarChart3, Target, Rocket } from 'lucide-react';
import SearchBar from './components/SearchBar';
import Dashboard from './components/Dashboard';
import LoadingState from './components/LoadingState';
import ErrorDisplay from './components/ErrorDisplay';
import Header from './components/Header';
import Footer from './components/Footer';
import { analyzeProfile } from './services/api';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleAnalyze = async (username, includeAiFeedback) => {
    setLoading(true);
    setError(null);
    setAnalysisResult(null);

    try {
      const result = await analyzeProfile(username, includeAiFeedback);
      setAnalysisResult(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAnalysisResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 via-blue-50 to-gray-100">
      <Header />
      
      <main className="flex-1 container mx-auto px-4 py-8 max-w-7xl">
        {!analysisResult && !loading && (
          <div className="max-w-3xl mx-auto">
            <div className="text-center mb-12 animate-fadeIn">
              <h1 className="text-5xl font-bold text-gray-900 mb-4">
                GitHub Portfolio <span className="text-blue-600">Analyzer</span>
              </h1>
              <p className="text-xl text-gray-600 mb-2">
                See your GitHub profile from a recruiter's perspective
              </p>
              <p className="text-gray-500">
                Get actionable insights to improve your developer portfolio
              </p>
            </div>
            
            <SearchBar onAnalyze={handleAnalyze} />
            
            {/* Features Section */}
            <div className="mt-16 grid md:grid-cols-3 gap-6">
              <div className="card text-center">
                <div className="flex justify-center mb-3">
                  <BarChart3 className="w-10 h-10 text-blue-600" />
                </div>
                <h3 className="font-semibold text-lg mb-2">Portfolio Score</h3>
                <p className="text-gray-600 text-sm">
                  Get a comprehensive 0-100 score based on 5 key metrics
                </p>
              </div>
              <div className="card text-center">
                <div className="flex justify-center mb-3">
                  <Target className="w-10 h-10 text-blue-600" />
                </div>
                <h3 className="font-semibold text-lg mb-2">Recruiter Insights</h3>
                <p className="text-gray-600 text-sm">
                  Discover strengths, weaknesses, and red flags
                </p>
              </div>
              <div className="card text-center">
                <div className="flex justify-center mb-3">
                  <Rocket className="w-10 h-10 text-blue-600" />
                </div>
                <h3 className="font-semibold text-lg mb-2">Action Plan</h3>
                <p className="text-gray-600 text-sm">
                  Get a 30-day roadmap to improve your profile
                </p>
              </div>
            </div>
          </div>
        )}

        {loading && <LoadingState />}
        
        {error && <ErrorDisplay error={error} onRetry={handleReset} />}
        
        {analysisResult && !loading && (
          <Dashboard data={analysisResult} onReset={handleReset} />
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;
