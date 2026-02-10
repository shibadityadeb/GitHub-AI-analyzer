import { CheckCircle, AlertTriangle, XCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { useState } from 'react';

export default function InsightsList({ strengths, weaknesses, redFlags }) {
  const [expandedStrength, setExpandedStrength] = useState(null);
  const [expandedWeakness, setExpandedWeakness] = useState(null);
  const [expandedRedFlag, setExpandedRedFlag] = useState(null);

  const InsightCard = ({ items, type, icon: Icon, colorClasses, expanded, setExpanded }) => {
    if (!items || items.length === 0) return null;

    return (
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Icon className={`w-6 h-6 ${colorClasses.icon}`} />
          <h3 className="card-header mb-0">
            {type} ({items.length})
          </h3>
        </div>

        <div className="space-y-3">
          {items.map((item, index) => (
            <div
              key={index}
              className={`border-l-4 ${colorClasses.border} bg-gray-50 p-4 rounded-r-lg`}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <span className={`badge ${colorClasses.badge}`}>
                      {item.category || item.flag_type || 'General'}
                    </span>
                    {item.impact && (
                      <span className={`text-xs font-medium ${
                        item.impact === 'High' ? 'text-red-600' :
                        item.impact === 'Medium' ? 'text-yellow-600' :
                        'text-gray-600'
                      }`}>
                        Impact: {item.impact}
                      </span>
                    )}
                    {item.severity && (
                      <span className={`text-xs font-medium ${
                        item.severity === 'Critical' ? 'text-red-600' :
                        item.severity === 'Moderate' ? 'text-yellow-600' :
                        'text-gray-600'
                      }`}>
                        Severity: {item.severity}
                      </span>
                    )}
                  </div>
                  
                  <h4 className="font-semibold text-gray-900 mb-2">{item.title}</h4>
                  <p className="text-gray-700 mb-3">{item.description}</p>

                  {expanded === index && (
                    <div className="mt-3 space-y-2 text-sm animate-fadeIn">
                      {item.evidence && item.evidence.length > 0 && (
                        <div>
                          <p className="font-medium text-gray-900 mb-1">Evidence:</p>
                          <ul className="list-disc list-inside space-y-1 text-gray-600">
                            {item.evidence.map((evidence, i) => (
                              <li key={i}>{evidence}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      {item.suggestion && (
                        <div className="bg-blue-50 p-3 rounded-lg">
                          <p className="font-medium text-blue-900 mb-1">💡 Suggestion:</p>
                          <p className="text-blue-800">{item.suggestion}</p>
                        </div>
                      )}
                      
                      {item.how_to_fix && (
                        <div className="bg-green-50 p-3 rounded-lg">
                          <p className="font-medium text-green-900 mb-1">🔧 How to Fix:</p>
                          <p className="text-green-800">{item.how_to_fix}</p>
                        </div>
                      )}
                      
                      {item.recruiter_perspective && (
                        <div className="bg-purple-50 p-3 rounded-lg">
                          <p className="font-medium text-purple-900 mb-1">👔 Recruiter Perspective:</p>
                          <p className="text-purple-800">{item.recruiter_perspective}</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                <button
                  onClick={() => setExpanded(expanded === index ? null : index)}
                  className="ml-3 text-gray-400 hover:text-gray-600 transition-colors"
                >
                  {expanded === index ? (
                    <ChevronUp className="w-5 h-5" />
                  ) : (
                    <ChevronDown className="w-5 h-5" />
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <InsightCard
        items={strengths}
        type="Strengths"
        icon={CheckCircle}
        colorClasses={{
          icon: 'text-green-600',
          border: 'border-green-500',
          badge: 'badge-success'
        }}
        expanded={expandedStrength}
        setExpanded={setExpandedStrength}
      />

      <InsightCard
        items={weaknesses}
        type="Weaknesses"
        icon={AlertTriangle}
        colorClasses={{
          icon: 'text-yellow-600',
          border: 'border-yellow-500',
          badge: 'badge-warning'
        }}
        expanded={expandedWeakness}
        setExpanded={setExpandedWeakness}
      />

      <InsightCard
        items={redFlags}
        type="Red Flags"
        icon={XCircle}
        colorClasses={{
          icon: 'text-red-600',
          border: 'border-red-500',
          badge: 'badge-danger'
        }}
        expanded={expandedRedFlag}
        setExpanded={setExpandedRedFlag}
      />
    </div>
  );
}
