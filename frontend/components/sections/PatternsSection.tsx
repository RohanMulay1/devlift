'use client';

import { CommonPattern } from '@/types/kit';

interface PatternsSectionProps {
  patterns: CommonPattern[];
}

export default function PatternsSection({ patterns }: PatternsSectionProps) {
  return (
    <div className="divide-y" style={{ borderColor: 'hsl(var(--border))' }}>
      {patterns.map((pattern, idx) => (
        <div key={idx} className="py-5 first:pt-0 last:pb-0 space-y-3">
          <h3 className="text-base font-semibold text-foreground">{pattern.pattern}</h3>

          <p className="text-base leading-7" style={{ color: 'hsl(var(--muted-foreground))' }}>
            {pattern.description}
          </p>

          {pattern.example && (
            <pre
              className="text-sm font-mono leading-7 overflow-x-auto rounded-lg px-5 py-4"
              style={{
                background: 'hsl(var(--muted))',
                color: 'hsl(var(--foreground))',
                opacity: 0.85,
                borderLeft: '2px solid rgba(0,98,255,0.4)',
              }}
            >
              {pattern.example}
            </pre>
          )}
        </div>
      ))}
    </div>
  );
}
