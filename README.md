# Lites

Intelligent LLM token optimization middleware platform.

Lites sits between an application and an LLM provider to reduce unnecessary
token consumption without changing the user's intended meaning — prioritizing
deterministic optimization, and only reaching for AI-based optimization when
the expected savings justify the cost.

> **Status: Phase 0 — Foundation.** This repository currently contains only
> the project scaffold: a Fastify server, environment configuration, and a
> health-check endpoint. None of the optimization, caching, or routing
> functionality described in the architecture below is implemented yet. This
> README will be updated at the end of each phase to describe only what
> actually exists — see [Roadmap](#roadmap).

## Architecture (target)

```
Application
  -> Lites API / SDK
  -> Request Analyzer
  -> Token Counter
  -> Rule-Based Optimizer
  -> Context Compression
  -> AI Prompt Optimizer (optional)
  -> Cache Normalization
  -> Exact / Semantic Cache
  -> Adaptive Model Router
  -> LLM Provider
  -> Response
  -> Metrics
```

Core principle: **never optimize a prompt if the optimization costs more than
the expected savings.**

## Requirements

- Node.js >= 20
- pnpm >= 9 (`corepack enable` will fetch the pinned version automatically)

## Getting started

```bash
pnpm install
cp .env.example .env
pnpm dev
```

The server starts on `http://localhost:3000` by default. Check it's alive:

```bash
curl http://localhost:3000/health
```

## Scripts

| Command              | Description                                      |
| --------------------- | ------------------------------------------------- |
| `pnpm dev`            | Run the server with hot reload (tsx watch)        |
| `pnpm build`          | Compile TypeScript to `dist/`                      |
| `pnpm start`          | Run the compiled server from `dist/`               |
| `pnpm test`           | Run the test suite once                            |
| `pnpm test:watch`     | Run tests in watch mode                            |
| `pnpm test:coverage`  | Run tests with coverage                            |
| `pnpm typecheck`      | Type-check without emitting                        |
| `pnpm lint`           | Lint the codebase                                  |
| `pnpm lint:fix`       | Lint and auto-fix                                  |
| `pnpm format`         | Format source and test files with Prettier         |

## Configuration

All configuration is environment-variable based and validated at startup with
Zod (`src/config/env.ts`) — the process refuses to start if the environment is
invalid rather than running with silently-wrong config. See `.env.example`
for the full list of variables.

## Running with Docker

```bash
docker build -t lites .
docker run --rm -p 3000:3000 --env-file .env lites
```

or, for local development parity with the production image:

```bash
docker compose up --build
```

The image is a multi-stage build (deps → build → slim production runtime),
runs as a non-root user, and includes a container-level `HEALTHCHECK` against
`/health`.

## Project structure

```
lites/
├── src/
│   ├── core/        # Fastify app + health check (implemented)
│   ├── config/      # Environment validation (implemented)
│   ├── optimizer/    # Phase 2 — not yet implemented
│   ├── tokenizer/    # Phase 1 — not yet implemented
│   ├── cache/        # Phase 4 — not yet implemented
│   ├── context/      # Phase 6 — not yet implemented
│   ├── router/       # Phase 9 — not yet implemented
│   ├── providers/    # Phase 7 — not yet implemented
│   └── metrics/      # Phase 10 — not yet implemented
├── tests/
│   ├── unit/         # implemented
│   ├── integration/  # Phase 5+ — not yet implemented
│   └── benchmarks/   # Phase 10+ — not yet implemented
├── examples/
└── docs/
```

## Roadmap

Phase 0 (this repo, current) covers foundation only: project setup, config,
health check, and deployment scaffolding (Docker). Subsequent phases —
token counting, rule-based optimization, the optimization decision engine,
cache normalization, the full request pipeline, context management, AI
optimization, semantic caching, adaptive routing, metrics, the SDK, and a
CLI — are implemented incrementally, one at a time, each validated with
passing type checks and tests before moving to the next.

## License

MIT — see [LICENSE](./LICENSE).
