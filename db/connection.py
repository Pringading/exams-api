from pg8000.native import Connection
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def connect_to_db() -> Connection:
    """returns pg8000 database connection."""

    return Connection(
        user = getenv('USERNAME'),
        database = getenv('DATABASE'),
        password = getenv('PASSWORD'),
        host = getenv('HOST'),
        port = getenv('PORT')
    )