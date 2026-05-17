'use client';

import { useEffect, useState } from 'react';

export default function RecommendingState() {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    const timer1 = setTimeout(() => setCurrentStep(1), 3000);
    const timer2 = setTimeout(() => setCurrentStep(2), 8000);
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, []);

  const steps = [
    { label: 'Understanding your requirements', icon: '🔍' },
    { label: 'Searching GitHub', icon: '🔎' },
    { label: 'Ranking matches', icon: '⭐' },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] space-y-8">
      {/* Spinning ring */}
      <div className="relative">
        <div
          className="w-12 h-12 rounded-full border-2 border-border animate-spin"
          style={{
            borderTopColor: '#0062FF',
          }}
        />
      </div>

      {/* Main text */}
      <div className="text-center space-y-2">
        <h2 className="text-xl font-semibold text-foreground">
          Finding the best repos for your requirements...
        </h2>
        <p className="text-sm text-muted-foreground">
          This usually takes 10–20 seconds
        </p>
      </div>

      {/* Progress steps */}
      <div className="space-y-3 w-full max-w-md">
        {steps.map((step, idx) => {
          const isComplete = idx < currentStep;
          const isCurrent = idx === currentStep;
          const isPending = idx > currentStep;

          return (
            <div key={idx} className="flex items-center gap-3">
              <div className="flex-shrink-0 w-6 h-6 flex items-center justify-center">
                {isComplete && (
                  <span className="text-green-400">✓</span>
                )}
                {isCurrent && (
                  <div
                    className="w-2 h-2 rounded-full animate-spin"
                    style={{ background: '#0062FF' }}
                  />
                )}
                {isPending && (
                  <span className="text-muted-foreground">○</span>
                )}
              </div>
              <span
                className={`text-sm ${
                  isComplete || isCurrent
                    ? 'text-foreground'
                    : 'text-muted-foreground'
                }`}
              >
                {step.icon} {step.label}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// Made with Bob