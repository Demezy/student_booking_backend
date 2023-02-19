from pydantic import BaseModel


class Event(BaseModel):
    pass


class APIEventBookingPreview(BaseModel):
    name: str
    phone: str
    email: str
    event: str
    from_date: int
    to_date: int
    price: int


class APIEventBookingPayload(BaseModel):
    guests_count: int
