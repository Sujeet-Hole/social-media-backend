import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Post
from app.schemas import PostCreate, PostResponse, PaginatedPostsResponse
import logging
router = APIRouter()
logger = logging.getLogger(__name__)


def paginate_posts(query, page: int, limit: int) -> dict:
    """Reusable helper: applies pagination to any Post query and returns response dict."""
    total = query.count()
    posts = query.order_by(Post.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    total_pages = math.ceil(total / limit) if total > 0 else 1
    return {
        "posts": posts,
        "total": total,
        "page": page,
        "pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }



@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Creating post for user: {user_id}")
    new_post = Post(content=post.content, user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    logger.info(f"Post created: {new_post.id}")
    return new_post



@router.get("/", response_model=PaginatedPostsResponse)
def get_posts(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Posts per page"),
    user_id: int = Query(None, description="Filter by user ID (optional)"),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching posts - user_id: {user_id}, page: {page}, limit: {limit}")
    query = db.query(Post)
    if user_id is not None:
        query = query.filter(Post.user_id == user_id)
    return paginate_posts(query, page, limit)



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


