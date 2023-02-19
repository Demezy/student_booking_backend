import json
import os
import requests
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import FileResponse

from ..constants import API_BASE, AVATARS_DIRECTORY
from ..dependencies import get_token_from_header

if not os.path.exists(AVATARS_DIRECTORY):
    os.mkdir(AVATARS_DIRECTORY)

router = APIRouter(prefix='/avatars')

@router.get('/{id}')
def get_avatar(id: str):
    avatar_path = os.path.join(AVATARS_DIRECTORY, id)
    if not os.path.exists(avatar_path):
        raise HTTPException(404, 'No avatar found for user')

    return FileResponse(avatar_path, media_type='application/json')

@router.post('/{id}')
def upload_avatar(id: str, body: dict = Body(...), token: str = Depends(get_token_from_header)):
    r = requests.get(f"{API_BASE}/me", headers={
        'Authorization': token
    })
    me = r.json()

    if 'id' not in me or me['id'] != id:
        raise HTTPException(403, 'Forbidden')

    with open(os.path.join(AVATARS_DIRECTORY, id), 'w') as avatar:
        avatar.write(json.dumps(body))
    
    return { 'status': 'ok' }
