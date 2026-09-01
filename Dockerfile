# syntax=docker/dockerfile:1

# ---- Base ----------------------------------------------------------------
# Pinned major+minor, not just major, so a base image rebuild doesn't
# silently change Node's minor version under us.
FROM node:20.18-slim AS base
RUN npm install -g pnpm@9.12.0
WORKDIR /app

# ---- Dependencies ----------------------------------------------------------
# Cached separately from source so `pnpm install` only reruns when
# package.json / lockfile actually change, not on every code edit.
FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# ---- Build -----------------------------------------------------------------
FROM base AS build
COPY --from=deps /app/node_modules ./node_modules
COPY package.json pnpm-lock.yaml tsconfig.json ./
COPY src ./src
RUN pnpm build

# Install only production dependencies for the final stage.
RUN pnpm install --frozen-lockfile --prod

# ---- Runtime -----------------------------------------------------------------
FROM node:20.18-slim AS runtime
ENV NODE_ENV=production
WORKDIR /app

# Run as a non-root user; slim images ship a "node" user by default.
USER node

COPY --chown=node:node --from=build /app/node_modules ./node_modules
COPY --chown=node:node --from=build /app/dist ./dist
COPY --chown=node:node package.json ./

EXPOSE 3000

# Container-level health check independent of any orchestrator's own probe
# config, so `docker ps` and `docker inspect` reflect real service health.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:'+(process.env.PORT||3000)+'/health').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"

CMD ["node", "dist/server.js"]
