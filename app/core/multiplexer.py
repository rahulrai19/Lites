import httpx
from typing import Optional
from app.core.client import LLMClient
from app.config.env import env

class HTTPMultiplexer(LLMClient):
    """
    A multiplexing client that routes requests to the correct LLM provider
    based on the model name. Currently supports OpenAI models.
    """
    async def execute(self, prompt: str, model: str) -> str:
        # Simplistic routing: assume OpenAI for now unless prefixed.
        # In a real system, you'd map "claude-*" to Anthropic, etc.
        if not env.OPENAI_API_KEY:
            # For testing without a key, just echo
            return f"Mocked LLM Response for: {prompt[:20]}..."
            
        try:
            async with httpx.AsyncClient() as client:
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
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return f"Error from provider: {response.text}"
        except Exception as e:
            return f"Failed to execute LLM request: {str(e)}"
