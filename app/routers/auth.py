import requests
from fastapi import APIRouter, Depends, HTTPException

from ..constants import API_BASE
from ..schemas.auth import APILogin, APIRegsiter, APIToken, APIUser
from ..dependencies import get_token_from_header

router = APIRouter(prefix='/auth')

@router.post("/login", response_model=APIToken)
def login(data: APILogin):
    r = requests.post(f"{API_BASE}/users/login", json=data.dict())
    auth = r.json()

    if 'token' not in auth:
        raise HTTPException(403, auth['message'])

    return auth

@router.post("/register", response_model=APIToken)
def register(data: APIRegsiter):
    r = requests.post(f"{API_BASE}/users/signup", json=data.dict())
    auth = r.json()

    if 'token' not in auth:
        raise HTTPException(403, auth['message'])

    r = requests.put(f"{API_BASE}/users", json=data.dict(), headers={
        'Authorization': auth['token']
    })

    return auth

@router.get("/me", response_model=APIUser)
def me(token: str = Depends(get_token_from_header)):
    r = requests.get(f"{API_BASE}/me", headers={
        'Authorization': token
    })
    me = r.json()

    if 'id' not in me:
        raise HTTPException(403, me['message'])

    return me
