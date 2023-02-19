import requests
from typing import List
from fastapi import APIRouter, Depends, HTTPException

from ..constants import API_BASE
from ..dependencies import get_token_from_header
from ..schemas.dormitories import APIRoomBookingPayload, APIRoomBookingPreview, Dormitory, Room

router = APIRouter(prefix='/dormitories')

def fix_coord(coord):
    if type(coord) == float:
        return round(coord, 6)
    if type(coord) == str:
        return round(float(coord), 6)
    return round(float(coord['value']), 6)

def map_room(room):
    return Room(
        id=room['id'],
        description=room['details']['description'],
        type=room['details']['type'],
        price=int(room['details']['price']),
        photos=room['details']['photos'],
    )

def map_address(dormitory):
    return f"г. {dormitory['details']['main-info']['city']} {dormitory['details']['main-info']['street']} д. {dormitory['details']['main-info']['houseNumber']}"

@router.get('/', response_model=List[Dormitory])
def all_dormitories():
    r = requests.get(f"{API_BASE}/dormitories/all")
    dormitories = r.json()

    return [
        Dormitory(
            id=dormitory['id'], 
            name=dormitory['details']['main-info']['name'], 
            description=dormitory['details']['rules']['requiredStudentsDocuments'],
            address=map_address(dormitory),
            lat=fix_coord(dormitory['details']['main-info']['coordinates']['lat']),
            lng=fix_coord(dormitory['details']['main-info']['coordinates']['lng']),
            photos=dormitory['details']['main-info']['photos'],
            rooms=list(map(map_room, dormitory['rooms'].values())),
            price_min=min([int(room['details']['price']) for room in dormitory['rooms'].values()]),
            price_max=max([int(room['details']['price']) for room in dormitory['rooms'].values()]),
        ) for dormitory in dormitories if 'details' in dormitory and 'main-info' in dormitory['details'] and 'rules' in dormitory['details'] and len(dormitory['rooms'].values()) > 0
    ]
    

@router.get('/{dormitoryId}/booking/{roomId}', response_model=APIRoomBookingPreview)
def booking_preview(dormitoryId: str, roomId: str, token: str = Depends(get_token_from_header)):
    r = requests.get(f"{API_BASE}/me", headers={
        'Authorization': token
    })
    me = r.json()

    if 'id' not in me:
        raise HTTPException(403, 'Forbidden')

    r = requests.get(f"{API_BASE}/dormitories/{dormitoryId}", headers={
        'Authorization': token
    })
    dormitory = r.json()

    r = requests.get(f"{API_BASE}/rooms/{roomId}", headers={
        'Authorization': token
    })
    room = r.json()

    return APIRoomBookingPreview(
        name=me['name'],
        phone=me['phone'],
        email=me['email'],
        dormitory=dormitory['details']['main-info']['name'],
        address=map_address(dormitory),
        room_type=room['details']['type'],
        price=int(room['details']['price']),
        available=int(room['details']['amount']),
    )

@router.post('/{dormitoryId}/booking/{roomId}')
def book(dormitoryId: str, roomId: str, data: APIRoomBookingPayload, token: str = Depends(get_token_from_header)):
    r = requests.get(f"{API_BASE}/me", headers={
        'Authorization': token
    })
    me = r.json()

    if 'id' not in me:
        raise HTTPException(403, 'Forbidden')

    payload = {
        'author': {
            'name': me['name'],
            'contacts': {
                'phone': me['phone'],
                'email': me['email']
            },
            'role': 'user'
        },
        'dates': {
            'from': data.date_from.strftime('%Y-%m-%d'),
            'to': data.date_to.strftime('%Y-%m-%d'),
        },
        'quantity': str(data.guests_count),
        'roomId': roomId,
        'studentList': me['name']
    }
    r = requests.post(f"{API_BASE}/bookings", json=payload, headers={
        'Authorization': token
    })
    resp = r.json()

    return resp
