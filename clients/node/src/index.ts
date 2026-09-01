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
  }

  // Intercept the chat.completions.create to inject the X-Lites-Context header
  override chat = {
    ...this.chat,
    completions: {
      ...this.chat.completions,
      create: async (body: OpenAI.Chat.ChatCompletionCreateParamsNonStreaming | OpenAI.Chat.ChatCompletionCreateParamsStreaming, options?: OpenAI.RequestOptions) => {
        const extraHeaders = {
          ...options?.headers,
        } as Record<string, string>;

        // Try to grab lites_context from the body (if passed implicitly) or default
        // We typecast body as any here to allow users to pass lites_context in the body if they want
        const reqBody = body as any;
        const litesContext = reqBody.lites_context || this.defaultLitesContext;
        
        if (litesContext) {
          extraHeaders['X-Lites-Context'] = litesContext;
          // Remove it from body so OpenAI doesn't complain about unknown parameter
          delete reqBody.lites_context;
        }

        const newOptions = {
          ...options,
          headers: Object.keys(extraHeaders).length > 0 ? extraHeaders : undefined
        };

        return super.chat.completions.create(reqBody, newOptions);
      }
    }
  };
}

export default LitesClient;
