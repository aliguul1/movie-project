import os
from sqlalchemy import create_engine, text

# PEP 8: Path constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "movies.db")
DB_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DB_URL, echo=False, connect_args={'timeout': 15})


def create_table():
    """Initializes schema with Users and Movies."""
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """))
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster TEXT,
                notes TEXT,
                imdb_id TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """))
        connection.commit()


create_table()


def get_users():
    """Returns all users as a dictionary {id: name}."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name FROM users"))
        return {row[0]: row[1] for row in result}


def add_user(name):
    """Adds a new user profile."""
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(
                text("INSERT OR IGNORE INTO users (name) VALUES (:n)"),
                {"n": name}
            )


def list_movies(user_id):
    """Retrieves all movies for a specific user ID."""
    with engine.connect() as connection:
        result = connection.execute(
            text("""SELECT title, year, rating, poster, notes, imdb_id 
                    FROM movies WHERE user_id = :u_id"""),
            {"u_id": user_id}
        )
        movies = result.fetchall()
    return {
        row[0]: {
            "year": row[1], "rating": row[2],
            "poster": row[3], "notes": row[4], "imdb_id": row[5]
        } for row in movies
    }


def add_movie(user_id, title, year, rating, poster, imdb_id):
    """Inserts a new movie record."""
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(
                text("""INSERT INTO movies (user_id, title, year, rating, poster, imdb_id) 
                        VALUES (:u_id, :t, :y, :r, :p, :imdb)"""),
                {"u_id": user_id, "t": title, "y": year, "r": rating, "p": poster, "imdb": imdb_id}
            )


def update_movie(user_id, title, notes):
    """Updates the personal note for a movie."""
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(
                text("""UPDATE movies SET notes = :n 
                        WHERE title = :t AND user_id = :u_id"""),
                {"n": notes, "t": title, "u_id": user_id}
            )


def delete_movie(user_id, title):
    """Deletes a movie record."""
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(
                text("DELETE FROM movies WHERE title = :t AND user_id = :u_id"),
                {"t": title, "u_id": user_id}
            )