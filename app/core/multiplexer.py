import httpx
from typing import Optional
from app.core.client import LLMClient
from app.config.env import env
from app.core.exceptions import (
    ProviderError,
    ProviderTimeoutError,
    ProviderAuthenticationError,
    ProviderRateLimitError,
    ProviderMalformedResponseError,
    ProviderEmptyResponseError
)

def _handle_response_status(response: httpx.Response, provider: str):
    if response.status_code == 401 or response.status_code == 403:
        raise ProviderAuthenticationError(provider)
    if response.status_code == 429:
        raise ProviderRateLimitError(provider)
    if response.status_code != 200:
        raise ProviderError(f"Error from {provider}: {response.text}", provider, response.status_code)

class HTTPMultiplexer(LLMClient):
    """
    A multiplexing client that routes requests to the correct LLM provider
    based on the model name. Currently supports OpenAI and Gemini models.
    """
    async def execute(self, prompt: str, model: str) -> str:
        provider_name = "gemini" if model.startswith("gemini") or "antigravity" in model or "deep-research" in model else "openai"
        
        try:
            async with httpx.AsyncClient() as client:
                if provider_name == "gemini":
                    if not env.GEMINI_API_KEY:
                        raise ProviderAuthenticationError("gemini")
                        
                    response = await client.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={env.GEMINI_API_KEY}",
                        headers={"Content-Type": "application/json"},
                        json={"contents": [{"parts": [{"text": prompt}]}]},
                        timeout=30.0
                    )
                    _handle_response_status(response, "gemini")
                    
                    try:
                        data = response.json()
                        text = data["candidates"][0]["content"]["parts"][0]["text"]
                        if not text.strip():
                            raise ProviderEmptyResponseError("gemini")
                        return text
                    except (ValueError, KeyError, IndexError) as e:
                        raise ProviderMalformedResponseError("gemini", str(e))
                else:
                    if not env.OPENAI_API_KEY:
                        raise ProviderAuthenticationError("openai")
                        
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {env.OPENAI_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": model,
                            "messages": [{"role": "user", "content": prompt}]
                        },
                        timeout=30.0
                    )
                    _handle_response_status(response, "openai")
                    
                    try:
                        data = response.json()
                        text = data["choices"][0]["message"]["content"]
                        if not text.strip():
                            raise ProviderEmptyResponseError("openai")
                        return text
                    except (ValueError, KeyError, IndexError) as e:
                        raise ProviderMalformedResponseError("openai", str(e))
        except httpx.TimeoutException:
            raise ProviderTimeoutError(provider_name)
        except httpx.RequestError as e:
            raise ProviderError(f"Network error contacting {provider_name}: {str(e)}", provider_name, 502)
