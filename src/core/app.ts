import Fastify, { LogController, type FastifyInstance } from 'fastify';
import type { Env } from '../config/env.js';
import { registerHealthRoutes } from './health.js';

export interface BuildAppOptions {
  env: Env;
}

/**
 * Fastify 5 moved per-request logging control off the top-level options and
 * onto a LogController you can subclass. Here we just suppress the noisy
 * incoming/completed lines for the test environment and for the health-check
 * endpoint (a load balancer or orchestrator can hit /health every few
 * seconds — that shouldn't flood real logs).
 */
class LitesLogController extends LogController {
  constructor(env: Env) {
    super({
      disableRequestLogging: (request) =>
        env.NODE_ENV === 'test' || request.url === '/health',
    });
  }
}

/**
 * Builds and configures the Fastify instance. Does NOT call `.listen()` —
 * that lives in server.ts. Keeping construction separate from binding a port
 * means tests can exercise real routes via `app.inject()` without opening a
 * socket, and the same app can later be reused by alternative entry points
 * (e.g. a test harness, or a serverless adapter) if ever needed.
 */
export function buildApp(options: BuildAppOptions): FastifyInstance {
  const { env } = options;

  const app = Fastify({
    logger: {
      level: env.LOG_LEVEL,
    },
    logController: new LitesLogController(env),
  });

  registerHealthRoutes(app);

  return app;
}
