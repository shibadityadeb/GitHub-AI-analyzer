import { Loader2 } from 'lucide-react';

export default function LoadingState() {
  return (
    <div className="flex flex-col items-center justify-center py-20 animate-fadeIn">
      <Loader2 className="w-16 h-16 text-blue-600 animate-spin mb-4" />
      <h3 className="text-xl font-semibold text-gray-900 mb-2">Analyzing GitHub Profile...</h3>
      <p className="text-gray-600 text-center max-w-md">
        Fetching repositories, calculating scores, and generating insights. This may take up to 30 seconds.
      </p>
      
      <div className="mt-8 space-y-2 text-sm text-gray-500">
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse"></div>
          <span>Fetching user profile and repositories...</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
          <span>Analyzing commit activity and languages...</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
          <span>Calculating portfolio scores...</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-pulse" style={{ animationDelay: '0.6s' }}></div>
          <span>Generating AI feedback...</span>
        </div>
      </div>
    </div>
  );
}
