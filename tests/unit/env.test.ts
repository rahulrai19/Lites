import { beforeEach, describe, expect, it } from 'vitest';
import { loadEnv, __resetEnvCacheForTests } from '../../src/config/env.js';

describe('loadEnv', () => {
  beforeEach(() => {
    __resetEnvCacheForTests();
  });

  it('applies sensible defaults when optional vars are absent', () => {
    const env = loadEnv({});

    expect(env.NODE_ENV).toBe('development');
    expect(env.HOST).toBe('0.0.0.0');
    expect(env.PORT).toBe(3000);
    expect(env.LOG_LEVEL).toBe('info');
    expect(env.SHUTDOWN_TIMEOUT_MS).toBe(10_000);
  });

  it('coerces PORT from a string to a number', () => {
    const env = loadEnv({ PORT: '8080' });
    expect(env.PORT).toBe(8080);
    expect(typeof env.PORT).toBe('number');
  });

  it('throws on an invalid NODE_ENV rather than silently defaulting', () => {
    expect(() => loadEnv({ NODE_ENV: 'staging' })).toThrow(
      /Invalid environment configuration/,
    );
  });

  it('throws on a non-numeric PORT', () => {
    expect(() => loadEnv({ PORT: 'not-a-number' })).toThrow(
      /Invalid environment configuration/,
    );
  });

  it('memoizes the result across calls', () => {
    const first = loadEnv({ PORT: '4000' });
    const second = loadEnv({ PORT: '9999' });
    expect(second.PORT).toBe(first.PORT);
  });
});
