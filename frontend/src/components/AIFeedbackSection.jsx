import { Sparkles, Lightbulb, Calendar, Code2, Target } from 'lucide-react';
import { useState } from 'react';

export default function AIFeedbackSection({ feedback }) {
  const [activeWeek, setActiveWeek] = useState(1);

  if (!feedback) return null;

  // Group roadmap items by week
  const weeklyRoadmap = feedback.roadmap_30_days.reduce((acc, item) => {
    if (!acc[item.week]) acc[item.week] = [];
    acc[item.week].push(item);
    return acc;
  }, {});

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'High': return 'text-red-600 bg-red-50';
      case 'Medium': return 'text-yellow-600 bg-yellow-50';
      case 'Low': return 'text-green-600 bg-green-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Advanced': return 'text-purple-600 bg-purple-50';
      case 'Intermediate': return 'text-blue-600 bg-blue-50';
      case 'Beginner': return 'text-green-600 bg-green-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <div className="space-y-6">
      {/* AI Summary Card */}
      <div className="card bg-gradient-to-br from-purple-50 to-blue-50 border-purple-200">
        <div className="flex items-start space-x-3 mb-4">
          <Sparkles className="w-6 h-6 text-purple-600 flex-shrink-0 mt-1" />
          <div>
            <h3 className="card-header mb-2">AI-Powered Analysis</h3>
            <p className="text-gray-700 text-lg leading-relaxed">{feedback.summary}</p>
          </div>
        </div>
      </div>

      {/* Key Takeaways */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Lightbulb className="w-6 h-6 text-yellow-600" />
          <h3 className="card-header mb-0">Key Takeaways</h3>
        </div>
        
        <ul className="space-y-3">
          {feedback.key_takeaways.map((takeaway, index) => (
            <li key={index} className="flex items-start space-x-3">
              <span className="flex-shrink-0 w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-medium">
                {index + 1}
              </span>
              <span className="text-gray-700 flex-1">{takeaway}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* 30-Day Roadmap */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <Calendar className="w-6 h-6 text-blue-600" />
          <h3 className="card-header mb-0">30-Day Improvement Roadmap</h3>
        </div>

        {/* Week selector */}
        <div className="flex items-center space-x-2 mb-6 overflow-x-auto pb-2">
          {[1, 2, 3, 4].map((week) => (
            <button
              key={week}
              onClick={() => setActiveWeek(week)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors whitespace-nowrap ${
                activeWeek === week
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              Week {week}
            </button>
          ))}
        </div>

        {/* Roadmap items for selected week */}
        <div className="space-y-4">
          {(weeklyRoadmap[activeWeek] || []).map((item, index) => (
            <div key={index} className="border-l-4 border-blue-500 bg-gray-50 p-4 rounded-r-lg">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <span className={`badge ${getPriorityColor(item.priority)}`}>
                    {item.priority} Priority
                  </span>
                  <span className="text-sm text-gray-500">{item.time_estimate}</span>
                </div>
              </div>
              
              <h4 className="font-semibold text-gray-900 mb-2">{item.action}</h4>
              
              <div className="bg-blue-50 p-3 rounded-lg">
                <p className="text-sm text-blue-900">
                  <span className="font-medium">Expected Impact:</span> {item.expected_impact}
                </p>
              </div>
            </div>
          ))}
          
          {(!weeklyRoadmap[activeWeek] || weeklyRoadmap[activeWeek].length === 0) && (
            <div className="text-center py-8 text-gray-500">
              No tasks scheduled for this week
            </div>
          )}
        </div>
      </div>

      {/* Project Suggestions */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <Code2 className="w-6 h-6 text-green-600" />
          <h3 className="card-header mb-0">Recommended Projects</h3>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {feedback.project_suggestions.map((project, index) => (
            <div key={index} className="border border-gray-200 rounded-lg p-5 hover:border-blue-300 hover:shadow-md transition-all">
              <div className="flex items-start justify-between mb-3">
                <h4 className="font-bold text-lg text-gray-900">{project.title}</h4>
                <span className={`badge ${getDifficultyColor(project.difficulty)}`}>
                  {project.difficulty}
                </span>
              </div>
              
              <p className="text-gray-700 mb-4 text-sm">{project.description}</p>
              
              <div className="space-y-3">
                <div>
                  <p className="text-xs font-medium text-gray-500 mb-2">Tech Stack:</p>
                  <div className="flex flex-wrap gap-2">
                    {project.tech_stack.map((tech, i) => (
                      <span key={i} className="badge badge-info text-xs">
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="bg-purple-50 p-3 rounded-lg">
                  <p className="text-xs text-purple-900">
                    <span className="font-medium">Why it matters:</span> {project.why_it_matters}
                  </p>
                </div>
                
                <div className="flex items-center justify-between text-xs text-gray-600">
                  <span className="flex items-center space-x-1">
                    <Target className="w-3 h-3" />
                    <span>Estimated: {project.estimated_time}</span>
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recruiter Perspective */}
      <div className="card bg-gradient-to-br from-gray-50 to-blue-50 border-gray-300">
        <div className="mb-4">
          <h3 className="card-header">💼 Recruiter's Honest Perspective</h3>
          <p className="text-sm text-gray-600">Frank feedback from a hiring manager's viewpoint</p>
        </div>
        
        <div className="bg-white p-6 rounded-lg border-l-4 border-blue-600">
          <p className="text-gray-800 leading-relaxed whitespace-pre-line">
            {feedback.recruiter_perspective}
          </p>
        </div>
      </div>
    </div>
  );
}
