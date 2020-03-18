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

Run the following bash command
 
```bash
docker-compose -f stack-productin.yml up
```

Docker builds the following containers:
- postgres database
- redis
- Flask application
- Celery worker


## API

Api is served on address 0.0.0.0:5000, equipped with Swagger documentation.




