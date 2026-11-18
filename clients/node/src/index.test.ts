import { describe, it, expect, vi } from 'vitest';
import { LitesClient } from './index';

describe('Lites SDK - Node.js', () => {
  it('should initialize with default Lites configurations', () => {
    const client = new LitesClient({ apiKey: 'test-key' });
    
    // Should automatically set the baseURL to the Lites proxy
    expect(client.baseURL).toBe('http://localhost:8000/v1');
    expect(client.apiKey).toBe('test-key');
  });

  it('should respect custom configuration and provider overrides', () => {
    const client = new LitesClient({
      baseURL: 'https://my-lites-server.com/v1',
      apiKey: 'custom-key',
      litesContext: 'chat'
    });
    
    expect(client.baseURL).toBe('https://my-lites-server.com/v1');
    expect(client.apiKey).toBe('custom-key');
  });

  it('should inject X-Lites-Context header dynamically on normal requests', async () => {
    const client = new LitesClient({ apiKey: 'test-key', litesContext: 'code' });
    
    // We will mock the underlying OpenAI fetch implementation to verify headers are injected
    const fetchSpy = vi.spyOn(client as any, 'buildRequest');

    try {
      // This will fail because it's not a real network, but we just want to intercept the buildRequest
      await client.chat.completions.create({
        model: 'gpt-4',
        messages: [{ role: 'user', content: 'hello' }]
      });
    } catch (e) {
      // Ignore network errors
    }

    // Verify the buildRequest was called
    expect(fetchSpy).toHaveBeenCalled();
    const requestArgs = fetchSpy.mock.calls[0][0];
    
    // Check headers
    expect(requestArgs.headers).toBeDefined();
    expect(requestArgs.headers['X-Lites-Context']).toBe('code');
  });

  it('should allow overriding Lites context on a per-request basis', async () => {
    const client = new LitesClient({ apiKey: 'test-key', litesContext: 'code' });
    
    const fetchSpy = vi.spyOn(client as any, 'buildRequest');

    try {
      await client.chat.completions.create({
        model: 'gpt-4',
        messages: [{ role: 'user', content: 'hello' }],
        // @ts-ignore - OpenAI types don't know about lites_context, but our wrapper does
        lites_context: 'creative' 
      });
    } catch (e) {}

    const requestArgs = fetchSpy.mock.calls[0][0];
    
    // Per-request context should override the client default
    expect(requestArgs.headers['X-Lites-Context']).toBe('creative');
    // It should strip the custom parameter from the body
    expect(requestArgs.body).toBeDefined();
    expect(requestArgs.body.lites_context).toBeUndefined();
  });

  it('should propagate errors accurately on invalid requests', async () => {
    // Deliberately use a bad URL that will refuse connection
    const client = new LitesClient({ baseURL: 'http://localhost:11111/v1', apiKey: 'test-key' });
    
    await expect(client.chat.completions.create({
      model: 'gpt-4',
      messages: [{ role: 'user', content: 'fail' }]
    })).rejects.toThrow();
  });
});
