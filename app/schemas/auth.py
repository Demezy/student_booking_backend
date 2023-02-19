from pydantic import BaseModel


class APILogin(BaseModel):
    email: str
    password: str


class APIRegsiter(APILogin):
    name: str
    phone: str


class APIToken(BaseModel):
    token: str


class APIUser(BaseModel):
    id: str
    name: str
    email: str
    phone: str
