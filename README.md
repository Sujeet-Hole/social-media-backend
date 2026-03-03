# Social Media Backend API — Mini Twitter Clone

A production-ready REST API for a social media platform built with **FastAPI**, **MySQL**, **JWT Authentication**.

## 🚀 Tech Stack

- **FastAPI** — Modern, fast web framework
- **MySQL** — Relational database
- **SQLAlchemy** — ORM for database interaction
- **JWT** — Stateless authentication
- **Passlib + Bcrypt** — Password hashing
- **Python Logging** — Production-grade logging

## 📁 Project Structure
```
mini-social/
├── app/
│   ├── main.py          # App entry point
│   ├── database.py      # DB connection
│   ├── models.py        # Database tables
│   ├── schemas.py       # Request/Response models
│   ├── auth.py          # JWT & password utilities
│   └── routes/
│       ├── users.py     # Auth routes
│       ├── posts.py     # Post routes
│       ├── follows.py   # Follow routes
│       └── feed.py      # Feed route
├── frontend/
│   └── index.html       # Simple frontend
├── .env                 # Environment variables
└── requirements.txt     # Dependencies
```

## 🔑 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| GET | `/auth/users/{id}` | Get user profile |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/posts/` | Create a post |
| GET | `/posts/{user_id}` | Get user's posts |
| DELETE | `/posts/{post_id}` | Delete a post |

### Follow
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/follow/{user_id}` | Follow a user |
| DELETE | `/follow/{user_id}` | Unfollow a user |
| GET | `/follow/{user_id}` | Get followers count |

### Feed
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/feed/` | Get feed from followed users |

## ⚙️ Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/Sujeet-Hole/social-media-backend.git
cd social-media-backend
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup `.env` file
```
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/minisocial
SECRET_KEY=your-secret-key
```

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

### 6. Open API docs
```
http://localhost:8000/docs
```

## 📌 Features

- JWT based stateless authentication
- Password hashing with bcrypt
- Follow/Unfollow system
- Personalized feed from followed users
- Production-grade logging on all routes
- CORS enabled
- Auto-generated Swagger docs

## 👨‍💻 Author

**Sujeet Hole** — [GitHub](https://github.com/Sujeet-Hole)