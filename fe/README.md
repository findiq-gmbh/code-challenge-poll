# Frontend - Svelte Application

Svelte frontend TypeScript support.

## Prerequisites

- Node.js 18 or higher
- npm (comes with Node.js)


## Quick Start

Navigate to the frontend directory
```bash
cd fe
```

Install dependencies
```bash
npm ci
```

Start the development server
```bash
npm run dev
```
OR
```bash
npm run dev -- --open
```

### Access the application
   - **Frontend:** http://localhost:5173


## Routes

- **`/`** - Home page with navigation links
- **`/questions`** - Create new questions and view all questions
- **`/question/[id]/answers`** - View and create answers for a specific question
- **`/questions/visits`** - Analytics page showing visit statistics
