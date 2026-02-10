import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

export default function ChartsSection({ languageStats, commitActivity, contributionData, scoreBreakdown }) {
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

      {/* Contribution Data (GraphQL-sourced) */}
      {contributionData && (
        <>
          {/* Yearly Contributions Trend – rate-normalised (Task 8) */}
          <div className="card">
            <h3 className="card-header">Yearly Activity Rate</h3>
            <p className="text-sm text-gray-600 mb-2">
              {contributionData.total_contributions.toLocaleString()} total contributions
              {contributionData.is_trending_up
                ? <span className="ml-2 text-green-600 font-medium">↑ {contributionData.growth_rate}% growth</span>
                : contributionData.growth_rate < 0
                  ? <span className="ml-2 text-red-500 font-medium">↓ {Math.abs(contributionData.growth_rate)}% decline</span>
                  : <span className="ml-2 text-gray-500 font-medium">— stable</span>}
            </p>

            {(() => {
              const yearlyData = (contributionData.yearly_metrics || [])
                .slice()
                .sort((a, b) => a.year - b.year)
                .map(m => ({
                  year: `${m.year}${m.is_partial ? '*' : ''}`,
                  'Per Week': m.per_week ?? 0,
                  'Per Month': m.per_month ?? 0,
                  total: m.total ?? 0,
                }));

              return yearlyData.length > 0 ? (
                <ResponsiveContainer width="100%" height={240}>
                  <BarChart data={yearlyData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip
                      formatter={(value, name) => [value.toFixed(1), name]}
                      labelFormatter={label => `Year: ${label}`}
                    />
                    <Legend />
                    <Bar dataKey="Per Week" fill="#6366f1" radius={[6, 6, 0, 0]} />
                    <Bar dataKey="Per Month" fill="#a5b4fc" radius={[6, 6, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="text-center py-12 text-gray-500">No yearly data available</div>
              );
            })()}

            {/* Partial year annotation */}
            {(contributionData.yearly_metrics || []).some(m => m.is_partial) && (
              <p className="text-xs text-gray-400 mt-1">* Current year (partial data)</p>
            )}
          </div>

          {/* Activity Overview – trend, momentum, volatility */}
          {contributionData.activity_overview && (
            <div className="card">
              <h3 className="card-header">Activity Overview</h3>

              {(() => {
                const ao = contributionData.activity_overview;
                const trendColors = {
                  strong_growth: 'text-green-600 bg-green-50',
                  growth: 'text-green-500 bg-green-50',
                  stable: 'text-blue-600 bg-blue-50',
                  decline: 'text-orange-500 bg-orange-50',
                  strong_decline: 'text-red-600 bg-red-50',
                  insufficient_data: 'text-gray-500 bg-gray-50',
                };
                const trendLabels = {
                  strong_growth: '↑↑ Strong Growth',
                  growth: '↑ Growth',
                  stable: '→ Stable',
                  decline: '↓ Decline',
                  strong_decline: '↓↓ Strong Decline',
                  insufficient_data: '— Insufficient Data',
                };
                const cls = trendColors[ao.trend_signal] || 'text-gray-500 bg-gray-50';
                const label = trendLabels[ao.trend_signal] || ao.trend_signal;

                return (
                  <div className="space-y-4">
                    {/* Trend badge */}
                    <div className={`inline-block px-3 py-1 rounded-full font-semibold text-sm ${cls}`}>
                      {label}
                    </div>
                    {ao.trend_details && (
                      <p className="text-sm text-gray-600">{ao.trend_details}</p>
                    )}

                    {/* Metrics cards */}
                    <div className="grid grid-cols-3 gap-3">
                      {ao.moving_average_3yr != null && (
                        <div className="bg-indigo-50 p-3 rounded-lg text-center">
                          <div className="text-xs text-indigo-600 font-medium mb-1">3-Yr Avg/Week</div>
                          <div className="text-xl font-bold text-indigo-900">{ao.moving_average_3yr.toFixed(1)}</div>
                        </div>
                      )}
                      {ao.momentum_index != null && (
                        <div className="bg-emerald-50 p-3 rounded-lg text-center">
                          <div className="text-xs text-emerald-600 font-medium mb-1">Momentum</div>
                          <div className="text-xl font-bold text-emerald-900">{ao.momentum_index.toFixed(2)}x</div>
                        </div>
                      )}
                      {ao.volatility_score != null && (
                        <div className="bg-amber-50 p-3 rounded-lg text-center">
                          <div className="text-xs text-amber-600 font-medium mb-1">Volatility</div>
                          <div className="text-xl font-bold text-amber-900">{(ao.volatility_score * 100).toFixed(0)}%</div>
                        </div>
                      )}
                    </div>

                    {/* Per-year active days table */}
                    {(contributionData.yearly_metrics || []).length > 0 && (
                      <div className="mt-2">
                        <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Active Days</h4>
                        <div className="space-y-1">
                          {(contributionData.yearly_metrics || [])
                            .slice()
                            .sort((a, b) => b.year - a.year)
                            .map(m => (
                              <div key={m.year} className="flex items-center justify-between text-sm">
                                <span className="text-gray-600">{m.year}{m.is_partial ? '*' : ''}</span>
                                <div className="flex items-center space-x-3">
                                  <span className="text-gray-900 font-medium">{m.active_days ?? 0} days</span>
                                  <span className="text-gray-500">{m.total?.toLocaleString()} contribs</span>
                                </div>
                              </div>
                            ))}
                        </div>
                      </div>
                    )}
                  </div>
                );
              })()}
            </div>
          )}

          {/* Contribution Breakdown */}
          <div className="card">
            <h3 className="card-header">Contribution Breakdown</h3>
            <p className="text-sm text-gray-600 mb-4">
              Avg {contributionData.weekly_average} contributions/week
            </p>

            {(() => {
              const bd = contributionData.contribution_breakdown || {};
              const breakdownData = [
                { name: 'Commits', value: bd.commits || 0 },
                { name: 'Pull Requests', value: bd.pull_requests || 0 },
                { name: 'Reviews', value: bd.reviews || 0 },
                { name: 'Issues', value: bd.issues || 0 },
                { name: 'New Repos', value: bd.repositories || 0 },
              ].filter(d => d.value > 0);

              const BD_COLORS = ['#3b82f6', '#10b981', '#f97316', '#ec4899', '#8b5cf6'];

              return breakdownData.length > 0 ? (
                <>
                  <ResponsiveContainer width="100%" height={240}>
                    <PieChart>
                      <Pie
                        data={breakdownData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, value }) => `${name} ${value}`}
                        outerRadius={90}
                        dataKey="value"
                      >
                        {breakdownData.map((_, i) => (
                          <Cell key={`bd-${i}`} fill={BD_COLORS[i % BD_COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>

                  <div className="mt-3 space-y-2">
                    {breakdownData.map((item, i) => (
                      <div key={item.name} className="flex items-center justify-between text-sm">
                        <div className="flex items-center space-x-2">
                          <div className="w-3 h-3 rounded-full" style={{ backgroundColor: BD_COLORS[i % BD_COLORS.length] }} />
                          <span className="text-gray-700">{item.name}</span>
                        </div>
                        <span className="font-medium text-gray-900">{item.value.toLocaleString()}</span>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <div className="text-center py-12 text-gray-500">No breakdown data</div>
              );
            })()}
          </div>
        </>
      )}
    </div>
  );
}
