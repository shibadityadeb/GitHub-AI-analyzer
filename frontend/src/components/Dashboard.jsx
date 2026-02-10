import { ArrowLeft, Download, Share2 } from 'lucide-react';
import ProfileHeader from './ProfileHeader';
import ScoreCard from './ScoreCard';
import ScoreBreakdown from './ScoreBreakdown';
import InsightsList from './InsightsList';
import AIFeedbackSection from './AIFeedbackSection';
import ChartsSection from './ChartsSection';

export default function Dashboard({ data, onReset }) {
  const handleShare = () => {
    const url = `${window.location.origin}?username=${data.username}`;
    navigator.clipboard.writeText(url);
    alert('Link copied to clipboard!');
  };

  const handleExport = () => {
    const dataStr = JSON.stringify(data, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `github-analysis-${data.username}-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header Actions */}
      <div className="flex items-center justify-between">
        <button
          onClick={onReset}
          className="btn btn-secondary inline-flex items-center space-x-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>New Analysis</span>
        </button>
        
        <div className="flex items-center space-x-3">
          <button
            onClick={handleShare}
            className="btn btn-secondary inline-flex items-center space-x-2"
          >
            <Share2 className="w-4 h-4" />
            <span>Share</span>
          </button>
          <button
            onClick={handleExport}
            className="btn btn-secondary inline-flex items-center space-x-2"
          >
            <Download className="w-4 h-4" />
            <span>Export</span>
          </button>
        </div>
      </div>

      {/* Profile Header */}
      <ProfileHeader profile={data.profile} />

      {/* Main Score Card */}
      <ScoreCard
        score={data.score_breakdown.final_score}
        percentileRank={data.score_breakdown.percentile_rank}
        analyzedAt={data.analyzed_at}
      />

      {/* Score Breakdown */}
      <ScoreBreakdown scoreBreakdown={data.score_breakdown} />

      {/* Charts */}
      <ChartsSection
        languageStats={data.language_stats}
        commitActivity={data.commit_activity}
        contributionData={data.contribution_data}
        scoreBreakdown={data.score_breakdown}
      />

      {/* Insights (Strengths, Weaknesses, Red Flags) */}
      <InsightsList
        strengths={data.strengths}
        weaknesses={data.weaknesses}
        redFlags={data.red_flags}
      />

      {/* AI Feedback */}
      {data.ai_feedback && (
        <AIFeedbackSection feedback={data.ai_feedback} />
      )}
    </div>
  );
}
