# Django Posts API

A lightweight Django REST Framework backend providing session-based authentication and user-scoped post management. Perfect for pairing with any React or modern JavaScript frontend.

## Features

- **Session-based Authentication**: Secure user login/logout with Django's built-in session management
- **User Authentication**: Get current user info and password change functionality
- **Post Management**: Full CRUD operations with automatic ownership enforcement
- **Django Password Validation**: Built-in Django security standards
- **Clean Architecture**: Well-organized app structure with separated concerns

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/login/` | User login |
| `POST` | `/api/auth/logout/` | User logout |
| `GET` | `/api/auth/me/` | Get current user info |
| `POST` | `/api/auth/password-change/` | Change password |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/posts/` | List user's posts |
| `POST` | `/api/posts/` | Create new post |
| `GET` | `/api/posts/<id>/` | Retrieve post details |
| `PUT` | `/api/posts/<id>/` | Replace entire post |
| `PATCH` | `/api/posts/<id>/` | Partial post update |
| `DELETE` | `/api/posts/<id>/` | Delete post |

> **Note**: Each user only has access to their own posts.

## Quick Start

### Prerequisites
- Python 3.8+
- pip and venv

### Installation

1. **Clone and navigate to the project:**
```bash
cd django_posts_api
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
# .\venv\Scripts\activate  # Windows
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

6. **Start development server:**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Frontend Integration

### React/Axios Example
```javascript
// Login request with credentials
const response = await axios.post("/api/auth/login/", {
  username: "user@example.com",
  password: "password123"
}, { withCredentials: true });

// Subsequent requests will automatically include session cookies
```

## Database Setup

### SQLite (Default)
The default configuration uses SQLite, which is configured out-of-the-box.

### PostgreSQL (Optional)

Run a PostgreSQL container locally:

```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=db_password \
  -e POSTGRES_DB=db_portfolio \
  -p 5432:5432 \
  postgres:16
```

Update `settings.py` to use PostgreSQL:
```python
DATABASES = {
    'default': dj_database_url.config(default='postgres://admin:db_password@localhost:5432/db_portfolio')
}
```

## Project Structure

```
django_posts_api/
├── auth/                          # Authentication app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── permissions.py
├── posts/                         # Posts app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── permissions.py
├── config/                        # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
└── README.md
```

## Docker Support

Build and run the application in Docker:

```bash
source environments/.env.prod && docker-compose up -d --build
```

Or build manually:
```bash
./build.sh
```

## Environment Variables

Create a `.env` file in the project root (optional for development):

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## Testing

Run tests with:
```bash
python manage.py test
```

## License

This project is part of a portfolio. Feel free to fork and modify for learning purposes.
