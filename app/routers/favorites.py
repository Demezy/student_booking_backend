import requests
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ..constants import API_BASE
from ..dependencies import get_token_from_header

router = APIRouter(prefix='/favorites')

@router.get("/dormitories/", response_model=List[str])
def get_starred_dormitory(token: str = Depends(get_token_from_header)):
    r = requests.get(f"{API_BASE}/me", headers={
        'Authorization': token
    })
    me = r.json()

    return me['starredDormitories']

@router.put("/dormitories/{dormitoryId}")
def add_dormitory(dormitoryId: str, token: str = Depends(get_token_from_header)):
    r = requests.get(f"{API_BASE}/me", headers={
        'Authorization': token
    })
    me = r.json()

    if 'id' not in me:
        raise HTTPException(403, 'Forbidden')

    me['starredDormitories'].append(dormitoryId)

    r = requests.put(f"{API_BASE}/users", json=me, headers={
        'Authorization': token
    })

@router.delete("/dormitories/{dormitoryId}")
def remove_dormitory(dormitoryId: str, token: str = Depends(get_token_from_header)):
    r = requests.get(f"{API_BASE}/me", headers={
        'Authorization': token
    })
    me = r.json()

    if 'id' not in me:
        raise HTTPException(403, 'Forbidden')

    newStarred = [dormitory for dormitory in me['starredDormitories'] if dormitory != dormitoryId]
    me['starredDormitories'] = newStarred

    r = requests.put(f"{API_BASE}/users", json=me, headers={
        'Authorization': token
    })
