import type { FastifyInstance } from 'fastify';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Read the version once at module load rather than on every request.
function readPackageVersion(): string {
  try {
    const pkgPath = join(__dirname, '..', '..', 'package.json');
    const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8')) as { version?: string };
    return pkg.version ?? 'unknown';
  } catch {
    return 'unknown';
  }
}

const version = readPackageVersion();
const startedAt = Date.now();

export interface HealthResponse {
  status: 'ok';
  uptimeSeconds: number;
  version: string;
  timestamp: string;
}

/**
 * Phase 0 has no external dependencies (no cache, no provider, no DB), so a
 * single unconditional health endpoint is honest: the process being able to
 * respond IS the whole health story right now.
 *
 * Once Phase 4+ introduces real dependencies (cache backend, providers),
 * split this into /health/live (process up) and /health/ready (dependencies
 * reachable) rather than overloading this one route with checks it can't
 * yet perform. Documented here so the TODO doesn't get lost.
 */
export function registerHealthRoutes(app: FastifyInstance): void {
  app.get('/health', (): HealthResponse => {
    return {
      status: 'ok',
      uptimeSeconds: Math.floor((Date.now() - startedAt) / 1000),
      version,
      timestamp: new Date().toISOString(),
    };
  });
}
