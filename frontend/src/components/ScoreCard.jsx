import { TrendingUp, Award } from 'lucide-react';

export default function ScoreCard({ score, percentileRank, analyzedAt }) {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreGradient = (score) => {
    if (score >= 80) return 'from-green-500 to-emerald-500';
    if (score >= 60) return 'from-blue-500 to-cyan-500';
    if (score >= 40) return 'from-yellow-500 to-orange-500';
    return 'from-red-500 to-pink-500';
  };

  const getRating = (score) => {
    if (score >= 90) return 'Exceptional';
    if (score >= 80) return 'Excellent';
    if (score >= 70) return 'Very Good';
    if (score >= 60) return 'Good';
    if (score >= 50) return 'Fair';
    return 'Needs Improvement';
  };

  return (
    <div className="card">
      <div className="grid md:grid-cols-2 gap-8">
        {/* Score Display */}
        <div className="flex flex-col items-center justify-center text-center">
          <div className="relative">
            {/* Circular progress */}
            <svg className="w-48 h-48" viewBox="0 0 200 200">
              {/* Background circle */}
              <circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke="#e5e7eb"
                strokeWidth="12"
              />
              {/* Progress circle */}
              <circle
                cx="100"
                cy="100"
                r="90"
                fill="none"
                stroke="url(#gradient)"
                strokeWidth="12"
                strokeDasharray={`${(score / 100) * 565.48} 565.48`}
                strokeLinecap="round"
                transform="rotate(-90 100 100)"
                className="transition-all duration-1000 ease-out"
              />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" className={`${getScoreGradient(score).split(' ')[0].replace('from-', 'text-')}`} stopColor="currentColor" />
                  <stop offset="100%" className={`${getScoreGradient(score).split(' ')[1].replace('to-', 'text-')}`} stopColor="currentColor" />
                </linearGradient>
              </defs>
            </svg>
            
            {/* Score text */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <div className={`text-5xl font-bold ${getScoreColor(score)}`}>
                {score}
              </div>
              <div className="text-gray-500 text-sm font-medium">out of 100</div>
            </div>
          </div>
          
          <div className="mt-4">
            <div className={`text-2xl font-bold ${getScoreColor(score)} mb-1`}>
              {getRating(score)}
            </div>
            <div className="text-gray-600">Portfolio Quality</div>
          </div>
        </div>

        {/* Details */}
        <div className="flex flex-col justify-center space-y-6">
          <div>
            <h3 className="card-header">GitHub Portfolio Score</h3>
            <p className="text-gray-600">
              Your portfolio ranks in the <span className="font-bold text-blue-600">{percentileRank}</span> of GitHub users analyzed.
            </p>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <Award className="w-5 h-5 text-blue-600" />
                <span className="font-medium text-gray-900">Percentile Rank</span>
              </div>
              <span className="font-bold text-blue-600">{percentileRank}</span>
            </div>

            <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <TrendingUp className="w-5 h-5 text-gray-600" />
                <span className="font-medium text-gray-900">Analyzed</span>
              </div>
              <span className="text-gray-600 text-sm">
                {new Date(analyzedAt).toLocaleDateString('en-US', {
                  month: 'short',
                  day: 'numeric',
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </span>
            </div>
          </div>

          <p className="text-sm text-gray-500 italic">
            This score reflects your GitHub profile from a recruiter's perspective for entry-level positions.
          </p>
        </div>
      </div>
    </div>
  );
}
