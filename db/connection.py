from pg8000.native import Connection
from os import getenv
from dotenv import load_dotenv


# loads environment variables from .env file
load_dotenv()


def connect_to_db() -> Connection:
    """returns pg8000 database connection.
    
    Uses environment variables: USERNAME, DATABASE, PASSWORD, HOST & PORT
    as defined in an .env file in the root directory."""

    return Connection(
        user = getenv('USERNAME'),
        database = getenv('DATABASE'),
        password = getenv('PASSWORD'),
        host = getenv('HOST'),
        port = getenv('PORT')
    )