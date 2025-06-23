# Code Courtroom Frontend

This is the frontend for **Code Courtroom**, an AI-powered platform that simulates a courtroom environment for advanced code review, compliance, and optimization. The frontend is built with React, TypeScript, Vite, and Bun for a fast, modern development experience.

## Overview
- **Modern UI:** Built with React and Vite for fast development and hot module reloading.
- **TypeScript:** Ensures type safety and maintainability.
- **Bun:** Used for dependency management and running scripts.
- **Agent Avatars:** Visual representation of specialized AI agents (Judge, Prosecutor, Defendant, Compliance, Optimizer, Rewriter).
- **API Integration:** Communicates with the Python backend for agent orchestration and code analysis.

## Getting Started

### Prerequisites
- [Bun](https://bun.sh/) (recommended)
- Node.js 18+ (if not using Bun)

### Installation
1. Install dependencies:
   ```bash
   bun install
   # or, if you prefer npm
   npm install
   ```
2. Start the development server:
   ```bash
   bun run dev
   # or
   npm run dev
   ```
3. Open [http://localhost:5173](http://localhost:5173) in your browser.

## Project Structure
```
frontend/
├── public/           # Static assets and images
├── src/              # Source code
│   ├── components/   # UI components and agent avatars
│   ├── hooks/        # Custom React hooks
│   ├── lib/          # Utility functions
│   ├── pages/        # Page components
├── package.json      # Project metadata
├── bun.lock          # Bun lockfile
├── tsconfig.json     # TypeScript config
├── vite.config.ts    # Vite config
└── ...
```

## Linting & Formatting
- ESLint is configured for React and TypeScript.
- For stricter or type-aware linting, see `eslint.config.js` and consider enabling recommended or strict rules.

## Customization
- Update agent avatars and UI in `src/components/` and `public/` as needed.

---
*Part of the Code Courtroom project.*
