# Product microservice in Flask

This is a Flask microservice API, which serves for:
1. Product management (CRUD)
2. Registration with external offer API endpoint
3. Viewing offers related to products
4. Tracking offer prices from a particular shop

## Get started

Requirements:
- Installed Docker
- git clone this repository

Set the following environment variables in an `./instance/production.env` file:
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `OFFERS_MICROSERVICE_BASE_URL=https://applifting-python-excercise-ms.herokuapp.com/api/v1`

Run the following bash command
 
```bash
docker-compose -f stack-production.yml up
```

Docker builds the following containers:
- postgres database
- redis
- Flask application
- Celery worker



## API

Api is served on address `0.0.0.0:5000`, equipped with Swagger documentation.




