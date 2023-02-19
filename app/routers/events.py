import datetime
import requests
from fastapi import APIRouter, Depends, HTTPException

from ..constants import API_BASE
from ..dependencies import get_token_from_header
from ..schemas.events import APIEventBookingPayload, APIEventBookingPreview

router = APIRouter(prefix='/events')

@router.get('/')
def all_events():
    r = requests.get(f"{API_BASE}/events/all")
    events = r.json()
    
    month_events = []
    cursor = datetime.datetime.today()

    for event in events:
        if event['details']['dates']['from'] / 1000.0 <= cursor.timestamp() <= event['details']['dates']['to'] / 1000.0:
            month_events.append({
                'id': event['id'],
                'type': event['details']['type'],
                'name': event['details']['name'],
                'description': event['details']['description'],
                'price': event['details']['price'],
                'photos': event['details']['photos'],
                'day': cursor.strftime("%d"),
                'month': cursor.strftime("%b")
            })
            cursor += datetime.timedelta(days=1)
        
        if len(month_events) == 30:
            break

    return month_events

@router.get('/{eventId}')
def evenT_details(eventId: str):
    r = requests.get(f"{API_BASE}/events/{eventId}")
    event = r.json()

    r = requests.get(f"{API_BASE}/universities/{event['universityId']}")
    university = r.json()

    return {
        'id': event['id'],
        'type': event['details']['type'],
        'name': event['details']['name'],
        'description': event['details']['description'],
        'price': int(event['details']['price']),
        'photos': event['details']['photos'],
        'videos': event['details']['video'] if 'video' in event['details'] else [],
        'university': university['details']['name'],
        'address': f"{university['details']['region']} г. {university['details']['city']}",
        'contacts': university['details']['adminContacts'] if 'adminContacts' in university['details'] else university['details']['site'],
    }


@router.get('/{eventId}/booking', response_model=APIEventBookingPreview)
def booking_preview(eventId: str, token: str = Depends(get_token_from_header)):
    r = requests.get(f"{API_BASE}/me", headers={
        'Authorization': token
    })
    me = r.json()

    if 'id' not in me:
        raise HTTPException(403, 'Forbidden')

    r = requests.get(f"{API_BASE}/events/{eventId}", headers={
        'Authorization': token
    })
    event = r.json()

    return APIEventBookingPreview(
        name=me['name'],
        phone=me['phone'],
        email=me['email'],
        event=event['details']['name'],
        from_date=round(float(event['details']['dates']['from']) / 1000),
        to_date=round(float(event['details']['dates']['from']) / 1000),
        price=int(event['details']['price'])
    )

@router.post('/{eventId}/booking')
def book(eventId: str, data: APIEventBookingPayload, token: str = Depends(get_token_from_header)):
    r = requests.get(f"{API_BASE}/me", headers={
        'Authorization': token
    })
    me = r.json()

    if 'id' not in me:
        raise HTTPException(403, 'Forbidden')

    payload = {
        'details': {
            'fullName': me['name'],
            'phone': me['phone'],
            'email': me['email'],
            'quantity': str(data.guests_count),
        },
        'eventId': eventId,
    }
    r = requests.post(f"{API_BASE}/event-bookings", json=payload, headers={
        'Authorization': token
    })
    resp = r.json()

    return resp
