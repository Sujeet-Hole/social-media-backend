from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Follow, Post
from app.schemas import PostResponse
import logging
import redis
import json
router = APIRouter()

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

import logging
logger = logging.getLogger(__name__)

@router.get("/", response_model=list[PostResponse])
def get_feed(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching feed for user: {user_id}")

    r = redis_client

    cache_key = f"feed:{user_id}"

    cached_feed = r.get(cache_key)

    if cached_feed:
        logger.info("Feed returned from Redis")
        return json.loads(cached_feed)
    logger.info(f"REDIS MISS: {cache_key}")
    following = db.query(Follow).filter(Follow.follower_id == user_id).all()
    following_ids = [f.following_id for f in following]
    
    if not following_ids:
        logger.warning(f"User {user_id} is not following anyone")
        return []
    
    posts = db.query(Post).filter(
        Post.user_id.in_(following_ids)
    ).order_by(Post.created_at.desc()).all()    
    
    response = [
        PostResponse.model_validate(post).model_dump()
        for post in posts
    ]

    redis_client.setex(
        cache_key,
        300,
        json.dumps(response)
    )
    logger.info("Feed stored in Redis")
    logger.info(f"Feed fetched for user {user_id}: {len(posts)} posts")
    return response