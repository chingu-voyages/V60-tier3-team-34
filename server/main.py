from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from db.database import async_session_maker
from models.tweet import Tweet
from models.user_settings import UserSettings
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    html_file = BASE_DIR / "templates" / "dashboard.html"
    return HTMLResponse(content=html_file.read_text())

@app.get("/api/signal-feed")
async def signal_feed_partial(limit: int = Query(default=20, ge=1, le=100)):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Tweet).order_by(Tweet.created_at.desc()).limit(limit)
        )
        tweets = result.scalars().all()
    return [
        {
            "text": t.tweet_text,
            "link": t.tweet_link,
            "created_at": str(t.created_at)
        }
        for t in tweets
    ]

@app.get("/tweets")
async def get_tweets(limit: int = Query(default=5, ge=1, le=100)):
    async with async_session_maker() as session:
        result = await session.execute(
            select(Tweet).order_by(Tweet.created_at.desc()).limit(limit)
        )
        tweets = result.scalars().all()
        return [{col.name: getattr(t, col.name) for col in t.__table__.columns} for t in tweets]

@app.get("/users")
async def get_users(limit: int = Query(default=5, ge=1, le=100)):
    async with async_session_maker() as session:
        result = await session.execute(
            select(UserSettings).order_by(UserSettings.created_at.desc()).limit(limit)
        )
        users = result.scalars().all()
        return [{col.name: getattr(u, col.name) for col in u.__table__.columns} for u in users]
