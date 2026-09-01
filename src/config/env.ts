import { z } from 'zod';

/**
 * All runtime configuration for Lites is sourced from environment variables
 * and validated once, at startup, through this schema.
 *
 * Fail fast: if the environment is misconfigured, the process should refuse
 * to start rather than run in an unknown state. This matters especially in
 * containers, where a bad deploy should fail health checks immediately
 * instead of serving traffic in a broken configuration.
 */
const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),

  // Network
  HOST: z.string().default('0.0.0.0'),
  PORT: z.coerce.number().int().positive().default(3000),

  // Logging
  LOG_LEVEL: z.enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace', 'silent']).default('info'),

  // Graceful shutdown
  SHUTDOWN_TIMEOUT_MS: z.coerce.number().int().positive().default(10_000),

  // Reserved for later phases (providers, cache, routing). Kept optional and
  // unused for now so Phase 0 has no hidden dependency on external services.
  ANTHROPIC_API_KEY: z.string().optional(),
  OPENAI_API_KEY: z.string().optional(),
  REDIS_URL: z.string().optional(),
});

export type Env = z.infer<typeof envSchema>;

let cachedEnv: Env | undefined;

/**
 * Parses and validates `process.env` on first call, then returns the cached
 * result. Throws synchronously (crashing the process) if required variables
 * are missing or malformed — this is intentional for Phase 0.
 */
export function loadEnv(source: NodeJS.ProcessEnv = process.env): Env {
  if (cachedEnv) {
    return cachedEnv;
  }

  const parsed = envSchema.safeParse(source);

  if (!parsed.success) {
    const issues = parsed.error.issues
      .map((issue) => `  - ${issue.path.join('.')}: ${issue.message}`)
      .join('\n');
    throw new Error(`Invalid environment configuration:\n${issues}`);
  }

  cachedEnv = parsed.data;
  return cachedEnv;
}

/** Test-only escape hatch to reset the memoized config between test cases. */
export function __resetEnvCacheForTests(): void {
  cachedEnv = undefined;
}
