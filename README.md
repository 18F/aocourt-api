# Administrative Office of the Courts E&I

This is a small API service to support the AO's E&I.

## Requirements  
To run locally you will need access to Python 3.6 or higher. You will also need access to a database like PostgreSQL, although SQLite, available on most systems, will work for local development and tests.

For development, some familiarity with the following libraries will be helpful:
- [SLQAlchemy](https://www.sqlalchemy.org): Database ORM (with the help of [Alembic](https://alembic.sqlalchemy.org/en/latest/) for DB migrations)
- [Ariadne](https://ariadne.readthedocs.io/en/0.3.0/): provides GraphQL support
- [FastAPI](https://fastapi.tiangolo.com): Web/API framework
- [Pydantic](https://pydantic-docs.helpmanual.io): Data validation and managing configuration/settings


## Installing locally  
To avoid installing dependencies in your global environment, create a virtual environment. You can replace `.venv` to any path where you want the environment files to live (just make sure you `source` the right place in the next step). However, placing it in the root directory of the project and naming it `.venv` will make some editors like VSCode load it automatically. 

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Install requirement into virtual env. 

```console
$ pip install -r requirements.txt
```

If this step gives you errors, make sure you are using a recent version of `pip`. You can make sure your venv has an up-to-date `pip` install with: `pip install -U pip`. 

To exit the virtual environment and get back to your original python env:

```console
$ deactivate
```

## Environment

The app expects to find a few environmental variables. An easy way to provide these is by creating a file called `.env` in the root directory and add them there. 

    SECRET_KEY=some_good_secret_for_signing_tokens
    DATABASE_URL=postgres://localhost:5432/some_database
    DATABASE_URL_TEST=postgresql://localhost:5432/some_test_database
    INITIAL_ADMIN_USER=initial_admin
    INITIAL_ADMIN_PASSWORD=their_password

Default values for these will be created in `app/core/config.py` but those defaults are probably not what you want.
## Initialize the database

This is designed to run Postgres, but should run on any database, including SQLite, that SQLAlchemy supports. 

The settings for the app will expect to find environmental variables for `DATABASE_URL` and `DATABASE_URL_TEST` containing connection strings to the databases. The test database is a convenience to allow you to run integration tests without messing up your seed data.

Creating and maintaining the database is currently done with alembic. Initial migrations are in `alembic/versions`. To run these use:

```console
$ alembic upgrade head
```

Future changes to the database schema should create further migrations. To create a migration file you can use alembic:

```console
$ alembic revision -m "some note about this migration"
```

Future changes to the database schema should create further migrations. 

## Starting

**In Development:**  
From the root directory run:

```console
$ uvicorn app.main:app
```

To auto-reload on change use:

```console
$ uvicorn app.main:app --reload
```
