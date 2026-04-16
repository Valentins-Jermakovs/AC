# VISITS METRICS SERVICE

## DESCRIPTION

This microservice is responsible for:

- Recording user visit metrics
- Storing data in MongoDB
- Preparing statistical data for analysis

The service is built using FastAPI.

## REQUIREMENTS

Python 3.10+
MongoDB
pip / virtualenv
Docker (optional)

## ENVIRONMENT VARIABLES

Create a .env file in the root directory before running the service.

DOCKER (.env)
MONGO_URL=mongodb://admin:secretpassword@mongodb_container:27017
DB_NAME=visits
SECRET_KEY=5354e4c2aac4ad10cd6c9e7d160c9276a34c65fbc5102b5cd49ce6d2697e7ab5
ALGORITHM=HS256

LOCAL DEVELOPMENT (.env)
MONGO_URL=mongodb://admin:secretpassword@localhost:27017
DB_NAME=visits
SECRET_KEY=5354e4c2aac4ad10cd6c9e7d160c9276a34c65fbc5102b5cd49ce6d2697e7ab5
ALGORITHM=HS256

## RUNNING LOCALLY

1. Create virtual environment python3 -m venv venv
2. Activate virtual environment

Linux / macOS:
source venv/bin/activate

Windows:
venv\Scripts\activate

3. Install dependencies

```pip install -r requirements.txt```

4. Run server

```uvicorn main:app --reload```

Service URL: http://localhost:8000
API docs: http://localhost:8000/docs

## NOTES

- MongoDB must be running before starting the service
- Docker uses mongodb_container as host
- Local uses localhost