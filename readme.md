# 🌍 Geoapp-backend

## Overview

This project is a geospatial application built with Python[FastAPI], SQLAlchemy[GeoAlchemy], Postgresql[PostGIS] and Alembic. It uses asynchronous database operations to handle geospatial data efficiently.
It uses the data bundle from the PostGIS introduction [🏙️ PostGIS Workshop](https://postgis.net/workshops/postgis-intro/index.html)
The idea was to serve GeoJSON 🌍 from an asynchronous Python 🐍 backend using API endpoints 🚀.
The GeoJSON 🌍 should be parsed and rendered by a JavaScript 🖥️ frontend application and displayed in a web browser 🌐.
## Features

- 🚀 Asynchronous database operations with SQLAlchemy and asyncpg
- 🔄 Database migrations with Alembic
- 🗺️ Geospatial data handling

## Requirements

- 🐍 Python 3.9+ (Written in 3.13)
- 🐘 PostgreSQL with PostGIS extension
- `asyncpg` for asynchronous PostgreSQL operations
- `SQLAlchemy` for ORM
- `Alembic` for database migrations

## Installation

1. Clone the repository:

    ```sh
    git https://github.com/RobertRivas/geoapp-backend.git
    cd geoapp-backend
    ```

2. Create a virtual environment and activate it:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
refer to for local setup - [🏙️ PostGIS Workshop](https://postgis.net/workshops/postgis-intro/index.html)
    ```sh
    createdb nyc
    psql -d nyc -c "CREATE EXTENSION postgis;"
    ```


## Usage

1. Run database migrations:

    ```sh
    alembic upgrade head
    ```

2. Start the application:

    ```sh
    python main.py
    ```

## Project Structure

- 📂 `alembic/`: Directory for Alembic migrations
- 🗄️ `database/`: Database models and configuration
- 🚀 `main.py`: Main application entry point

## Alembic

To create a new migration, use:

```sh
alembic revision --autogenerate -m "description"
```

To apply migrations, use:

```sh
alembic upgrade head
```



