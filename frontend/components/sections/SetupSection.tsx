'use client';

import { SetupSummary } from '@/types/kit';
import { useState } from 'react';

interface SetupSectionProps {
  setup: SetupSummary;
}

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  return (
    <button
      onClick={() => {
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }}
      className="text-xs px-2.5 py-1.5 rounded-md transition-all duration-150 flex-shrink-0 font-medium"
      style={{
        background: copied ? 'rgba(34,197,94,0.12)' : 'rgba(0,98,255,0.1)',
        color: copied ? 'rgb(74,222,128)' : '#0062FF',
        border: copied ? '1px solid rgba(34,197,94,0.25)' : '1px solid rgba(0,98,255,0.2)',
      }}
    >
      {copied ? '✓ copied' : 'copy'}
    </button>
  );
}

function Label({ children }: { children: React.ReactNode }) {
  return (
    <p className="text-xs font-semibold uppercase tracking-widest mb-3"
      style={{ color: 'hsl(var(--muted-foreground))' }}>
      {children}
    </p>
  );
}

export default function SetupSection({ setup }: SetupSectionProps) {
  return (
    <div className="space-y-7">
      {/* Prerequisites */}
      {setup.prerequisites.length > 0 && (
        <div>
          <Label>Prerequisites</Label>
          <div className="flex flex-wrap gap-2">
            {setup.prerequisites.map((prereq, idx) => (
              <span
                key={idx}
                className="text-sm font-mono px-3 py-1.5 rounded-md"
                style={{
                  background: 'hsl(var(--muted))',
                  color: 'hsl(var(--foreground))',
                  border: '1px solid hsl(var(--border))',
                }}
              >
                {prereq}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Install steps */}
      {setup.install_steps.length > 0 && (
        <div>
          <Label>Installation</Label>
          <div className="space-y-3">
            {setup.install_steps.map((step, idx) => (
              <div key={idx} className="flex items-start gap-4">
                <span
                  className="text-sm font-mono font-bold flex-shrink-0 mt-0.5 w-5 text-right"
                  style={{ color: '#0062FF', opacity: 0.45 }}
                >
                  {idx + 1}.
                </span>
                <p className="text-base leading-7" style={{ color: 'hsl(var(--muted-foreground))' }}>
                  {step}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Run command */}
      {setup.run_command && (
        <div>
          <Label>Run</Label>
          <div className="flex items-center gap-3">
            <pre
              className="text-base font-mono flex-1 px-4 py-3 rounded-lg overflow-x-auto"
              style={{
                background: 'hsl(var(--muted))',
                color: 'hsl(var(--foreground))',
                border: '1px solid hsl(var(--border))',
              }}
            >
              {setup.run_command}
            </pre>
            <CopyButton text={setup.run_command} />
          </div>
        </div>
      )}

      {/* Test command */}
      {setup.test_command && (
        <div>
          <Label>Test</Label>
          <div className="flex items-center gap-3">
            <pre
              className="text-base font-mono flex-1 px-4 py-3 rounded-lg overflow-x-auto"
              style={{
                background: 'hsl(var(--muted))',
                color: 'hsl(var(--foreground))',
                border: '1px solid hsl(var(--border))',
              }}
            >
              {setup.test_command}
            </pre>
            <CopyButton text={setup.test_command} />
          </div>
        </div>
      )}

      {/* Notes */}
      {setup.notes && (
        <div>
          <Label>Notes</Label>
          <p className="text-base leading-7" style={{ color: 'hsl(var(--muted-foreground))' }}>
            {setup.notes}
          </p>
        </div>
      )}
    </div>
  );
}
