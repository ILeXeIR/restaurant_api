# Restaurant API
___
## Installation
**1.** Clone this repository.

**2.** Open the project folder and create .env file with the following environmental variables:
```commandline
POSTGRES_USER="<user>"
POSTGRES_PASSWORD="<password>"
POSTGRES_DB="<postgres_db>"
POSTGRES_HOST="restaurant_db"
```
You can choose any values for variables POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB.

You also may add variable POSTGRES_PORT.
It has default value 5432.

**3.** Run it with Docker-compose:
- Install Docker Compose
  (https://docs.docker.com/compose/install/)
- Run all containers with ```docker-compose up -d```

**4.** You can start all tests with command:
```docker-compose -f docker-compose-test.yaml up -d```
