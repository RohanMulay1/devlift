'use client';

import { useState } from 'react';

interface HeroInputProps {
  onSubmit: (url: string) => void;
  onRecommend: (requirement: string) => void;
  recentRepos: Array<{ url: string; repo: string; language: string }>;
}

type Mode = 'url' | 'desc';

const ACCENT = { url: '#0062FF', desc: '#7B2FFF' } as const;
const ACCENT_BG = { url: 'rgba(0,98,255,0.08)', desc: 'rgba(123,47,255,0.08)' } as const;
const ACCENT_GLOW = { url: 'rgba(0,98,255,0.18)', desc: 'rgba(123,47,255,0.18)' } as const;
const ACCENT_HOVER = { url: '#0053d6', desc: '#6822e0' } as const;

export default function HeroInput({ onSubmit, onRecommend, recentRepos }: HeroInputProps) {
  const [mode, setMode] = useState<Mode>('url');
  const [url, setUrl] = useState('');
  const [requirement, setRequirement] = useState('');
  const [error, setError] = useState('');

  const switchMode = (m: Mode) => { setMode(m); setError(''); };

  const handleUrlSubmit = () => {
    setError('');
    if (!url.trim()) { setError('Please enter a GitHub URL'); return; }
    if (!url.startsWith('https://github.com/')) { setError('Expected: https://github.com/owner/repo'); return; }
    onSubmit(url.trim());
  };

  const handleDescSubmit = () => {
    setError('');
    const t = requirement.trim();
    if (t.length < 20) { setError('Describe your requirement in at least 20 characters'); return; }
    onRecommend(t);
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 relative">
      {/* Top shimmer */}
      <div className="fixed top-0 left-0 right-0 h-[2px] animate-shimmer"
        style={{ background: 'linear-gradient(90deg,#0062FF,#7B2FFF,#0062FF)', backgroundSize: '200% 100%' }} />

      {/* Radial glow — color shifts with mode */}
      <div className="fixed inset-0 pointer-events-none transition-all duration-500"
        style={{
          background: mode === 'url'
            ? 'radial-gradient(ellipse 80% 40% at 50% -5%, rgba(0,98,255,0.13) 0%, transparent 70%)'
            : 'radial-gradient(ellipse 80% 40% at 50% -5%, rgba(123,47,255,0.13) 0%, transparent 70%)',
        }} />

      <div className="max-w-2xl w-full mx-auto relative z-10">

        {/* Logo — always same */}
        <div className="text-center mb-8">
          <h1 className="text-6xl font-bold tracking-tight mb-3 transition-all duration-500"
            style={{
              color: ACCENT[mode],
              textShadow: `0 0 60px ${ACCENT_GLOW[mode]}`,
            }}>
            DevLift
          </h1>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium border transition-all duration-500"
            style={{
              borderColor: `${ACCENT[mode]}55`,
              color: ACCENT[mode],
              background: ACCENT_BG[mode],
            }}>
            Powered by IBM watsonx.ai
          </div>
        </div>

        {/* Mode selector cards */}
        <div className="grid grid-cols-2 gap-3 mb-6">
          {(['url', 'desc'] as const).map((m) => {
            const active = mode === m;
            const labels = { url: { icon: '🔗', title: 'Analyze a repo', desc: 'Paste any GitHub URL — get a full AI-generated onboarding kit in 60 seconds.' },
                            desc: { icon: '✦', title: 'Discover repos', desc: 'Describe your project or stack and get the best open-source repos matched to your needs.' } };
            return (
              <button
                key={m}
                type="button"
                onClick={() => switchMode(m)}
                className="text-left p-4 rounded-xl border transition-all duration-300"
                style={{
                  background: active ? ACCENT_BG[m] : 'hsl(var(--card))',
                  borderColor: active ? ACCENT[m] : 'hsl(var(--border))',
                  boxShadow: active ? `0 0 24px ${ACCENT_GLOW[m]}` : 'none',
                  transform: active ? 'translateY(-1px)' : 'translateY(0)',
                }}
              >
                <div className="flex items-center gap-2 mb-1.5">
                  <span className="text-sm">{labels[m].icon}</span>
                  <span className="text-sm font-semibold transition-colors duration-300"
                    style={{ color: active ? ACCENT[m] : 'hsl(var(--foreground))' }}>
                    {labels[m].title}
                  </span>
                  <span
                    className="ml-auto text-xs px-1.5 py-0.5 rounded font-medium transition-all duration-300"
                    style={{
                      opacity: active ? 1 : 0,
                      background: `${ACCENT[m]}22`,
                      color: ACCENT[m],
                    }}
                  >
                    active
                  </span>
                </div>
                <p className="text-xs leading-5 text-muted-foreground">{labels[m].desc}</p>
              </button>
            );
          })}
        </div>

        {/* Hero copy — fixed height, cross-fade */}
        <div className="relative text-center mb-5 overflow-hidden" style={{ height: '4.5rem' }}>
          {/* URL copy */}
          <div className="absolute inset-0 transition-all duration-300"
            style={{ opacity: mode === 'url' ? 1 : 0, transform: mode === 'url' ? 'translateY(0)' : 'translateY(-6px)', pointerEvents: mode === 'url' ? 'auto' : 'none' }}>
            <p className="text-xl font-semibold text-foreground">Understand any codebase in 60 seconds</p>
            <p className="text-sm text-muted-foreground mt-1.5">Paste a GitHub URL — get architecture, hotspots, tasks and a readiness score.</p>
          </div>
          {/* Desc copy */}
          <div className="absolute inset-0 transition-all duration-300"
            style={{ opacity: mode === 'desc' ? 1 : 0, transform: mode === 'desc' ? 'translateY(0)' : 'translateY(6px)', pointerEvents: mode === 'desc' ? 'auto' : 'none' }}>
            <p className="text-xl font-semibold text-foreground">Find the right open-source repo for your stack</p>
            <p className="text-sm text-muted-foreground mt-1.5">Describe what you're building — get curated repo matches with kits ready to go.</p>
          </div>
        </div>

        {/* Input area — fixed height container, both modes always rendered */}
        <div className="relative" style={{ minHeight: '132px' }}>
          {/* URL mode */}
          <div className="absolute inset-0 transition-all duration-300 flex flex-col gap-2"
            style={{ opacity: mode === 'url' ? 1 : 0, transform: mode === 'url' ? 'translateY(0)' : 'translateY(-8px)', pointerEvents: mode === 'url' ? 'auto' : 'none' }}>
            <div className="flex gap-2">
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') handleUrlSubmit(); }}
                placeholder="https://github.com/owner/repo"
                className="flex-1 px-4 py-3 rounded-lg bg-input border border-border text-foreground placeholder:text-muted-foreground focus:outline-none transition-colors duration-150"
                onFocus={(e) => e.target.style.borderColor = ACCENT.url}
                onBlur={(e) => e.target.style.borderColor = 'hsl(var(--border))'}
              />
              <button
                type="button"
                onClick={handleUrlSubmit}
                className="px-5 py-3 rounded-lg font-medium text-sm text-white transition-all duration-200 whitespace-nowrap"
                style={{ background: ACCENT.url, minWidth: '130px' }}
                onMouseEnter={(e) => e.currentTarget.style.background = ACCENT_HOVER.url}
                onMouseLeave={(e) => e.currentTarget.style.background = ACCENT.url}
              >
                Generate Kit →
              </button>
            </div>
          </div>

          {/* Desc mode */}
          <div className="absolute inset-0 transition-all duration-300 flex flex-col gap-2"
            style={{ opacity: mode === 'desc' ? 1 : 0, transform: mode === 'desc' ? 'translateY(0)' : 'translateY(8px)', pointerEvents: mode === 'desc' ? 'auto' : 'none' }}>
            <div className="relative">
              <textarea
                value={requirement}
                onChange={(e) => setRequirement(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) handleDescSubmit(); }}
                placeholder='e.g. "I need a Python web framework with async support and great docs for building REST APIs"'
                rows={3}
                className="w-full px-4 py-3 rounded-lg bg-input border border-border text-foreground placeholder:text-muted-foreground focus:outline-none transition-colors duration-150 resize-none"
                onFocus={(e) => e.target.style.borderColor = ACCENT.desc}
                onBlur={(e) => e.target.style.borderColor = 'hsl(var(--border))'}
              />
              <span className="absolute bottom-2.5 right-3 text-xs text-muted-foreground pointer-events-none">
                {requirement.length} / 2000
              </span>
            </div>
            <button
              type="button"
              onClick={handleDescSubmit}
              className="w-full py-3 rounded-lg font-medium text-sm text-white transition-all duration-200"
              style={{ background: ACCENT.desc }}
              onMouseEnter={(e) => e.currentTarget.style.background = ACCENT_HOVER.desc}
              onMouseLeave={(e) => e.currentTarget.style.background = ACCENT.desc}
            >
              Find Repos →
            </button>
          </div>
        </div>

        {/* Error — fade in below input */}
        <div className="transition-all duration-200 overflow-hidden mt-2"
          style={{ maxHeight: error ? '2rem' : '0', opacity: error ? 1 : 0 }}>
          <p className="text-sm" style={{ color: 'hsl(var(--destructive))' }}>{error}</p>
        </div>

        {/* Recent repos — fade in only in URL mode */}
        <div className="transition-all duration-300 overflow-hidden mt-4"
          style={{ maxHeight: mode === 'url' && recentRepos.length > 0 ? '80px' : '0', opacity: mode === 'url' && recentRepos.length > 0 ? 1 : 0 }}>
          <p className="text-xs text-muted-foreground mb-2">Recent:</p>
          <div className="flex flex-wrap gap-2">
            {recentRepos.map((repo, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => { setUrl(repo.url); setError(''); setMode('url'); }}
                className="px-3 py-1.5 rounded-md text-sm border border-border bg-secondary text-secondary-foreground transition-all duration-150"
                onMouseEnter={(e) => { e.currentTarget.style.borderColor = 'rgba(0,98,255,0.4)'; e.currentTarget.style.color = '#0062FF'; }}
                onMouseLeave={(e) => { e.currentTarget.style.borderColor = 'hsl(var(--border))'; e.currentTarget.style.color = 'hsl(var(--secondary-foreground))'; }}
              >
                {repo.repo}<span className="text-muted-foreground"> · {repo.language}</span>
              </button>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
