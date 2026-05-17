'use client';

import { useState, useEffect } from 'react';
import { AnalyzeResponse, RepoSuggestion } from '@/types/kit';
import { analyzeRepo, recommendRepos } from '@/lib/api';
import HeroInput from '@/components/HeroInput';
import LoadingState from '@/components/LoadingState';
import RecommendingState from '@/components/RecommendingState';
import RecommendationResults from '@/components/RecommendationResults';
import RepoHeader from '@/components/RepoHeader';
import ReadinessScore from '@/components/ReadinessScore';
import KitTabs from '@/components/KitTabs';
import DownloadButton from '@/components/DownloadButton';
import ArchitectureSection from '@/components/sections/ArchitectureSection';
import ComponentsSection from '@/components/sections/ComponentsSection';
import HotspotsSection from '@/components/sections/HotspotsSection';
import TasksSection from '@/components/sections/TasksSection';
import PatternsSection from '@/components/sections/PatternsSection';
import SetupSection from '@/components/sections/SetupSection';

type AppState = 'idle' | 'loading' | 'recommending' | 'recommendations' | 'result' | 'error';

interface RecentRepo {
  url: string;
  repo: string;
  language: string;
}

export default function Home() {
  const [state, setState] = useState<AppState>('idle');
  const [data, setData] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [recentRepos, setRecentRepos] = useState<RecentRepo[]>([]);
  const [requirement, setRequirement] = useState<string>('');
  const [suggestions, setSuggestions] = useState<RepoSuggestion[]>([]);

  // Load recent repos from localStorage
  useEffect(() => {
    const stored = localStorage.getItem('devlift_recent');
    if (stored) {
      try {
        setRecentRepos(JSON.parse(stored));
      } catch (e) {
        // Ignore parse errors
      }
    }
  }, []);

  // Save to recent repos
  const saveToRecent = (response: AnalyzeResponse) => {
    const newRepo: RecentRepo = {
      url: `https://github.com/${response.owner}/${response.repo}`,
      repo: response.repo,
      language: response.language,
    };

    const updated = [
      newRepo,
      ...recentRepos.filter((r) => r.url !== newRepo.url),
    ].slice(0, 5);

    setRecentRepos(updated);
    localStorage.setItem('devlift_recent', JSON.stringify(updated));
  };

  const handleSubmit = async (url: string) => {
    setState('loading');
    setError('');

    try {
      const response = await analyzeRepo(url);
      setData(response);
      setState('result');
      saveToRecent(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setState('error');
    }
  };

  const handleRecommend = async (req: string) => {
    setState('recommending');
    setError('');
    setRequirement(req);

    try {
      const response = await recommendRepos(req);
      setSuggestions(response.suggestions);
      setState('recommendations');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get recommendations');
      setState('error');
    }
  };

  const handleSelectRepo = (url: string) => {
    // When user selects a repo from recommendations, analyze it
    handleSubmit(url);
  };

  const handleReset = () => {
    setState('idle');
    setData(null);
    setError('');
    setRequirement('');
    setSuggestions([]);
  };

  // State 1: Idle (Hero)
  if (state === 'idle') {
    return (
      <HeroInput 
        onSubmit={handleSubmit} 
        onRecommend={handleRecommend}
        recentRepos={recentRepos} 
      />
    );
  }

  // State 2: Loading (analyzing repo)
  if (state === 'loading') {
    return <LoadingState />;
  }

  // State 3: Recommending (finding repos)
  if (state === 'recommending') {
    return <RecommendingState />;
  }

  // State 4: Recommendations (show repo suggestions)
  if (state === 'recommendations') {
    return (
      <div className="min-h-screen bg-background px-4 py-12">
        <RecommendationResults
          requirement={requirement}
          suggestions={suggestions}
          onSelect={handleSelectRepo}
          onBack={handleReset}
        />
      </div>
    );
  }

  // State 5: Error
  if (state === 'error') {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="max-w-md w-full">
          <div className="bg-card border border-destructive rounded-lg p-6">
            <div className="flex items-start gap-3 mb-4">
              <span className="text-2xl">⚠</span>
              <div>
                <h2 className="text-xl font-bold text-destructive mb-2">
                  {suggestions.length > 0 ? 'Could not analyze this repository' : 'Could not get recommendations'}
                </h2>
                <p className="text-muted-foreground text-sm">{error}</p>
              </div>
            </div>
            <div className="flex gap-3">
              <button
                onClick={handleReset}
                className="flex-1 px-4 py-2 bg-secondary hover:bg-secondary/80 border border-border rounded-lg text-foreground transition-colors"
              >
                Try again
              </button>
              {data && (
                <button
                  onClick={() => handleSubmit(`https://github.com/${data.owner}/${data.repo}`)}
                  className="flex-1 px-4 py-2 rounded-lg text-white transition-colors"
                  style={{ background: '#0062FF' }}
                  onMouseEnter={(e) => e.currentTarget.style.background = '#0053d6'}
                  onMouseLeave={(e) => e.currentTarget.style.background = '#0062FF'}
                >
                  Retry
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // State 6: Result (show onboarding kit)
  if (state === 'result' && data) {
    return (
      <div className="min-h-screen bg-background">
        <div className="max-w-6xl mx-auto px-4 py-8">
          {/* Back button */}
          <button
            onClick={handleReset}
            className="mb-6 transition-colors flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground"
            style={{
              color: suggestions.length > 0 ? '#0062FF' : undefined
            }}
          >
            <span>←</span>
            <span>{suggestions.length > 0 ? 'Back to recommendations' : 'Analyze another repo'}</span>
          </button>

          {/* Repo header */}
          <RepoHeader data={data} />

          {/* Readiness Score */}
          <ReadinessScore readiness={data.readiness} />

          {/* Kit tabs and sections */}
          <div className="bg-card border border-border rounded-lg p-6">
            <KitTabs>
              <ArchitectureSection overview={data.kit.architecture_overview} />
              <ComponentsSection components={data.kit.key_components} />
              <HotspotsSection hotspots={data.kit.complexity_hotspots} />
              <TasksSection tasks={data.kit.suggested_first_tasks} />
              <PatternsSection patterns={data.kit.common_patterns} />
              <SetupSection setup={data.kit.setup_summary} />
            </KitTabs>
          </div>

          {/* Download button */}
          <DownloadButton data={data} />
        </div>
      </div>
    );
  }

  return null;
}

// Made with Bob
