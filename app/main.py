from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth
from .routers import news
from .routers import events
from .routers import avatars
from .routers import favorites
from .routers import dormitories

from .notifications import notify_all

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(news.router)
app.include_router(events.router)
app.include_router(avatars.router)
app.include_router(favorites.router)
app.include_router(dormitories.router)

@app.get('/')
def main():
    notify_all('Кто-то стучиться в сервис')
