import { useState } from 'react';
import { Search, Sparkles } from 'lucide-react';

export default function SearchBar({ onAnalyze }) {
  const [username, setUsername] = useState('');
  const [includeAiFeedback, setIncludeAiFeedback] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (username.trim()) {
      onAnalyze(username.trim(), includeAiFeedback);
    }
  };

  return (
    <div className="card animate-fadeIn">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
            GitHub Username
          </label>
          <div className="relative">
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="octocat"
              className="input pl-12"
              required
            />
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          </div>
          <p className="mt-2 text-sm text-gray-500">
            Enter any public GitHub username to analyze their portfolio
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <input
            type="checkbox"
            id="ai-feedback"
            checked={includeAiFeedback}
            onChange={(e) => setIncludeAiFeedback(e.target.checked)}
            className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <label htmlFor="ai-feedback" className="flex items-center text-sm text-gray-700 cursor-pointer">
            <Sparkles className="w-4 h-4 mr-1 text-purple-500" />
            Include AI-powered feedback and recommendations
          </label>
        </div>

        <button type="submit" className="btn btn-primary w-full">
          Analyze Profile
        </button>
      </form>
    </div>
  );
}
