import OpenAI from 'openai';
import { ClientOptions } from 'openai';

export interface LitesClientOptions extends ClientOptions {
  /**
   * Optional context profile to guide the Lites optimization engine.
   * e.g. "code", "chat", "summarization"
   */
  litesContext?: string;
}

export class LitesClient extends OpenAI {
  private defaultLitesContext?: string;

  constructor(options: LitesClientOptions = {}) {
    // Override the default baseURL to point to the local Lites proxy
    const baseURL = options.baseURL || "http://localhost:8000/v1";
    
    super({
      ...options,
      baseURL
    });

    this.defaultLitesContext = options.litesContext;

    // Patch chat.completions.create to inject the X-Lites-Context header
    const originalCreate = this.chat.completions.create.bind(this.chat.completions);
    
    this.chat.completions.create = (async (body: any, options?: OpenAI.RequestOptions) => {
      const extraHeaders = {
        ...options?.headers,
      } as Record<string, string>;

      const litesContext = body.lites_context || this.defaultLitesContext;
      
      if (litesContext) {
        extraHeaders['X-Lites-Context'] = litesContext;
        delete body.lites_context;
      }

      const newOptions = {
        ...options,
        headers: Object.keys(extraHeaders).length > 0 ? extraHeaders : undefined
      };

      return originalCreate(body, newOptions);
    }) as any;
  }
}

export default LitesClient;
