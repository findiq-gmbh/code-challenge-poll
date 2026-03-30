# Frontend

SvelteKit + Svelte 5 + TypeScript, styled with Tailwind CSS v4 and shadcn-svelte.

## Running

```bash
cp .env.example .env    # sets PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev             # development server with HMR on http://localhost:5173
```

For a production build:

```bash
npm run build
npm run preview         # preview the built app locally
```

## Environment variables

See `.env.example`. The app will not build without `PUBLIC_API_URL` — the build fails fast if it is missing rather than shipping a broken URL at runtime.

| Variable         | Default      | Description                                               |
| ---------------- | ------------ | --------------------------------------------------------- |
| `PUBLIC_API_URL` | _(required)_ | Base URL of the backend API, e.g. `http://localhost:8000` |

## Structure

```
src/
├── app.html                  # HTML shell; dark-mode class applied here by mode-watcher
├── app.css                   # Tailwind v4 entry; qrafthive theme tokens; view-transition keyframes
├── lib/
│   ├── utils.ts              # cn() helper (clsx + tailwind-merge)
│   └── components/ui/        # shadcn-svelte components (Button, Card, Badge, Sonner)
└── routes/
    ├── +layout.svelte        # ModeWatcher, loading bar, view transitions, Toaster
    ├── Header.svelte         # Nav links, dark/light toggle (mode-watcher)
    ├── models.ts             # Shared TypeScript interfaces (Question, Answer)
    ├── +page.svelte          # Landing page
    ├── questions/
    │   ├── +page.ts          # load: GET /questions/
    │   └── +page.svelte      # Create question form + question list
    ├── answers/[id]/
    │   ├── +page.ts          # load: GET /questions/{id}, GET /questions/{id}/answers, POST /questions/{id}/visit
    │   └── +page.svelte      # Submit answer form + answer list
    └── visits/
        ├── +page.ts          # load: GET /visits/
        └── +page.svelte      # Questions ranked by visit count
```

## Playwright

Playwright is listed as a dev dependency but its browsers must be installed separately:

```bash
npx playwright install
```

To also install system-level dependencies (required on Linux CI):

```bash
npx playwright install --with-deps
```

## Useful commands

```bash
npm run check       # svelte-check type checking
npm run lint        # prettier + eslint
npm run format      # prettier --write
npm run test        # vitest (unit tests)
```
