Authentication Service - Deployment Guide

Requirements

-   Docker installed
-   PostgreSQL
-   Google OAuth credentials

Environment Variables (.env)

Create a .env file in the project root:

DATABASE_URL=postgresql+asyncpg://postgres:rootpass@auth_postgres:5432/authdb
SECRET_KEY=your_super_secret_key ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10 GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

Description

DATABASE_URL -> Async PostgreSQL connection string
SECRET_KEY -> Used for JWT signing
ALGORITHM -> JWT algorithm
ACCESS_TOKEN_EXPIRE_MINUTES -> Token lifetime
GOOGLE_CLIENT_ID / SECRET -> From Google Cloud Console
GOOGLE_REDIRECT_URI -> Must match authorized redirect URI

1.  Start PostgreSQL

docker run -d –name auth_postgres -e POSTGRES_USER=postgres -e
POSTGRES_PASSWORD=rootpass -e POSTGRES_DB=authdb -p 5432:5432 -v
auth_pg_data:/var/lib/postgresql/data postgres:16

2.  Start pgAdmin (Optional)

docker run -d –name auth_pgadmin –link auth_postgres:db -e
PGADMIN_DEFAULT_EMAIL=admin@admin.com -e PGADMIN_DEFAULT_PASSWORD=admin
-p 8081:80 dpage/pgadmin4

3.  Build Authentication Server

docker build -t auth-fastapi .

4.  Run Authentication Server

docker run -d –name auth-fastapi-container –link auth_postgres:db
–env-file .env -p 8000:80 auth-fastapi

Access

API: http://localhost:8000 Swagger: http://localhost:8000/docs

Google OAuth

Add authorized redirect URI in Google Cloud Console:

http://localhost:8000/auth/google/callback