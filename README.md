# Aryu Blog, REST API
Simple and practice project aimed at skill enhancement, utilizing and combining the various technologies listed below:

- **Python, Django Framework**
- **Django REST Framework**
- **Swagger, Redoc**
- **PostgreSQL, Redis**
- **Celery, RabbitMQ**
- **Simple JWT**
- **Gunicorn, Nginx**
- **Git, Gitflow, Docker**

## Description
This project is a REST API built with Django and DRF, featuring user management, a follower and following system, multiple authentication methods including JWT, post creation and editing, using search, pagination, and permissions, it includes query optimization, implementation of various database relationships and generics, caching and idempotency with Redis, the integration of Celery and RabbitMQ as a message broker, a soft delete system, Swagger and Redoc for documentation, Gunicorn and Nginx for deployment and serving static and media files, and Dockerization of the project.

## Commit Conventions
This repository uses special rules for commit messages. Syntax & Example:

    <type>(<scope>) : <message>
    <description>

    $ git commit -m "docs(readme): update project documention" -m "description"

Complete information: [commit conventions](https://github.com/aliaryu/aryu-blog/blob/feature/readme/docs/commit-conventions.md)

## How To Use
First, clone the project:

    https://github.com/aliaryu/aryu-blog.git

Secondly, you should create a **.env** file with contents similar to **.env.example** , (You can modify the **.env** configuration as needed, but be sure to update the **docker-compose.yml** file accordingly).

If you don't want to use docker, then **DEBUG** must be **True** (in **.env** file: **DEBUG=1**) , Now create the virtual environment for python (depends on OS) and execute the following commands in order:

    pip install -r requirements/development.txt
    python manage.py makemigrations
    python manage.py migrate

    # Run this command only once to load test data into the database.
    python manage.py loaddata fixtures/data.json

    python manage.py runserver

If you want to use docker, according to the **DEBUG** , you can run the following command:

    docker-compose build
    docker-compose up -d

    # Run this command only once to load test data into the database.
    docker-compose exec web python manage.py loaddata fixtures/data.json

After loading the data into the database and running the project, you can log in with a superuser account username: **`a@a.com`** and password: **1** to review the project.
