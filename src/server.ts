import { loadEnv } from './config/env.js';
import { buildApp } from './core/app.js';

const env = loadEnv();
const app = buildApp({ env });

let shuttingDown = false;

/**
 * Container orchestrators (Docker, Fly.io, Kubernetes, ECS...) send SIGTERM
 * before killing a container and expect the process to stop accepting new
 * connections, finish in-flight requests, then exit — all within a grace
 * period. Failing to handle this means dropped requests on every deploy or
 * scale-down. This is deliberately part of Phase 0, not an afterthought.
 */
async function shutdown(signal: string): Promise<void> {
  if (shuttingDown) {
    return;
  }
  shuttingDown = true;

  app.log.info({ signal }, 'Received shutdown signal, closing server');

  const forceExitTimer = setTimeout(() => {
    app.log.error('Graceful shutdown timed out, forcing exit');
    process.exit(1);
  }, env.SHUTDOWN_TIMEOUT_MS);
  forceExitTimer.unref();

  try {
    await app.close();
    clearTimeout(forceExitTimer);
    app.log.info('Server closed cleanly');
    process.exit(0);
  } catch (err) {
    app.log.error({ err }, 'Error during shutdown');
    process.exit(1);
  }
}

process.on('SIGTERM', () => void shutdown('SIGTERM'));
process.on('SIGINT', () => void shutdown('SIGINT'));

process.on('unhandledRejection', (reason) => {
  app.log.error({ reason }, 'Unhandled promise rejection');
});

async function start(): Promise<void> {
  try {
    await app.listen({ host: env.HOST, port: env.PORT });
  } catch (err) {
    app.log.error({ err }, 'Failed to start server');
    process.exit(1);
  }
}

void start();
