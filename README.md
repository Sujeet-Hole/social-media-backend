# Social Media Backend API — Mini Twitter Clone

A production-ready REST API for a social media platform built with **FastAPI**, **MySQL**, **JWT Authentication**, and **Docker**.

---

# 🚀 Tech Stack

* **FastAPI** — Modern, high-performance web framework
* **MySQL** — Relational database
* **SQLAlchemy** — ORM for database interaction
* **JWT** — Stateless authentication
* **Passlib + Bcrypt** — Secure password hashing
* **Docker** — Containerized deployment
* **Python Logging** — Production-grade logging

---

# 📁 Project Structure

```
mini-social/
├── app/
│   ├── main.py          # Application entry point
│   ├── database.py      # Database connection setup
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic request/response models
│   ├── auth.py          # JWT authentication utilities
│   └── routes/
│       ├── users.py     # User authentication routes
│       ├── posts.py     # Post management routes
│       ├── follows.py   # Follow/unfollow routes
│       └── feed.py      # Feed generation routes
│
├── frontend/
│   └── index.html       # Simple frontend test page
│
├── Dockerfile           # Docker image configuration
├── docker-compose.yml   # Multi-container setup
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
└── README.md
```

---

# 🔑 API Endpoints

## Authentication

| Method | Endpoint           | Description                 |
| ------ | ------------------ | --------------------------- |
| POST   | `/auth/register`   | Register new user           |
| POST   | `/auth/login`      | Login and receive JWT token |
| GET    | `/auth/users/{id}` | Get user profile            |

---

## Posts

| Method | Endpoint           | Description      |
| ------ | ------------------ | ---------------- |
| POST   | `/posts/`          | Create a post    |
| GET    | `/posts/{user_id}` | Get user's posts |
| DELETE | `/posts/{post_id}` | Delete a post    |

---

## Follow System

| Method | Endpoint            | Description         |
| ------ | ------------------- | ------------------- |
| POST   | `/follow/{user_id}` | Follow a user       |
| DELETE | `/follow/{user_id}` | Unfollow a user     |
| GET    | `/follow/{user_id}` | Get followers count |

---

## Feed

| Method | Endpoint | Description                   |
| ------ | -------- | ----------------------------- |
| GET    | `/feed/` | Get posts from followed users |

---

# ⚙️ Local Setup (Without Docker)

## 1. Clone the repository

```
git clone https://github.com/Sujeet-Hole/social-media-backend.git
cd social-media-backend
```

---

## 2. Create virtual environment

```
python -m venv venv
```

Activate:

Windows

```
venv\Scripts\activate
```

Linux / Mac

```
source venv/bin/activate
```

---

## 3. Install dependencies

```
pip install -r requirements.txt
```

---

## 4. Create `.env` file

```
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/minisocial
SECRET_KEY=your-secret-key
```

---

## 5. Run the server

```
uvicorn app.main:app --reload
```

---

## 6. Open API documentation

```
http://localhost:8000/docs
```

---

# 🐳 Run with Docker

## 1. Build and start containers

```
docker-compose up --build
```

---

## 2. Run containers in background

```
docker-compose up -d
```

---

## 3. Stop containers

```
docker-compose down
```

---

## 4. View container logs

```
docker-compose logs -f
```

---

## 5. Open API documentation

```
http://localhost:8000/docs
```

---

# 📌 Features

* JWT based stateless authentication
* Password hashing using bcrypt
* Follow / Unfollow system
* Personalized feed system
* Production-ready logging
* CORS enabled
* Automatic Swagger documentation
* Docker container support

---

# 👨‍💻 Author

**Sujeet Hole**

GitHub
https://github.com/Sujeet-Hole
