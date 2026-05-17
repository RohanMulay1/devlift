'use client';

interface ArchitectureSectionProps {
  overview: string;
}

export default function ArchitectureSection({ overview }: ArchitectureSectionProps) {
  const paragraphs = overview
    .split(/\n\n+/)
    .map((p) => p.trim())
    .filter((p) => p.length > 0);

  return (
    <div className="space-y-5">
      {paragraphs.map((paragraph, idx) => (
        <p
          key={idx}
          className="text-base leading-8"
          style={{
            color: idx === 0
              ? 'hsl(var(--foreground))'
              : 'hsl(var(--muted-foreground))',
          }}
        >
          {paragraph}
        </p>
      ))}
    </div>
  );
}
