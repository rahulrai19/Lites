from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.env import env

security = HTTPBearer(auto_error=False)

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to verify the incoming Lites API key.
    If LITES_API_KEY is not set in the environment, the proxy is open.
    """
    if not env.LITES_API_KEY:
        return None
        
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authentication scheme.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if credentials.credentials != env.LITES_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return credentials.credentials
