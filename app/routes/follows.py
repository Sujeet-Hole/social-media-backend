from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Follow, User
import logging
router = APIRouter()

import logging
logger = logging.getLogger(__name__)

@router.post("/{user_id}")
def follow_user(user_id: int, follower_id: int, db: Session = Depends(get_db)):
    logger.info(f"User {follower_id} trying to follow {user_id}")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    
    existing = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.following_id == user_id
    ).first()
    
    if existing:
        logger.warning(f"User {follower_id} already following {user_id}")
        raise HTTPException(status_code=400, detail="Already following")
    
    follow = Follow(follower_id=follower_id, following_id=user_id)
    db.add(follow)
    db.commit()
    logger.info(f"User {follower_id} followed {user_id}")
    return {"message": "Followed successfully"}

@router.delete("/{user_id}")
def unfollow_user(user_id: int, follower_id: int, db: Session = Depends(get_db)):
    logger.info(f"User {follower_id} trying to unfollow {user_id}")
    
    follow = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.following_id == user_id
    ).first()
    
    if not follow:
        logger.warning(f"User {follower_id} not following {user_id}")
        raise HTTPException(status_code=404, detail="Not following")
    
    db.delete(follow)
    db.commit()
    logger.info(f"User {follower_id} unfollowed {user_id}")
    return {"message": "Unfollowed successfully"}

@router.get("/{user_id}")
def get_followers(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching followers for user: {user_id}")
    followers = db.query(Follow).filter(Follow.following_id == user_id).all()
    logger.info(f"User {user_id} has {len(followers)} followers")
    return {"followers": len(followers), "data": followers}