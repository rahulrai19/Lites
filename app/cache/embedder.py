import httpx
from typing import Optional, List
from app.config.env import env

class Embedder:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.model = model
        
    async def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Calls OpenAI to get the embedding vector for the text.
        Fails safely (returns None) if API key is missing or request fails.
        """
        if not env.OPENAI_API_KEY:
            return None
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.openai.com/v1/embeddings",
                    headers={
                        "Authorization": f"Bearer {env.OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "input": text,
                        "model": self.model
                    },
                    timeout=5.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data["data"][0]["embedding"]
        except Exception:
            pass
            
        return None
