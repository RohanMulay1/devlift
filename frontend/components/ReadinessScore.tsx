'use client';

import { ReadinessScore as ReadinessScoreType } from '@/types/kit';

interface ReadinessScoreProps {
  readiness: ReadinessScoreType;
}

function barColor(pct: number): string {
  if (pct >= 70) return 'rgb(34, 197, 94)';
  if (pct >= 40) return 'rgb(234, 179, 8)';
  return 'rgb(239, 68, 68)';
}

function barGlow(pct: number): string {
  if (pct >= 70) return 'rgba(34,197,94,0.35)';
  if (pct >= 40) return 'rgba(234,179,8,0.35)';
  return 'rgba(239,68,68,0.35)';
}

const GRADE_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  A: { bg: 'rgba(34,197,94,0.12)',  text: 'rgb(34,197,94)',  border: 'rgba(34,197,94,0.3)'  },
  B: { bg: 'rgba(0,98,255,0.12)',   text: '#0062FF',         border: 'rgba(0,98,255,0.3)'   },
  C: { bg: 'rgba(234,179,8,0.12)',  text: 'rgb(234,179,8)',  border: 'rgba(234,179,8,0.3)'  },
  D: { bg: 'rgba(239,68,68,0.12)',  text: 'rgb(239,68,68)',  border: 'rgba(239,68,68,0.3)'  },
};

export default function ReadinessScore({ readiness }: ReadinessScoreProps) {
  const { score, grade, verdict, breakdown } = readiness;

  const gradeStyle = GRADE_COLORS[grade] ?? GRADE_COLORS.C;

  // SVG gauge
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const gaugeColor = barColor(score);

  return (
    <div className="rounded-xl bg-card border border-border p-6 mb-6">
      <h2 className="text-base font-semibold text-foreground mb-5">Contribution Readiness</h2>

      <div className="flex flex-col lg:flex-row gap-8 items-start">
        {/* Circular gauge */}
        <div className="flex flex-col items-center gap-3 flex-shrink-0">
          <div className="relative">
            <svg width="120" height="120" className="transform -rotate-90">
              <circle cx="60" cy="60" r={radius} fill="none"
                stroke="hsl(var(--border))" strokeWidth="8" />
              <circle cx="60" cy="60" r={radius} fill="none"
                stroke={gaugeColor} strokeWidth="8"
                strokeDasharray={circumference}
                strokeDashoffset={offset}
                strokeLinecap="round"
                className="transition-all duration-1000 ease-out"
                style={{ filter: `drop-shadow(0 0 6px ${gaugeColor}60)` }}
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className="text-3xl font-bold text-foreground">{score}</span>
              <span className="text-xs text-muted-foreground">/ 100</span>
            </div>
          </div>

          {/* Grade badge */}
          <span
            className="px-4 py-1.5 rounded-full text-sm font-semibold"
            style={{ background: gradeStyle.bg, color: gradeStyle.text, border: `1px solid ${gradeStyle.border}` }}
          >
            Grade {grade}
          </span>

          <p className="text-xs text-center text-muted-foreground max-w-[180px] leading-5">
            {verdict}
          </p>
        </div>

        {/* Breakdown bars */}
        <div className="flex-1 space-y-4 w-full">
          {breakdown.map((item, idx) => {
            const pct = Math.round((item.score / item.max) * 100);
            const color = barColor(pct);
            const glow  = barGlow(pct);
            return (
              <div key={idx}>
                <div className="flex justify-between items-baseline mb-1.5">
                  <span className="text-sm font-medium text-foreground">{item.label}</span>
                  <span className="text-xs text-muted-foreground font-mono">
                    {item.score} / {item.max}
                  </span>
                </div>

                {/* Track */}
                <div className="h-1.5 rounded-full overflow-hidden"
                  style={{ background: 'hsl(var(--muted))' }}>
                  <div
                    className="h-full rounded-full transition-all duration-700 ease-out"
                    style={{
                      width: `${pct}%`,
                      background: color,
                      boxShadow: pct > 0 ? `0 0 6px ${glow}` : 'none',
                    }}
                  />
                </div>

                {item.note && (
                  <p className="text-xs text-muted-foreground mt-1">{item.note}</p>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
