import type { Metadata } from 'next';
import { GeistMono } from 'geist/font/mono';
import './globals.css';

export const metadata: Metadata = {
  title: 'DevLift - Understand any codebase in 60 seconds',
  description: 'Paste a GitHub URL. Get an AI-generated onboarding kit. Powered by IBM watsonx.ai.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${GeistMono.variable} dark`}>
      <body>
        <div aria-hidden="true" className="gradient-bg">
          <span className="gradient-orb-3"></span>
        </div>
        {children}
      </body>
    </html>
  );
}

// Made with Bob
