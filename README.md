# Sports Recruitment Platform

An intelligent sports recruitment platform that connects athletes with sports organizations.

Built with FastAPI, SQLAlchemy 2.0, and PostgreSQL.

## Features

### Athletes
- Register and login with simple token-based authentication
- Create and manage athlete profile
- Add diplomas and certifications
- Add professional experiences
- Search job offers
- Apply to offers
- Contact sports organizations through messages

### Sports Organizations
- Register and login
- Create and manage organization profile
- Publish job offers
- Search athlete profiles
- View applications
- Contact athletes through messages

## Tech Stack

- **FastAPI** - modern Python web framework
- **SQLAlchemy 2.0** - ORM with async support
- **PostgreSQL** - relational database
- **Alembic** - database migrations
- **Pydantic v2** - data validation
- **Passlib** - password hashing

## Project Structure

```
├── alembic/                  # Migration configuration
├── src/
│   ├── core/                 # Config, database, security, dependencies
│   ├── auth/                 # Authentication module
│   ├── users/                # User management
│   ├── athlete_profiles/     # Athlete profile management
│   ├── organizations/        # Organization management
│   ├── diplomas/             # Diploma & certification management
│   ├── experiences/          # Professional experience management
│   ├── offers/               # Job offer management
│   ├── applications/         # Application management
│   ├── messages/             # Messaging system
│   └── main.py              # Application entry point
├── tests/
├── .env
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sports-recruitment-platform
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in `.env`:
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/sports_recruitment
   SECRET_KEY=your-secret-key-here
   ```

5. Create the database:
   ```bash
   createdb sports_recruitment
   ```

6. Run database migrations:
   ```bash
   alembic upgrade head
   ```

7. (Optional) Seed the database with sample data:
   ```bash
   python seed.py
   ```

8. Start the server:
   ```bash
   uvicorn src.main:app --reload
   ```

9. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get auth token |
| GET | `/auth/me` | Get current user info |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | List all users |
| GET | `/users/{id}` | Get user by ID |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |

### Athlete Profiles
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/athletes/` | Create athlete profile |
| GET | `/athletes/` | List all athletes |
| GET | `/athletes/{id}` | Get athlete by ID |
| PUT | `/athletes/{id}` | Update athlete profile |
| DELETE | `/athletes/{id}` | Delete athlete profile |

### Organizations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/organizations/` | Create organization |
| GET | `/organizations/` | List all organizations |
| GET | `/organizations/{id}` | Get organization by ID |
| PUT | `/organizations/{id}` | Update organization |
| DELETE | `/organizations/{id}` | Delete organization |

### Diplomas
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/diplomas/` | Add diploma |
| GET | `/diplomas/` | List diplomas |
| PUT | `/diplomas/{id}` | Update diploma |
| DELETE | `/diplomas/{id}` | Delete diploma |

### Experiences
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/experiences/` | Add experience |
| GET | `/experiences/` | List experiences |
| PUT | `/experiences/{id}` | Update experience |
| DELETE | `/experiences/{id}` | Delete experience |

### Offers
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/offers/` | Create job offer |
| GET | `/offers/` | List offers |
| GET | `/offers/{id}` | Get offer by ID |
| PUT | `/offers/{id}` | Update offer |
| DELETE | `/offers/{id}` | Delete offer |

### Applications
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/applications/` | Submit application |
| GET | `/applications/` | List applications |
| PUT | `/applications/{id}/accept` | Accept application |
| PUT | `/applications/{id}/reject` | Reject application |

### Messages
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/messages/` | Send message |
| GET | `/messages/` | List user messages |
| GET | `/messages/conversation/{user_id}` | Get conversation |

## Authentication

The API uses a simple token-based authentication system:
- Register or login to receive an auth token
- Include the token in the `Authorization` header: `Bearer <token>`
- No JWT involved - tokens are random UUIDs stored in the database

## Architecture

The project follows clean architecture principles:
- **Models** - SQLAlchemy ORM models defining database schema
- **Schemas** - Pydantic models for request/response validation
- **Repositories** - Data access layer for database operations
- **Services** - Business logic layer
- **Routers** - HTTP layer with endpoints
- **Dependencies** - Shared dependencies (auth, DB session)

## Generating Migrations

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```
