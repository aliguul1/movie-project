from sqlalchemy import create_engine, text

DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL, echo=False) # echo=False for cleaner terminal output

def create_table():
    """Initializes the database and ensures the schema is up to date."""
    with engine.connect() as connection:
        # We add 'poster' as a TEXT column
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster TEXT
            )
        """))
        
        # Check if the 'poster' column exists, and add it if it doesn't
        # This handles cases where the table was created before the 'poster' column was added
        cursor = connection.execute(text("PRAGMA table_info(movies)"))
        columns = [row[1] for row in cursor.fetchall()]
        if "poster" not in columns:
            connection.execute(text("ALTER TABLE movies ADD COLUMN poster TEXT"))
            
        connection.commit()

# Run the create_table function immediately
create_table()

def list_movies():
    """Retrieve all movies including the poster URL."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster FROM movies")
        )
        movies = result.fetchall()

    # row[3] is the new poster field
    return {
        row[0]: {
            "year": row[1],
            "rating": row[2],
            "poster": row[3]
        } for row in movies
    }

def add_movie(title, year, rating, poster):
    """Add a new movie with data fetched from the API."""
    with engine.connect() as connection:
        with connection.begin(): # Using begin() for safer transactions
            try:
                connection.execute(
                    text("""
                        INSERT INTO movies (title, year, rating, poster)
                        VALUES (:title, :year, :rating, :poster)
                    """),
                    {"title": title, "year": year, "rating": rating, "poster": poster}
                )
                print(f"Movie '{title}' added successfully.")
            except Exception as e:
                print(f"Error adding movie: {e}")

def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        with connection.begin():
            result = connection.execute(
                text("DELETE FROM movies WHERE title = :title"),
                {"title": title}
            )
            if result.rowcount == 0:
                print(f"Movie '{title}' not found.")
            else:
                print(f"Movie '{title}' deleted successfully.")

def update_movie(title, rating):
    """Manually update a movie rating (as requested to leave as-is)."""
    with engine.connect() as connection:
        with connection.begin():
            result = connection.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"rating": rating, "title": title}
            )
            if result.rowcount == 0:
                print(f"Movie '{title}' not found.")
            else:
                print(f"Update successful.")