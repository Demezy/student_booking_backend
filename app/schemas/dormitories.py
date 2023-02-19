from typing import List
from datetime import date
from pydantic import BaseModel


class Room(BaseModel):
    id: str
    description: str
    type: str
    price: int
    photos: List[str]


class Dormitory(BaseModel):
    id: str
    name: str
    address: str
    description: str
    lat: float
    lng: float
    photos: List[str]
    rooms: List[Room]
    price_min: int
    price_max: int


class APIRoomBookingPreview(BaseModel):
    name: str
    email: str
    phone: str
    dormitory: str
    address: str
    room_type: str
    price: int
    available: int


class APIRoomBookingPayload(BaseModel):
    guests_count: int
    date_from: date
    date_to: date
