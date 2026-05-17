'use client';

import { FirstTask } from '@/types/kit';

interface TasksSectionProps {
  tasks: FirstTask[];
}

const DIFFICULTY_CONFIG = {
  easy: {
    label: 'Easy',
    accent: 'rgb(74, 222, 128)',
    bg: 'rgba(34, 197, 94, 0.06)',
    border: 'rgba(34, 197, 94, 0.2)',
    dot: 'rgb(34, 197, 94)',
  },
  medium: {
    label: 'Medium',
    accent: 'rgb(250, 204, 21)',
    bg: 'rgba(234, 179, 8, 0.06)',
    border: 'rgba(234, 179, 8, 0.2)',
    dot: 'rgb(234, 179, 8)',
  },
  hard: {
    label: 'Hard',
    accent: 'rgb(248, 113, 113)',
    bg: 'rgba(239, 68, 68, 0.06)',
    border: 'rgba(239, 68, 68, 0.2)',
    dot: 'rgb(239, 68, 68)',
  },
} as const;

export default function TasksSection({ tasks }: TasksSectionProps) {
  const groups = (['easy', 'medium', 'hard'] as const).map((level) => ({
    level,
    config: DIFFICULTY_CONFIG[level],
    items: tasks.filter((t) => t.difficulty === level),
  })).filter((g) => g.items.length > 0);

  return (
    <div className="space-y-6">
      {groups.map(({ level, config, items }) => (
        <div key={level}>
          {/* Section header */}
          <div className="flex items-center gap-2 mb-3">
            <span
              className="w-2 h-2 rounded-full flex-shrink-0"
              style={{ background: config.dot }}
            />
            <span className="text-xs font-semibold uppercase tracking-widest"
              style={{ color: config.accent }}>
              {config.label}
            </span>
            <span className="text-xs text-muted-foreground">
              — {items.length} task{items.length > 1 ? 's' : ''}
            </span>
          </div>

          {/* Task rows */}
          <div
            className="rounded-lg overflow-hidden"
            style={{ border: `1px solid ${config.border}`, background: config.bg }}
          >
            {items.map((task, idx) => (
              <div
                key={idx}
                className={`flex items-start gap-4 px-4 py-3 ${
                  idx < items.length - 1 ? 'border-b' : ''
                }`}
                style={idx < items.length - 1 ? { borderColor: config.border } : {}}
              >
                {/* Step number */}
                <span
                  className="text-xs font-mono font-bold mt-0.5 flex-shrink-0 w-5 text-right"
                  style={{ color: config.accent, opacity: 0.7 }}
                >
                  {String(idx + 1).padStart(2, '0')}
                </span>

                {/* Content */}
                <div className="min-w-0">
                  <p className="text-sm font-medium text-foreground leading-snug">
                    {task.title}
                  </p>
                  <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                    {task.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
