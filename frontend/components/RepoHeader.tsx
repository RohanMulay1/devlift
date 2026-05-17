'use client';

import { AnalyzeResponse } from '@/types/kit';

interface RepoHeaderProps {
  data: AnalyzeResponse;
}

export default function RepoHeader({ data }: RepoHeaderProps) {
  return (
    <div className="rounded-xl border border-border bg-card p-6 mb-6">
      {/* Repo name */}
      <h1 className="text-2xl font-bold">
        <span className="text-muted-foreground">{data.owner}/</span>
        <span className="text-foreground">{data.repo}</span>
      </h1>

      {/* Description */}
      {data.description && (
        <p className="text-sm text-muted-foreground mt-1 mb-4">{data.description}</p>
      )}

      {/* Stats row */}
      <div className="flex flex-wrap gap-2 mt-3">
        {/* Language pill */}
        <div 
          className="px-2.5 py-1 rounded-md text-xs font-medium"
          style={{
            background: 'rgba(0, 98, 255, 0.08)',
            border: '1px solid rgba(0, 98, 255, 0.25)',
            color: '#0062FF'
          }}
        >
          {data.language}
        </div>

        {/* Stars pill */}
        <div className="px-2.5 py-1 rounded-md text-xs bg-muted text-muted-foreground">
          ★ {data.stars.toLocaleString()}
        </div>

        {/* Forks pill */}
        <div className="px-2.5 py-1 rounded-md text-xs bg-muted text-muted-foreground">
          ⑂ {data.forks.toLocaleString()}
        </div>

        {/* Files analyzed pill */}
        <div className="px-2.5 py-1 rounded-md text-xs bg-muted text-muted-foreground">
          ⊞ {data.files_analyzed} files analyzed
        </div>
      </div>

      {/* Topics */}
      {data.topics.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-3">
          {data.topics.map((topic, idx) => (
            <span
              key={idx}
              className="px-2 py-0.5 rounded-md text-xs bg-secondary text-secondary-foreground border border-border"
            >
              {topic}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

// Made with Bob
