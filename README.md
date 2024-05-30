# Read Me
This repository contains code for web scraping API scraping from the sites:
- https://www.scrapethissite.com/pages/ajax-javascript/#2015
- https://www.scrapethissite.com/pages/forms/
- https://www.scrapethissite.com/pages/advanced/

Following technologies have been used in this project:
- **BeautifulSoup** - For scraping websites
- **Python Requests Library** - To get websites
- **Django** - Python based web framework
- **PostgreSQL** - For data persistence with Django ORM
- **Celery** - Distributed task queue system for server offloading
- **Redis** - In-memory storage used as task broker for celery
- **Docker** - For deployment purposes

## Technical Requirements
- ### For local setup
  - Python 3.9+
  - pip 22+
  - a virtual envrionment (**venv** preffered)
  - Redis-server v7+
  - PostgreSQL v16.0+
- ### For Docker setup
  - Compose version v2.17+

## Setup
Firstly git clone the project to the local machine.

- ### Docker Setup
  The use of Docker images allows us to avoid installing all the dependencies—including PostgeSQL, Redis—locally.

  Docker container **does not** expect any existing environment file.
  To setup using docker compose:
  
  ```
  cd ./scrapingsite/
  docker compose up
  ```
- ### Local Setup
  Setup a ```.env``` file in the root directory of system.

  Should be setup as follows:
  ```
  CELERY_BROKER_URL=<redis_or_rabbitMQ_url>
  PG_USER=<postgresql_username>
  PG_PASSWORD=<postgresql_password>
  PG_DB=<postgresql_database_name>
  PG_PORT=<postgresql_port_no>
  PG_HOST=<postgresql_host>
  LOG_FILENAME=<log_filename>
  ```
  Then, again in the root directory setup python virtual environment and activate it:

  ```
  python -m venv .venv
  source ./.venv/scripts/activate
  ```
  Change directory to Project base i.e.,
  
  ```cd scrapingsite/```
  
  now install the requirements:
  
  ```pip -r install requirements.txt```

  migrate the database:
  
  ```python manage.py migrate```

  Finally, start the server:

  ```python manage.py runserver```

  To start celery service:

  ```celery -A scrapingsite worker -l INFO```
  
  Logs can be viewed in the file defined by the ```.env``` file.

## Functionality
  The code works by offloading the heavy scraping tasks off to the celery server, hence not blocking the main wsgi server thread.

  - For the link https://www.scrapethissite.com/pages/ajax-javascript/#2015:

    all the table data is stored and persisted and thereafter retrived
    
    ![image](https://github.com/Kyroyen/VakilDeskIntern/assets/70828054/e3c0cebf-2093-4529-ae7b-41c75b1500e2)

  - for link https://www.scrapethissite.com/pages/forms/
    
    all the table data is stored and persisted and thereafter retrived

    ![image](https://github.com/Kyroyen/VakilDeskIntern/assets/70828054/fc9a59be-43ad-401b-aeec-8a72e801c373)

  - for link https://www.scrapethissite.com/pages/advanced/

    Since it is a one off request, only success and failure of request is returned by the API, although data is still persisted

    ![image](https://github.com/Kyroyen/VakilDeskIntern/assets/70828054/c158f5c6-444e-45df-b396-362d94f76307)

  - Meanwhile in Celery terminal

    ![image](https://github.com/Kyroyen/VakilDeskIntern/assets/70828054/5409a8b4-01b3-40b2-86d0-88d967c730ce)


  API works as mentioned in the requirement.

## Code Quality
 - Readability : Code is written according to PEP 8 standard.
 - Modularity : Code is broken into indepentently functioning modules with consideration of low coupling and high cohesion among them.
 - Maintainibility : Code is maintainable with focus on easy changes in case of changes to the website structure such as headings, table tags etc.

## Error Handling
  With Robust error handling such as requests timeouts, decoding error, inconsistencies in data.

  - try-catch block wrapping of code at every instance of requests, decoding, database manipulation, etc.
  - logging of errors to log file using logging module.

## Data Persistence
  Data is persisted using PostgreSQL using Django ORM.
  - Sleep of 2 sec after every database insertion to avoid blocking the database
  - Collected data having high schema integrity would lead to better quality of analytics

## Performance Optimisation
  Performance is optimised with using Celery and Redis. Celery's ```@shared_tasks``` offload the resource heavy scraping tasks to the celery tasks queue, where they are executed without disturbing the main wsgi server.
  Hence the main server is free to handle other primary API server tasks such as serving requests, querying the database, etc.
  

