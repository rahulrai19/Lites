import { beforeEach, describe, expect, it } from 'vitest';
import { buildApp } from '../../src/core/app.js';
import { loadEnv, __resetEnvCacheForTests } from '../../src/config/env.js';
import type { HealthResponse } from '../../src/core/health.js';

describe('GET /health', () => {
  beforeEach(() => {
    __resetEnvCacheForTests();
  });

  it('returns 200 with an ok status body', async () => {
    const env = loadEnv({ NODE_ENV: 'test', LOG_LEVEL: 'silent' });
    const app = buildApp({ env });

    const response = await app.inject({ method: 'GET', url: '/health' });

    expect(response.statusCode).toBe(200);

    const body = response.json<HealthResponse>();
    expect(body.status).toBe('ok');
    expect(typeof body.uptimeSeconds).toBe('number');
    expect(typeof body.version).toBe('string');
    expect(typeof body.timestamp).toBe('string');

    await app.close();
  });

  it('returns a valid ISO timestamp', async () => {
    const env = loadEnv({ NODE_ENV: 'test', LOG_LEVEL: 'silent' });
    const app = buildApp({ env });

    const response = await app.inject({ method: 'GET', url: '/health' });
    const body = response.json<HealthResponse>();

    expect(() => new Date(body.timestamp).toISOString()).not.toThrow();

    await app.close();
  });
});
