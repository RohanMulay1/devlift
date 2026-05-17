'use client';

import { KeyComponent } from '@/types/kit';

interface ComponentsSectionProps {
  components: KeyComponent[];
}

export default function ComponentsSection({ components }: ComponentsSectionProps) {
  return (
    <div className="divide-y" style={{ borderColor: 'hsl(var(--border))' }}>
      {components.map((component, idx) => (
        <div key={idx} className="flex gap-5 py-5 first:pt-0 last:pb-0">
          {/* Index */}
          <span
            className="text-sm font-mono font-bold flex-shrink-0 pt-0.5 w-6 text-right"
            style={{ color: '#0062FF', opacity: 0.4 }}
          >
            {String(idx + 1).padStart(2, '0')}
          </span>

          {/* Content */}
          <div className="min-w-0 space-y-1.5">
            <div className="flex items-baseline gap-2.5 flex-wrap">
              <span className="text-base font-semibold text-foreground">{component.name}</span>
              <code
                className="text-sm font-mono"
                style={{ color: 'hsl(var(--muted-foreground))' }}
              >
                {component.path}
              </code>
            </div>
            <p className="text-base leading-7" style={{ color: 'hsl(var(--muted-foreground))' }}>
              {component.description}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
