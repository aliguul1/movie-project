🎬 My Movie App
A robust, relational-database-driven Python application that allows users to manage their personal movie collections. The app features multi-user support, real-time data fetching from the OMDb API, and dynamic generation of a responsive website featuring personal notes and IMDB links.

✨ Key Features
Multi-User Management: Create and switch between different user profiles. Each user has their own private movie collection.

OMDb API Integration: Fetch movie titles, years, ratings, and posters automatically using the OMDb API.

Relational Database (SQLAlchemy): Utilizes a one-to-many schema to link movies to specific users, ensuring data integrity.

IMDB Integration: Clicking on a movie poster in the generated website takes you directly to its IMDB page.

Interactive Web Generation: Generates a custom HTML file for each user with a "Hover-for-Notes" feature, revealing personal reviews or thoughts.

Movie Insights: Built-in statistics (average rating, best/worst movies) and randomized suggestions.

🏗️ Project Architecture
The project follows a modular design, separating data persistence from business logic:

main.py: The "Controller." Handles the CLI menu, user interactions, API requests, and website generation.

movie_storage_sql.py: The "Data Layer." Manages SQLite connections and SQL queries via SQLAlchemy.

_static/: Contains the HTML/CSS template used to render the frontend.

data/: Stores the SQLite database file (movies.db).

🛠️ Installation & Setup
1. Prerequisites
Python 3.x

An OMDb API Key (available at omdbapi.com)

requests and sqlalchemy libraries

2. Install Dependencies
Bash
pip install requests sqlalchemy
3. Configuration
Open main.py and replace the API_KEY variable with your unique key:

Python
API_KEY = "your_key_here"
4. Running the App
Bash
python main.py
🎮 How to Use
Managing Your Movies
Add Movie: Enter a title; the app fetches data from the API and saves it to your profile.

Update Movie: Add personal notes to any movie (these appear as a green overlay on your website).

Stats & Sorting: View your average rating or sort your collection from highest to lowest score.

Generating Your Website
Choose Option 9 from the menu. The app will generate a file in the _static/ folder named [YourName].html. Open this file in any browser to view your interactive library.

📜 PEP 8 Compliance
This project strictly adheres to PEP 8 standards, including:

Consistent 4-space indentation.

Descriptive snake_case naming for functions and variables.

Clear separation of imports and function definitions.

Robust error handling (try-except blocks) for user input and API calls.

🚀 Future Improvements
Direct Search: Searching for movies on the website using JavaScript.

Genre Filtering: Expanding the database schema to include movie genres.

User Passwords: Adding basic security to user profiles.