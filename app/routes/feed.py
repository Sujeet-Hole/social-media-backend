from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Follow, Post
from app.schemas import PostResponse
import logging
router = APIRouter()


import logging
logger = logging.getLogger(__name__)

@router.get("/", response_model=list[PostResponse])
def get_feed(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching feed for user: {user_id}")
    
    following = db.query(Follow).filter(Follow.follower_id == user_id).all()
    following_ids = [f.following_id for f in following]
    
    if not following_ids:
        logger.warning(f"User {user_id} is not following anyone")
        return []
    
    posts = db.query(Post).filter(
        Post.user_id.in_(following_ids)
    ).order_by(Post.created_at.desc()).all()
    
    logger.info(f"Feed fetched for user {user_id}: {len(posts)} posts")
    return posts