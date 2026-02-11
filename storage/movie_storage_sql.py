import os
from sqlalchemy import create_engine, text

# Get project root and data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DB_PATH = os.path.join(DATA_DIR, "movies.db")
DB_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(DB_URL, echo=False)

def create_table():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster TEXT
            )
        """))
        connection.commit()

create_table()

def list_movies():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}

def add_movie(title, year, rating, poster):
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(
                text("INSERT INTO movies (title, year, rating, poster) VALUES (:t, :y, :r, :p)"),
                {"t": title, "y": year, "r": rating, "p": poster}
            )

def delete_movie(title):
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(text("DELETE FROM movies WHERE title = :t"), {"t": title})

def update_movie(title, rating):
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(text("UPDATE movies SET rating = :r WHERE title = :t"), {"r": rating, "t": title})
            connection.execute(text("UPDATE movies SET rating = :r WHERE title = :t"), {"r": rating, "t": title})