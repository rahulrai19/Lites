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
        # Simplistic routing: support OpenAI and Gemini
            
        try:
            async with httpx.AsyncClient() as client:
                if model.startswith("gemini") or "antigravity" in model or "deep-research" in model:
                    if not env.GEMINI_API_KEY:
                        return f"Error: GEMINI_API_KEY not set for model {model}"
                    
                    if env.GEMINI_API_KEY.startswith("AQ."):
                        return f"Mocked Gemini Response for: {prompt[:20]}... (Internal API Key)"
                        
                    response = await client.post(
                        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={env.GEMINI_API_KEY}",
                        headers={
                            "Content-Type": "application/json"
                        },
                        json={
                            "contents": [
                                {
                                    "parts": [{"text": prompt}]
                                }
                            ]
                        },
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return data["candidates"][0]["content"]["parts"][0]["text"]
                    else:
                        return f"Error from Gemini provider: {response.text}"
                else:
                    # Default to OpenAI
                    if not env.OPENAI_API_KEY:
                        return f"Mocked LLM Response for: {prompt[:20]}... (OpenAI API Key not set)"
                        
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
                        return f"Error from OpenAI provider: {response.text}"
        except Exception as e:
            return f"Failed to execute LLM request: {str(e)}"
