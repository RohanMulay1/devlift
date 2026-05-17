<div align="center">

# DevLift

### AI-Powered Developer Onboarding Accelerator

**Understand any codebase in 60 seconds**

[![Built with IBM watsonx.ai](https://img.shields.io/badge/Built%20with-IBM%20watsonx.ai-0062FF?style=for-the-badge&logo=ibm)](https://www.ibm.com/watsonx)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

[Live Demo](#) • [Documentation](#running-locally) • [IBM Bob Hackathon](https://ibm.biz/bob-hackathon)

</div>

---

## 🎯 Overview

DevLift eliminates the costly 1-3 week onboarding period when developers join new projects. By leveraging IBM watsonx.ai's Llama 3.3 70B model, DevLift analyzes any public GitHub repository and generates a comprehensive **Onboarding Kit** in under 90 seconds.

### The Problem

- **Time Lost:** New developers spend 1-3 weeks understanding unfamiliar codebases
- **Cost Impact:** Industry estimates put onboarding costs at $15,000-$30,000 per engineer per project
- **Knowledge Gap:** README files are incomplete, wikis are stale, and asking teammates wastes senior engineer time

### The Solution

DevLift provides instant, AI-generated onboarding documentation that gives developers exactly what they need to become productive immediately.

---

## ✨ Features

### 🔍 Dual-Mode Analysis

| Mode | Description | Use Case |
|------|-------------|----------|
| **Analyze Repository** | Paste any GitHub URL to get a complete onboarding kit | Joining an existing project |
| **Discover Repositories** | Describe your requirements to get curated repo recommendations | Finding the right tools/frameworks |

### 📋 Comprehensive Onboarding Kit

Each generated kit includes six critical sections:

1. **Architecture Overview**
   - High-level system design and component interactions
   - Data flow and request lifecycle
   - Technology stack breakdown

2. **Key Components Map**
   - 6-8 most important files ranked by significance
   - Purpose and responsibility of each component
   - Dependencies and relationships

3. **Complexity Hotspots**
   - Areas with high cognitive load or technical debt
   - Risk assessment and modification warnings
   - Actionable tips for safe navigation

4. **Suggested First Tasks**
   - Beginner-friendly contribution opportunities
   - Difficulty ratings (Easy/Medium/Hard)
   - Clear success criteria

5. **Common Patterns**
   - Code conventions and architectural patterns
   - Idioms and best practices used throughout
   - Real examples from the codebase

6. **Setup & Run Guide**
   - Prerequisites and dependencies
   - Step-by-step installation instructions
   - Commands to run and test locally

### 📊 Contribution Readiness Score

A proprietary 0-100 scoring system that evaluates repositories across five dimensions:

- **Documentation Quality** (0-20 points)
- **Test Coverage** (0-20 points)
- **CI/CD Automation** (0-20 points)
- **Code Complexity** (0-20 points)
- **Community Health** (0-20 points)

Scores are visualized with letter grades (A/B/C/D) and detailed breakdowns.

---

## 🏗️ Architecture

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 14 (App Router) | Server-side rendering, optimal performance |
| | TypeScript | Type safety and developer experience |
| | Tailwind CSS + shadcn/ui | Modern, accessible UI components |
| | Geist Mono | Professional monospace typography |
| **Backend** | FastAPI (Python 3.11+) | High-performance async API |
| | Uvicorn | ASGI server with WebSocket support |
| **AI Engine** | IBM watsonx.ai | Enterprise-grade AI platform |
| | Llama 3.3 70B Instruct | State-of-the-art language model |
| **Data Source** | GitHub REST API | Repository metadata and file contents |
| | PyGithub | Python wrapper for GitHub API |
| **Deployment** | Vercel | Frontend hosting with edge functions |
| | Railway | Backend hosting with auto-scaling |

### System Flow

```
┌─────────────┐
│   User      │
│  Interface  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│         Next.js Frontend                │
│  • Dual-mode input (URL/Requirements)  │
│  • Real-time progress tracking          │
│  • Interactive kit visualization        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│  • /analyze endpoint                    │
│  • /recommend endpoint                  │
│  • Request validation & error handling  │
└──────┬──────────────────────────────────┘
       │
       ├──────────────────┬─────────────────┐
       ▼                  ▼                 ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│   GitHub    │  │   watsonx.ai │  │  Recommender │
│     API     │  │    (Llama)   │  │    Engine    │
└─────────────┘  └──────────────┘  └──────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** >= 18.0.0
- **Python** >= 3.11
- **IBM Cloud Account** with watsonx.ai access ([Sign up](https://cloud.ibm.com/registration))
- **GitHub Personal Access Token** ([Create one](https://github.com/settings/tokens))

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/RohanMulay1/devlift.git
cd devlift
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create `backend/.env` file:

```env
# GitHub API (increases rate limit from 60 to 5,000 requests/hour)
GITHUB_TOKEN=your_github_personal_access_token

# IBM watsonx.ai credentials
WATSONX_API_KEY=your_ibm_cloud_api_key
WATSONX_PROJECT_ID=your_watsonx_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**Getting IBM watsonx.ai Credentials:**
1. Log in to [IBM Cloud](https://cloud.ibm.com/)
2. Navigate to **watsonx** > **Projects**
3. Create a new project or select existing
4. Copy the **Project ID** from project settings
5. Generate an **API Key** from IBM Cloud IAM

Start the backend server:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Backend will be available at `http://localhost:8000`

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

Create `frontend/.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Build and start the frontend:

```bash
npm run build
npm start
```

Frontend will be available at `http://localhost:3000`

### Quick Start Scripts (Windows)

```powershell
# Start backend
.\start-backend.ps1

# Start frontend (in a new terminal)
.\start-frontend.ps1
```

---

## 📡 API Reference

### `POST /analyze`

Analyzes a GitHub repository and generates a complete onboarding kit.

**Request:**
```json
{
  "repo_url": "https://github.com/owner/repository"
}
```

**Response:** (200 OK)
```json
{
  "owner": "owner",
  "repo": "repository",
  "description": "Repository description",
  "language": "Python",
  "stars": 12400,
  "forks": 890,
  "topics": ["api", "framework"],
  "files_analyzed": 18,
  "readiness": {
    "score": 85,
    "grade": "A",
    "breakdown": { ... }
  },
  "kit": {
    "architecture_overview": "...",
    "key_components": [...],
    "complexity_hotspots": [...],
    "suggested_first_tasks": [...],
    "common_patterns": [...],
    "setup_summary": { ... }
  }
}
```

**Typical Response Time:** 60-90 seconds

### `POST /recommend`

Recommends GitHub repositories based on natural language requirements.

**Request:**
```json
{
  "requirement": "I need a Python web framework with async support and good documentation for building REST APIs"
}
```

**Response:** (200 OK)
```json
{
  "suggestions": [
    {
      "owner": "tiangolo",
      "repo": "fastapi",
      "full_name": "tiangolo/fastapi",
      "description": "FastAPI framework, high performance...",
      "stars": 75000,
      "forks": 6300,
      "language": "Python",
      "url": "https://github.com/tiangolo/fastapi",
      "why": "FastAPI perfectly matches your requirements..."
    }
  ]
}
```

**Typical Response Time:** 15-25 seconds

### `GET /health`

Health check endpoint.

**Response:** (200 OK)
```json
{
  "status": "ok",
  "model": "meta-llama/llama-3-3-70b-instruct"
}
```

---

## 🤖 IBM Bob Integration

This project was developed entirely using **IBM Bob** as the AI development partner, demonstrating Bob's capabilities across the full software development lifecycle:

### Development Tasks Completed with Bob

1. **Project Scaffolding**
   - Generated FastAPI backend structure with proper async patterns
   - Created Next.js 14 App Router frontend with TypeScript configuration
   - Set up testing infrastructure and CI/CD templates

2. **Core Algorithm Development**
   - Designed the smart file selection algorithm for GitHub repositories
   - Implemented the contribution readiness scoring system
   - Built the two-stage recommendation engine (query extraction + ranking)

3. **Prompt Engineering**
   - Crafted the optimal prompt structure for onboarding kit generation
   - Tuned parameters for consistent JSON output from Llama 3.3
   - Developed fallback strategies for edge cases

4. **UI/UX Implementation**
   - Built responsive components with shadcn/ui design system
   - Implemented smooth state transitions and loading animations
   - Created accessible, keyboard-navigable interfaces

5. **Testing & Quality Assurance**
   - Generated comprehensive unit test suite
   - Wrote integration tests for API endpoints
   - Performed code reviews and refactoring suggestions

6. **Documentation**
   - Authored this README with professional formatting
   - Created inline code documentation
   - Generated API reference documentation

**Bob Session Report:** See `/bob-report/` directory for exported session transcripts and task breakdowns.

---

## 📁 Project Structure

```
devlift/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── github_fetcher.py          # Repository analysis & readiness scoring
│   ├── bob_client.py              # IBM watsonx.ai client wrapper
│   ├── prompt_builder.py          # Prompt construction for AI
│   ├── repo_recommender.py        # Two-stage recommendation engine
│   ├── requirements.txt           # Python dependencies
│   ├── .env.example               # Environment variable template
│   └── tests/
│       ├── test_github_fetcher.py
│       └── test_prompt_builder.py
├── frontend/
│   ├── app/
│   │   ├── page.tsx               # Main application page
│   │   ├── layout.tsx             # Root layout with metadata
│   │   └── globals.css            # Global styles & CSS variables
│   ├── components/
│   │   ├── HeroInput.tsx          # Dual-mode input interface
│   │   ├── LoadingState.tsx       # Analysis progress indicator
│   │   ├── RecommendingState.tsx  # Recommendation progress
│   │   ├── RecommendationResults.tsx  # Repository suggestions
│   │   ├── RepoHeader.tsx         # Repository metadata display
│   │   ├── ReadinessScore.tsx     # Score visualization
│   │   ├── KitTabs.tsx            # Tab navigation
│   │   ├── DownloadButton.tsx     # Markdown export
│   │   └── sections/              # Kit section components
│   ├── lib/
│   │   └── api.ts                 # Backend API client
│   ├── types/
│   │   └── kit.ts                 # TypeScript type definitions
│   ├── package.json
│   └── tailwind.config.ts
├── bob-report/                    # IBM Bob session exports
├── BOB_PRD.md                     # Product requirements document
├── README.md                      # This file
└── LICENSE
```

---

## 🎨 Design System

DevLift uses a custom design system built on shadcn/ui principles:

- **Color Palette:** Dark theme with IBM Blue (#0062FF) accents
- **Typography:** Geist Mono for consistent monospace rendering
- **Components:** Accessible, keyboard-navigable UI elements
- **Animations:** Subtle transitions and loading states
- **Responsive:** Mobile-first design with breakpoints at 640px, 768px, 1024px

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

---

## 🚢 Deployment

### Backend (Railway)

1. Push code to GitHub
2. Connect repository to [Railway](https://railway.app/)
3. Set environment variables in Railway dashboard
4. Deploy with automatic HTTPS

### Frontend (Vercel)

1. Push code to GitHub
2. Import project in [Vercel](https://vercel.com/)
3. Set `NEXT_PUBLIC_API_URL` environment variable
4. Deploy with automatic edge optimization

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IBM watsonx.ai** for providing the AI infrastructure
- **IBM Bob** for being an exceptional AI development partner
- **GitHub** for the comprehensive REST API
- **Vercel** and **Railway** for hosting platforms
- **shadcn/ui** for the component library

---

## 📞 Contact

**Rohan Mulay**

- GitHub: [@RohanMulay1](https://github.com/RohanMulay1)
- Project Link: [https://github.com/RohanMulay1/devlift](https://github.com/RohanMulay1/devlift)

---

<div align="center">

**Built with ❤️ for the IBM Bob Hackathon**

[⬆ Back to Top](#devlift)

</div>
