from bs4 import BeautifulSoup
import requests
from fastapi import APIRouter

from ..constants import API_BASE


router = APIRouter(prefix='/news')

@router.get('/')
def all_events():
    r = requests.get(f"{API_BASE}/articles")
    articles = r.json()

    news = []

    for article in articles:
        news.append({
            'id': article['id'],
            'title': article['title'],
            'cover': article['cover'],
            'content': BeautifulSoup(article['content'], 'html.parser').text
        })

        if len(news) == 10:
            break

    return news
