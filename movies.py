import os
import random
import statistics

import requests

from storage import movie_storage_sql as storage


def load_env_manually(filepath=".env"):
    """Loads environment variables from a .env file without libraries."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key.strip()] = value.strip()


# Security: Load key from environment
load_env_manually()
API_KEY = os.getenv("OMDB_API_KEY")

# Global session variables
current_user_id = None
current_user_name = ""


def fetch_movie_from_api(title):
    """OMDb API data fetcher."""
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
    try:
        res = requests.get(url, timeout=10).json()
        if res.get("Response") == "True":
            return {
                "title": res.get("Title"),
                "year": int(res.get("Year")[:4]),
                "rating": float(res.get("imdbRating") if res.get("imdbRating") != "N/A" else 0),
                "poster": res.get("Poster") if res.get("Poster") != "N/A" else None,
                "imdb_id": res.get("imdbID")
            }
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
    return None


def list_movies():
    """Option 1: Lists movies for current user."""
    movies = storage.list_movies(current_user_id)
    print(f"\n{len(movies)} movies in total:")
    for t, d in movies.items():
        print(f"{t} ({d['year']}): {d['rating']}")


def add_movie():
    """Option 2: Adds movie via API."""
    t = input("Enter movie name: ")
    data = fetch_movie_from_api(t)
    if data:
        storage.add_movie(current_user_id, **data)
        print(f"Movie {data['title']} successfully added")
    else:
        print(f"Error: Movie '{t}' not found.")


def delete_movie():
    """Option 3: Deletes movie with existence check."""
    t = input("Enter movie name to delete: ")
    movies = storage.list_movies(current_user_id)
    if t in movies:
        storage.delete_movie(current_user_id, t)
        print(f"Movie {t} successfully deleted")
    else:
        print(f"Error: Movie '{t}' does not exist.")


def update_movie():
    """Option 4: Updates movie note with existence check."""
    t = input("Enter movie name: ")
    movies = storage.list_movies(current_user_id)
    if t in movies:
        n = input("Enter movie note: ")
        storage.update_movie(current_user_id, t, n)
        print(f"Movie {t} successfully updated")
    else:
        print(f"Error: Movie '{t}' does not exist.")


def stats():
    """Option 5: Displays Average, Median, Best, and Worst ratings."""
    movies = storage.list_movies(current_user_id)
    if not movies:
        print("Add movies first!")
        return

    ratings = [m['rating'] for m in movies.values()]
    avg_val = sum(ratings) / len(ratings)
    med_val = statistics.median(ratings)

    sorted_m = sorted(movies.items(), key=lambda x: x[1]['rating'])

    print(f"Average rating: {avg_val:.2f}")
    print(f"Median rating: {med_val:.2f}")
    print(f"Best movie: {sorted_m[-1][0]} ({sorted_m[-1][1]['rating']})")
    print(f"Worst movie: {sorted_m[0][0]} ({sorted_m[0][1]['rating']})")


def random_movie():
    """Option 6: Random pick with rating."""
    movies = storage.list_movies(current_user_id)
    if movies:
        t, d = random.choice(list(movies.items()))
        print(f"Your movie for tonight: {t} ({d['rating']})")


def search_movie():
    """Option 7: Search with ratings."""
    q = input("Enter part of movie name: ").lower()
    movies = storage.list_movies(current_user_id)
    for t, d in movies.items():
        if q in t.lower():
            print(f"{t}: {d['rating']}")


def generate_website():
    """Option 9: Website generator using template in _static folder."""
    movies = storage.list_movies(current_user_id)
    if not movies:
        print("Add movies first!")
        return

    # Use absolute paths relative to this script's location
    base_dir = os.path.dirname(__file__)
    template_path = os.path.join(base_dir, "_static", "index_template.html")

    if not os.path.exists(template_path):
        print(f"Error: {template_path} not found.")
        return

    grid_html = ""
    for title, data in movies.items():
        # Feedback fix: ensure rating and notes are handled correctly for the grid
        poster = data.get('poster') or "https://via.placeholder.com/220x330"
        note = data.get('notes') or ""
        url = f"https://www.imdb.com/title/{data['imdb_id']}/"

        grid_html += f'''
        <li class="movie-card">
            <a href="{url}" target="_blank"><img src="{poster}"></a>
            <div class="movie-notes-overlay">{note}</div>
            <h3>{title}</h3><p>{data["year"]} - ⭐ {data["rating"]}</p>
        </li>\n'''

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        content = template.replace("__TEMPLATE_TITLE__", f"{current_user_name}'s Collection")
        content = content.replace("__TEMPLATE_MOVIE_GRID__", grid_html)

        # Saves the HTML in the main project folder
        output_file = os.path.join(base_dir, f"{current_user_name}.html")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Website generated successfully: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


def user_login():
    """Handles profile selection."""
    global current_user_id, current_user_name
    while True:
        print("\nWelcome to the Movie App! 🎬")
        users_dict = storage.get_users()
        user_list = list(users_dict.items())
        for i, (u_id, u_name) in enumerate(user_list, 1):
            print(f"{i}. {u_name}")
        print(f"{len(user_list) + 1}. Create new user")

        choice = input("\nSelect a user: ")
        try:
            idx = int(choice)
            if 1 <= idx <= len(user_list):
                current_user_id, current_user_name = user_list[idx - 1]
                break
            elif idx == len(user_list) + 1:
                new_name = input("Enter new user name: ").strip()
                if new_name:
                    storage.add_user(new_name)
                    users = storage.get_users()
                    for u_id, u_name in users.items():
                        if u_name == new_name:
                            current_user_id, current_user_name = u_id, u_name
                    break
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    """Main menu loop."""
    user_login()
    while True:
        print(f"\nMenu:")
        print("0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie")
        print("5. Stats\n6. Random movie\n7. Search movie\n8. Sort by rating")
        print("9. Generate website\n10. Switch User")

        choice = input("\nEnter choice (0-10): ")
        try:
            if choice == "1":
                list_movies()
            elif choice == "2":
                add_movie()
            elif choice == "3":
                delete_movie()
            elif choice == "4":
                update_movie()
            elif choice == "5":
                stats()
            elif choice == "6":
                random_movie()
            elif choice == "7":
                search_movie()
            elif choice == "8":
                movies = storage.list_movies(current_user_id)
                sorted_list = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
                for t, d in sorted_list:
                    print(f"{t}: {d['rating']}")
            elif choice == "9":
                generate_website()
            elif choice == "10":
                user_login()
            elif choice == "0":
                print("Bye!")
                break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()