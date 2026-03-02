import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routes import users, posts, follows, feed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)
logger.info("Database tables created")

app = FastAPI(title="Social Media API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/auth", tags=["Auth"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(follows.router, prefix="/follow", tags=["Follow"])
app.include_router(feed.router, prefix="/feed", tags=["Feed"])

@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "Social Media API is running!"}