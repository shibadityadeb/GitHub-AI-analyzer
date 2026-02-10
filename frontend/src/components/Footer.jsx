import { Github, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 mt-16">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <div className="flex flex-col md:flex-row items-center justify-between text-sm text-gray-600">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <span>Built with</span>
            <Heart className="w-4 h-4 text-red-500 fill-current" />
            <span>for students and early-career developers</span>
          </div>
          
          <div className="flex items-center space-x-6">
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-1 hover:text-blue-600 transition-colors"
            >
              <Github className="w-4 h-4" />
              <span>GitHub</span>
            </a>
            <span className="text-gray-400">|</span>
            <span>© 2026 GitHub Analyzer</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
