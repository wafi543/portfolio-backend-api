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

### Portfolio Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/portfolio/categories/` | List user's categories |
| `POST` | `/api/portfolio/categories/` | Create new category |
| `GET` | `/api/portfolio/categories/<id>/` | Retrieve category details |
| `PUT` | `/api/portfolio/categories/<id>/` | Update category |
| `DELETE` | `/api/portfolio/categories/<id>/` | Delete category |

### Portfolio
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/portfolio/` | List portfolios (filter by `?category=<id>`, `?recent`) |
| `POST` | `/api/portfolio/` | Create new portfolio (authenticated) |
| `GET` | `/api/portfolio/<id>/` | Retrieve portfolio details |
| `PUT` | `/api/portfolio/<id>/` | Update portfolio (authenticated) |
| `PATCH` | `/api/portfolio/<id>/` | Partial portfolio update (authenticated) |
| `DELETE` | `/api/portfolio/<id>/` | Delete portfolio (authenticated) |
| `GET` | `/api/portfolio/info/` | Get public portfolio info |

> **Note**: Portfolio filtering supports `?category=<id>` for category-based filtering and `?recent` to get the latest 6 portfolios.

## Quick Start

### Prerequisites
- Python 3.11+
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

### Loading Fixture Data (Optional)

To quickly set up a photographer user with default portfolio categories:

```bash
# Create photographer user with default categories
python manage.py add_photographer_fixtures

# Or specify custom username and email
python manage.py add_photographer_fixtures --username john_doe --email john@example.com
```

This command creates:
- A user with "Photographer" job title
- 4 default portfolio categories: Photography, Video Editing, Branding, and Design

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

### Create Superuser in Docker

To create a superuser in your running Django container:

```bash
docker exec -it django_app python manage.py createsuperuser
```

Or use a Python script for non-interactive setup:

```bash
docker exec -it django_app python manage.py shell << EOF
from users.models import User
User.objects.create_superuser('admin', 'admin@example.com', '@admin123123')
EOF

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
