'use client';

import { RepoSuggestion } from '@/types/kit';
import { Star, GitFork, ArrowRight } from 'lucide-react';

interface RecommendationResultsProps {
  requirement: string;
  suggestions: RepoSuggestion[];
  onSelect: (url: string) => void;
  onBack: () => void;
}

export default function RecommendationResults({
  requirement,
  suggestions,
  onSelect,
  onBack,
}: RecommendationResultsProps) {
  return (
    <div className="w-full max-w-5xl mx-auto space-y-6 animate-fadeIn">
      {/* Back button */}
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        <span>←</span>
        <span>Try a different requirement</span>
      </button>

      {/* Heading */}
      <div className="space-y-3">
        <h2 className="text-2xl font-semibold text-foreground">
          Best matches for your requirement
        </h2>
        <blockquote className="text-sm text-muted-foreground italic border-l-2 border-border pl-4 line-clamp-2">
          {requirement}
        </blockquote>
      </div>

      {/* Repository cards */}
      <div className="space-y-4">
        {suggestions.map((repo, idx) => (
          <div
            key={idx}
            className="border border-border bg-card rounded-xl p-5 hover:border-[#0062FF] transition-all duration-300 space-y-3"
          >
            {/* Header row */}
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <h3 className="text-lg font-semibold text-foreground truncate">
                  <span className="text-muted-foreground">{repo.owner}/</span>
                  <span>{repo.repo}</span>
                </h3>
              </div>
              <div className="flex items-center gap-3 text-sm text-muted-foreground flex-shrink-0">
                <div className="flex items-center gap-1">
                  <Star className="w-4 h-4" />
                  <span>{repo.stars.toLocaleString()}</span>
                </div>
                <div className="flex items-center gap-1">
                  <GitFork className="w-4 h-4" />
                  <span>{repo.forks.toLocaleString()}</span>
                </div>
              </div>
            </div>

            {/* Description */}
            <p className="text-sm text-muted-foreground line-clamp-2">
              {repo.description}
            </p>

            {/* Language pill */}
            {repo.language && (
              <div className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-muted text-muted-foreground border border-border">
                {repo.language}
              </div>
            )}

            {/* Why it matches */}
            <div className="pt-2 border-t border-border">
              <p className="text-xs text-muted-foreground italic">
                <span className="font-semibold text-foreground">Why this matches: </span>
                {repo.why}
              </p>
            </div>

            {/* Analyze button */}
            <div className="flex justify-end pt-2">
              <button
                onClick={() => onSelect(repo.url)}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
                style={{
                  background: '#0062FF',
                  color: 'white',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = '#0053d6';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = '#0062FF';
                }}
              >
                <span>Analyze this repo</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Footer note */}
      <p className="text-xs text-center text-muted-foreground pt-4">
        Found {suggestions.length} {suggestions.length === 1 ? 'repository' : 'repositories'} matching your requirements
      </p>
    </div>
  );
}

// Made with Bob