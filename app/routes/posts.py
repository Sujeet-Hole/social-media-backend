from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post
from app.schemas import PostCreate, PostResponse
import logging
router = APIRouter()
@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Creating post for user: {user_id}")
    new_post = Post(content=post.content, user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    logger.info(f"Post created: {new_post.id}")
    return new_post

@router.get("/{user_id}", response_model=list[PostResponse])
def get_posts(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching posts for user: {user_id}")
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    return posts

@router.delete("/{post_id}")
def delete_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Delete request for post: {post_id} by user: {user_id}")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        logger.warning(f"Post not found: {post_id}")
        raise HTTPException(status_code=404, detail="Post not found")
    if post.user_id != user_id:
        logger.warning(f"Unauthorized delete attempt by user: {user_id}")
        raise HTTPException(status_code=403, detail="Not your post")
    db.delete(post)
    db.commit()
    logger.info(f"Post deleted: {post_id}")
    return {"message": "Post deleted"}