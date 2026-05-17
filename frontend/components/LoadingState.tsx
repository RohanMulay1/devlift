'use client';

import { useEffect, useState } from 'react';

export default function LoadingState() {
  const [currentStep, setCurrentStep] = useState(0);

  const steps = [
    'Fetching repository files',
    'Reading code with IBM watsonx.ai',
    'Building your onboarding kit',
    'Done',
  ];

  const progressWidths = [0, 20, 50, 80, 100];

  useEffect(() => {
    const timings = [10000, 25000, 60000]; // ms to advance each step
    let step = 0;
    const timers: ReturnType<typeof setTimeout>[] = [];

    timings.forEach((delay) => {
      timers.push(setTimeout(() => {
        step += 1;
        setCurrentStep(step);
      }, delay));
    });

    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-80 space-y-8 text-center">
        {/* Spinner */}
        <div className="mx-auto w-12 h-12 rounded-full border-[3px] border-border animate-spin-smooth"
          style={{
            borderTopColor: '#0062FF'
          }}
        />

        {/* Status text */}
        <p className="text-lg font-medium text-foreground">
          Analyzing repository with IBM watsonx.ai...
        </p>

        {/* Steps - left aligned */}
        <div className="space-y-3 text-left">
          {steps.map((step, idx) => (
            <div
              key={idx}
              className={`flex items-center gap-3 text-sm ${
                idx === currentStep
                  ? 'text-foreground font-medium'
                  : idx < currentStep
                  ? 'text-muted-foreground line-through'
                  : 'text-muted-foreground/40'
              }`}
            >
              {idx < currentStep ? (
                <span className="text-green-500">✓</span>
              ) : idx === currentStep ? (
                <div 
                  className="w-4 h-4 rounded-full border-2 animate-spin-smooth"
                  style={{
                    borderColor: 'hsl(var(--border))',
                    borderTopColor: '#0062FF'
                  }}
                />
              ) : (
                <span className="text-muted-foreground/40">○</span>
              )}
              <span>{step}</span>
            </div>
          ))}
        </div>

        {/* Progress bar */}
        <div className="w-full">
          <div className="h-1 bg-muted rounded-full overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-700 ease-in-out"
              style={{
                background: '#0062FF',
                width: `${progressWidths[currentStep]}%`
              }}
            />
          </div>
        </div>

        {/* Footer note */}
        <p className="text-xs text-muted-foreground">
          This usually takes 60–90 seconds
        </p>
      </div>
    </div>
  );
}

// Made with Bob
