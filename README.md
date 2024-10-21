# FastAPI Social Media API

A robust REST API for a social media platform built with FastAPI, featuring user authentication, post management, and secure data handling.

## 🚀 Features

- **User Management**
  - Secure user registration and authentication
  - JWT token-based authorization
  - Password hashing with bcrypt
  - User profile management

- **Post Management**
  - Create, read, update, and delete posts
  - Pagination support
  - Vote/Like system for posts
  - User-post relationship handling

- **Security**
  - OAuth2 implementation with JWT
  - Password hashing
  - Input validation and sanitization
  - Protected routes with authentication required

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Primary database
- **SQLAlchemy**: ORM (Object Relational Mapping)
- **Alembic**: Database migrations
- **Pydantic**: Data validation using Python type annotations
- **passlib**: Password hashing
- **python-jose**: JWT token handling

## 📋 Prerequisites

- Python 3.8+
- PostgreSQL
- Docker (optional)

## 🔧 Installation

1. Clone the repository
```bash
git clone https://github.com/Ahmad-Git-Hub/fastapi-social-media.git
cd fastapi-social-media
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file in the root directory with the following variables:
```env
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_password
DATABASE_NAME=fastapi
DATABASE_USERNAME=postgres
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. Run database migrations
```bash
alembic upgrade head
```

## 🚀 Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## 📝 API Endpoints

### Authentication
- `POST /users/`: Create new user
- `POST /login`: Login user
- `GET /users/{id}`: Get user by ID

### Posts
- `GET /posts/`: Get all posts
- `POST /posts/`: Create new post
- `GET /posts/{id}`: Get post by ID
- `PUT /posts/{id}`: Update post
- `DELETE /posts/{id}`: Delete post
- `POST /vote/`: Vote on post


## 🔐 Security Features

- Password hashing using bcrypt
- JWT token authentication
- OAuth2 with Password Bearer
- Input validation using Pydantic models
- Protected routes requiring authentication

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👏 Acknowledgments

This project was developed by following the comprehensive FastAPI tutorial series by [Sanjeev Thiyagarajan](https://www.youtube.com/@SanjeevThiyagarajan). His excellent tutorial series provided the foundation and inspiration for this implementation.

* Tutorial Author: Sanjeev Thiyagarajan
* Tutorial Channel: [Watch the tutorial series](https://www.youtube.com/@SanjeevThiyagarajan)

The project structure and core functionality are based on his teachings, with some modifications and additional features added for learning purposes.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

