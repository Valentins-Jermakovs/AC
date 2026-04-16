# NEWS SERVICE

## DESCRIPTION

This microservice is responsible for:

- Creating news articles
- Reading and retrieving news content
- Managing news feeds and updates
- Supporting content delivery for users and systems

The service is built using FastAPI and MongoDB.

## REQUIREMENTS

- Python 3.10+
- MongoDB
- pip / virtualenv
- Docker (optional)

## ENVIRONMENT VARIABLES

Create a .env file in the root directory before running the service.

DOCKER (.env)
MONGO_URL=mongodb://admin:secretpassword@mongodb_container:27017
DB_NAME=news
SECRET_KEY=5354e4c2aac4ad10cd6c9e7d160c9276a34c65fbc5102b5cd49ce6d2697e7ab5
ALGORITHM=HS256

LOCAL DEVELOPMENT (.env)
MONGO_URL=mongodb://admin:secretpassword@localhost:27017
DB_NAME=news
SECRET_KEY=5354e4c2aac4ad10cd6c9e7d160c9276a34c65fbc5102b5cd49ce6d2697e7ab5
ALGORITHM=HS256

## RUNNING LOCALLY

1. Create virtual environment: python3 -m venv venv
2. Activate virtual environment

Linux / macOS:
source venv/bin/activate

Windows:
venv\Scripts\activate

3. Install dependencies

```pip install -r requirements.txt```

4. Run server

```fastapi dev main.py```

Service URL: http://localhost:8000
API docs: http://localhost:8000/docs

## RUNNING THE NEWS SERVICE IN DOCKER

```
docker build -t news-fastapi .
```

```
docker run -d \
  --name news-fastapi-container \
  --network analytics-network \
  --env-file .env \
  -p 8004:80 \
  news-fastapi
```

## NOTES

- MongoDB must be running before starting the service
- Docker uses mongodb_container as hostname
- Local development uses localhost
- This service handles news creation, storage, and retrieval for users and systems