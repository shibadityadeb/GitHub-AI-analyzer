import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

export default function ChartsSection({ languageStats, commitActivity, scoreBreakdown }) {
  // Language distribution data
  const languageData = Object.entries(languageStats.languages || {})
    .sort(([, a], [, b]) => b - a)
    .slice(0, 8)
    .map(([name, bytes]) => ({
      name,
      value: bytes,
      percentage: Math.round((bytes / Object.values(languageStats.languages).reduce((a, b) => a + b, 0)) * 100)
    }));

  // Score components data for bar chart
  const scoreData = [
    {
      name: 'Activity',
      score: scoreBreakdown.activity_and_consistency.score,
      color: '#3b82f6'
    },
    {
      name: 'Documentation',
      score: scoreBreakdown.documentation_and_readability.score,
      color: '#10b981'
    },
    {
      name: 'Quality',
      score: scoreBreakdown.project_quality_and_originality.score,
      color: '#8b5cf6'
    },
    {
      name: 'Professionalism',
      score: scoreBreakdown.professionalism_and_branding.score,
      color: '#f97316'
    },
    {
      name: 'Impact',
      score: scoreBreakdown.impact_and_collaboration.score,
      color: '#ec4899'
    }
  ];

  const COLORS = ['#3b82f6', '#10b981', '#8b5cf6', '#f97316', '#ec4899', '#6366f1', '#14b8a6', '#f59e0b'];

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-medium text-gray-900">{payload[0].name}</p>
          <p className="text-sm text-gray-600">
            {payload[0].value.toLocaleString()} bytes ({payload[0].payload.percentage}%)
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="grid md:grid-cols-2 gap-6">
      {/* Language Distribution */}
      <div className="card">
        <h3 className="card-header">Language Distribution</h3>
        <p className="text-sm text-gray-600 mb-4">
          Based on {languageStats.language_diversity} languages across all repositories
        </p>
        
        {languageData.length > 0 ? (
          <>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={languageData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percentage }) => `${name} ${percentage}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {languageData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip content={<CustomTooltip />} />
              </PieChart>
            </ResponsiveContainer>
            
            <div className="mt-4 space-y-2">
              {languageData.slice(0, 5).map((lang, index) => (
                <div key={lang.name} className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: COLORS[index % COLORS.length] }}
                    />
                    <span className="text-gray-700">{lang.name}</span>
                  </div>
                  <span className="font-medium text-gray-900">{lang.percentage}%</span>
                </div>
              ))}
            </div>
          </>
        ) : (
          <div className="text-center py-12 text-gray-500">
            No language data available
          </div>
        )}
      </div>

      {/* Score Components */}
      <div className="card">
        <h3 className="card-header">Score Components</h3>
        <p className="text-sm text-gray-600 mb-4">
          Comparative view of all five scoring dimensions
        </p>
        
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={scoreData} layout="vertical">
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" domain={[0, 100]} />
            <YAxis dataKey="name" type="category" width={120} />
            <Tooltip />
            <Bar dataKey="score" radius={[0, 8, 8, 0]}>
              {scoreData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>

        {/* Score summary */}
        <div className="mt-4 grid grid-cols-2 gap-3 text-sm">
          <div className="bg-gray-50 p-3 rounded-lg">
            <div className="text-gray-600">Highest Score</div>
            <div className="font-bold text-lg text-green-600">
              {Math.max(...scoreData.map(s => s.score))}
            </div>
          </div>
          <div className="bg-gray-50 p-3 rounded-lg">
            <div className="text-gray-600">Lowest Score</div>
            <div className="font-bold text-lg text-red-600">
              {Math.min(...scoreData.map(s => s.score))}
            </div>
          </div>
        </div>
      </div>

      {/* Commit Activity Stats */}
      <div className="card md:col-span-2">
        <h3 className="card-header">Commit Activity Overview</h3>
        
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="text-sm text-blue-600 font-medium mb-1">Total Commits</div>
            <div className="text-3xl font-bold text-blue-900">{commitActivity.total_commits}</div>
          </div>
          
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="text-sm text-green-600 font-medium mb-1">Recent (Year)</div>
            <div className="text-3xl font-bold text-green-900">{commitActivity.recent_commits}</div>
          </div>
          
          <div className="bg-purple-50 p-4 rounded-lg">
            <div className="text-sm text-purple-600 font-medium mb-1">Frequency</div>
            <div className="text-3xl font-bold text-purple-900">{commitActivity.commit_frequency}</div>
            <div className="text-xs text-purple-600">commits/month</div>
          </div>
          
          <div className="bg-orange-50 p-4 rounded-lg">
            <div className="text-sm text-orange-600 font-medium mb-1">Longest Streak</div>
            <div className="text-3xl font-bold text-orange-900">{commitActivity.longest_streak}</div>
            <div className="text-xs text-orange-600">days</div>
          </div>
          
          <div className="bg-pink-50 p-4 rounded-lg">
            <div className="text-sm text-pink-600 font-medium mb-1">Current Streak</div>
            <div className="text-3xl font-bold text-pink-900">{commitActivity.current_streak}</div>
            <div className="text-xs text-pink-600">days</div>
          </div>
        </div>
      </div>
    </div>
  );
}
