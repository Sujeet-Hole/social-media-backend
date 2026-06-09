from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Follow, Post
from app.schemas import PostResponse
import logging
import redis
import json
import os

router = APIRouter()

logger = logging.getLogger(__name__)

redis_client = redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)


@router.get("/", response_model=list[PostResponse])
def get_feed(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching feed for user: {user_id}")

    # Check Redis connection
    try:
        logger.info(f"Redis Ping: {redis_client.ping()}")
    except Exception as e:
        logger.error(f"Redis Error: {e}")

    cache_key = f"feed:{user_id}"

    # Check cache
    cached_feed = redis_client.get(cache_key)

    if cached_feed:
        logger.info(f"REDIS HIT: {cache_key}")
        return json.loads(cached_feed)

    logger.info(f"REDIS MISS: {cache_key}")

    # Get following users
    following = db.query(Follow).filter(
        Follow.follower_id == user_id
    ).all()

    following_ids = [f.following_id for f in following]

    # Empty feed
    if not following_ids:
        logger.warning(f"User {user_id} is not following anyone")

        logger.info("BEFORE CACHE EMPTY")

        redis_client.setex(
            cache_key,
            300,
            json.dumps([])
        )

        logger.info("AFTER CACHE EMPTY")

        # Verify immediately
        test = redis_client.get(cache_key)
        logger.info(f"CACHE VERIFY: {test}")

        return []

    # Fetch posts
    posts = db.query(Post).filter(
        Post.user_id.in_(following_ids)
    ).order_by(Post.created_at.desc()).all()

    response = [
        PostResponse.model_validate(post).model_dump(mode="json")
        for post in posts
    ]

    logger.info("BEFORE CACHE POSTS")

    redis_client.setex(
        cache_key,
        300,
        json.dumps(response)
    )

    logger.info("AFTER CACHE POSTS")

    test = redis_client.get(cache_key)

    if test:
        logger.info("CACHE STORED SUCCESSFULLY")
    else:
        logger.error("CACHE STORE FAILED")

    logger.info(f"Feed stored in Redis: {cache_key}")
    logger.info(f"Feed fetched for user {user_id}: {len(posts)} posts")

    return response