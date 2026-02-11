# Movie Collection Project

A professional Python CLI application that manages a movie database and generates a visual web gallery.

## Features
- **SQL Storage**: Uses SQLAlchemy to manage data in a `/data` directory.
- **OMDb API**: Automatically fetches movie posters, years, and ratings.
- **Web Generation**: Creates a responsive HTML grid with a green banner.
- **CLI Tools**: Search, sort, and get statistics on your collection.

## Installation
1. Ensure you have Python 3.x installed.
2. Install dependencies:
   ```bash
   pip install sqlalchemy requests