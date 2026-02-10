import { AlertCircle, RefreshCw } from 'lucide-react';

export default function ErrorDisplay({ error, onRetry }) {
  return (
    <div className="max-w-2xl mx-auto animate-fadeIn">
      <div className="card border-red-200 bg-red-50">
        <div className="flex items-start space-x-4">
          <AlertCircle className="w-8 h-8 text-red-600 flex-shrink-0 mt-1" />
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-red-900 mb-2">
              Analysis Failed
            </h3>
            <p className="text-red-700 mb-4">
              {error}
            </p>
            
            <div className="bg-white rounded-lg p-4 mb-4 text-sm text-gray-700">
              <p className="font-medium mb-2">Common issues:</p>
              <ul className="list-disc list-inside space-y-1 text-gray-600">
                <li>Username doesn't exist or is private</li>
                <li>Backend server is not running (should be at http://localhost:8000)</li>
                <li>GitHub API rate limit exceeded (add GITHUB_TOKEN to backend .env)</li>
                <li>User has no public repositories</li>
              </ul>
            </div>
            
            <button
              onClick={onRetry}
              className="btn btn-secondary inline-flex items-center space-x-2"
            >
              <RefreshCw className="w-4 h-4" />
              <span>Try Again</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
