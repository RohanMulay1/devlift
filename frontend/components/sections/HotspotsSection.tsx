'use client';

import { ComplexityHotspot } from '@/types/kit';

interface HotspotsSectionProps {
  hotspots: ComplexityHotspot[];
}

export default function HotspotsSection({ hotspots }: HotspotsSectionProps) {
  return (
    <div className="divide-y" style={{ borderColor: 'hsl(var(--border))' }}>
      {hotspots.map((hotspot, idx) => (
        <div key={idx} className="py-5 first:pt-0 last:pb-0 space-y-3">
          {/* Name + path */}
          <div className="flex items-start gap-2.5">
            <span className="flex-shrink-0 mt-1 text-sm" style={{ color: 'rgb(234,179,8)' }}>▲</span>
            <div>
              <span className="text-base font-semibold text-foreground">{hotspot.name}</span>
              <code
                className="ml-2.5 text-sm font-mono"
                style={{ color: 'hsl(var(--muted-foreground))' }}
              >
                {hotspot.path}
              </code>
            </div>
          </div>

          {/* Why */}
          <p className="text-base leading-7 pl-6" style={{ color: 'hsl(var(--muted-foreground))' }}>
            {hotspot.reason}
          </p>

          {/* Tip */}
          <div className="pl-6 flex gap-2 items-start">
            <span className="flex-shrink-0 mt-1 text-sm" style={{ color: '#0062FF' }}>→</span>
            <p className="text-sm leading-6" style={{ color: 'hsl(var(--foreground))', opacity: 0.55 }}>
              {hotspot.tip}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
