import { Activity, BookOpen, Star, User, Users } from 'lucide-react';

export default function ScoreBreakdown({ scoreBreakdown }) {
  const components = [
    {
      key: 'activity_and_consistency',
      label: 'Activity & Consistency',
      icon: Activity,
      color: 'blue',
      weight: scoreBreakdown.activity_and_consistency.weight
    },
    {
      key: 'documentation_and_readability',
      label: 'Documentation & Readability',
      icon: BookOpen,
      color: 'green',
      weight: scoreBreakdown.documentation_and_readability.weight
    },
    {
      key: 'project_quality_and_originality',
      label: 'Project Quality & Originality',
      icon: Star,
      color: 'purple',
      weight: scoreBreakdown.project_quality_and_originality.weight
    },
    {
      key: 'professionalism_and_branding',
      label: 'Professionalism & Branding',
      icon: User,
      color: 'orange',
      weight: scoreBreakdown.professionalism_and_branding.weight
    },
    {
      key: 'impact_and_collaboration',
      label: 'Impact & Collaboration',
      icon: Users,
      color: 'pink',
      weight: scoreBreakdown.impact_and_collaboration.weight
    }
  ];

  const getColorClasses = (color) => {
    const colors = {
      blue: { bg: 'bg-blue-500', text: 'text-blue-600', bgLight: 'bg-blue-50' },
      green: { bg: 'bg-green-500', text: 'text-green-600', bgLight: 'bg-green-50' },
      purple: { bg: 'bg-purple-500', text: 'text-purple-600', bgLight: 'bg-purple-50' },
      orange: { bg: 'bg-orange-500', text: 'text-orange-600', bgLight: 'bg-orange-50' },
      pink: { bg: 'bg-pink-500', text: 'text-pink-600', bgLight: 'bg-pink-50' }
    };
    return colors[color];
  };

  return (
    <div className="card">
      <h2 className="card-header">Score Breakdown</h2>
      <p className="text-gray-600 mb-6">
        Your portfolio is evaluated across 5 key dimensions that matter to recruiters
      </p>

      <div className="space-y-4">
        {components.map(({ key, label, icon: Icon, color, weight }) => {
          const componentData = scoreBreakdown[key];
          const score = componentData.score;
          const colors = getColorClasses(color);

          return (
            <div key={key} className="group">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-3">
                  <div className={`p-2 rounded-lg ${colors.bgLight}`}>
                    <Icon className={`w-5 h-5 ${colors.text}`} />
                  </div>
                  <div>
                    <div className="font-medium text-gray-900">{label}</div>
                    <div className="text-xs text-gray-500">Weight: {weight}%</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-2xl font-bold ${colors.text}`}>{score}</div>
                  <div className="text-xs text-gray-500">/ 100</div>
                </div>
              </div>

              {/* Progress bar */}
              <div className="relative h-3 bg-gray-100 rounded-full overflow-hidden">
                <div
                  className={`absolute inset-y-0 left-0 ${colors.bg} rounded-full transition-all duration-1000 ease-out`}
                  style={{ width: `${score}%` }}
                />
              </div>

              {/* Details on hover/expand */}
              <div className="mt-2 text-xs text-gray-500 grid grid-cols-2 md:grid-cols-3 gap-2">
                {Object.entries(componentData.details).slice(0, 3).map(([key, value]) => (
                  <div key={key} className="flex items-center justify-between bg-gray-50 px-2 py-1 rounded">
                    <span className="capitalize">{key.replace(/_/g, ' ')}:</span>
                    <span className="font-medium text-gray-700">
                      {typeof value === 'object' ? value.score || value.value || 'N/A' : value}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
