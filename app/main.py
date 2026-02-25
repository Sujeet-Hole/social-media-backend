from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import users, posts, likes, follows

# Create FastAPI app
app = FastAPI(
    title="Social Media API",
    version="1.0.0",
    description="FastAPI backend with JWT authentication"
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(likes.router, prefix="/likes", tags=["Likes"])
app.include_router(follows.router, prefix="/follows", tags=["Follows"])

# Health check
@app.get("/")
def root():
    return {"message": "API is running"}