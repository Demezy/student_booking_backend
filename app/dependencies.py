from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

def get_token_from_header(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return credentials.credentials
