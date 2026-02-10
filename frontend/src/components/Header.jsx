import { Github } from 'lucide-react';

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="container mx-auto px-4 py-4 max-w-7xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Github className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-lg font-bold text-gray-900">GitHub Portfolio Analyzer</h1>
              <p className="text-xs text-gray-500">Recruiter Scorecard</p>
            </div>
          </div>
          
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-gray-600 hover:text-blue-600 transition-colors"
          >
            About
          </a>
        </div>
      </div>
    </header>
  );
}
