# Repository Guidelines

## Project Structure & Module Organization

This repository is split into a Python backend and a Next.js frontend. Backend code lives in `backend/app/`: routers in `api/`, models in `models/`, schemas in `schemas/`, business logic in `services/`, and settings/security helpers in `core/`. Alembic migrations are in `backend/alembic/versions/`. Frontend code lives in `frontend/src/`: route pages in `app/`, components in `components/`, helpers in `lib/`, and global styles in `styles/` or `app/globals.css`. Documentation is in `docs/`; deployment uses root compose and nginx files.

## Build, Test, and Development Commands

- `cp .env.example .env`: create local configuration before starting services.
- `docker compose up -d --build`: build and run the production-style stack.
- `docker compose -f docker-compose.dev.yml up -d --build`: run the development stack.
- `cd frontend && pnpm install && pnpm dev`: install dependencies and start Next.js.
- `cd frontend && pnpm build`: verify the Next.js production build.
- `cd frontend && pnpm lint`: run Next/TypeScript linting.
- `cd backend && pip install -r requirements.txt`: install backend dependencies.
- `cd backend && uvicorn app.main:app --reload`: run the API locally when dependent services are available.

## Coding Style & Naming Conventions

Follow PEP 8 for Python: 4-space indentation, `snake_case` functions/modules, typed schemas, and clear router/service/persistence boundaries. Frontend code uses strict TypeScript, path alias `@/*`, 2-space indentation, `PascalCase` components, and `camelCase` variables. Prefer existing shadcn/Radix UI patterns, Tailwind utilities, and helpers such as `cn()` in `frontend/src/lib/utils.ts`.

## Testing Guidelines

There is no dedicated unit test suite checked in. CI validates the Docker stack with `docker compose up -d`, then probes `/` and `/api/health`. For changes, run `pnpm lint` and `pnpm build` for frontend work, and start the compose stack plus check `http://localhost:80/api/health` for backend or integration changes. Add focused tests when introducing test infrastructure; use `test_*.py` for Python and `*.test.ts(x)` for frontend tests.

## Commit & Pull Request Guidelines

Recent history uses Conventional Commits such as `fix: ...`, `docs: ...`, `ci: ...`, `refactor: ...`, and scoped forms like `fix(security): ...`. Keep commits concise and imperative. Pull requests should include a description, linked issue when available, configuration or migration notes, verification commands, and screenshots for UI changes.

## Security & Configuration Tips

Do not commit real secrets. Keep local credentials in `.env`, update `.env.example` when adding required variables, and document any new external services. Be careful with migrations and startup behavior: `backend/app/main.py` runs database migrations on application startup.
