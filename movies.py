import requests
import os
import random
from storage import movie_storage_sql as storage

API_KEY = "29bc9a20"


def fetch_movie_from_api(title):
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
    try:
        res = requests.get(url, timeout=10).json()
        if res.get("Response") == "True":
            return {
                "title": res.get("Title"),
                "year": int(res.get("Year")[:4]),
                "rating": float(res.get("imdbRating") if res.get("imdbRating") != "N/A" else 0),
                "poster": res.get("Poster") if res.get("Poster") != "N/A" else None
            }
    except:
        return None
    return None


def command_list_movies():
    movies = storage.list_movies()
    if not movies:
        print("No movies found.")
        return
    print(f"{len(movies)} movies in total:")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_add_movie():
    title = input("Enter movie title: ").strip()
    data = fetch_movie_from_api(title)
    if data:
        storage.add_movie(data['title'], data['year'], data['rating'], data['poster'])
        print(f"Added {data['title']}")
    else:
        print("Movie not found.")


def command_delete_movie():
    storage.delete_movie(input("Enter title to delete: "))


def command_update_movie():
    title = input("Enter title: ")
    try:
        rating = float(input("Enter new rating: "))
        storage.update_movie(title, rating)
    except ValueError:
        print("Invalid rating.")


def command_statistics():
    movies = storage.list_movies()
    if not movies: return
    ratings = [d['rating'] for d in movies.values()]
    print(f"Average: {sum(ratings) / len(ratings):.2f}, High: {max(ratings)}, Low: {min(ratings)}")


def command_random_movie():
    movies = storage.list_movies()
    if not movies: return
    title, data = random.choice(list(movies.items()))
    print(f"Your lucky movie: {title} ({data['year']})")


def command_search_movie():
    query = input("Enter part of movie name: ").lower()
    movies = storage.list_movies()
    found = [t for t in movies if query in t.lower()]
    for f in found:
        print(f"{f} ({movies[f]['year']}): {movies[f]['rating']}")


def command_sort_movies():
    movies = storage.list_movies()
    sorted_m = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for title, data in sorted_m:
        print(f"{title} ({data['year']}): {data['rating']}")


def command_generate_website():
    """Generates MyMovieApp.html inside the _static directory."""
    movies = storage.list_movies()
    if not movies: return

    grid_html = ""
    for title, data in movies.items():
        poster = data.get('poster') or "https://via.placeholder.com/220x330"
        grid_html += f'''<div class="movie-card">
            <img src="{poster}" alt="{title} poster">
            <h3>{title}</h3>
            <p>{data["year"]}</p>
        </div>\n'''

    root_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(root_dir, "_static")
    template_path = os.path.join(static_dir, "index_template.html")
    output_path = os.path.join(static_dir, "MyMovieApp.html")

    try:
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()

        content = content.replace("__TEMPLATE_TITLE__", "My Movie App")
        content = content.replace("__TEMPLATE_MOVIE_GRID__", grid_html)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Success! Website saved as: {output_path}")
    except FileNotFoundError:
        print(f"Error: Could not find template at {template_path}")


def print_menu():
    print(
        "\nMenu:\n0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie\n5. Stats\n6. Random movie\n7. Search movie\n8. Movies sorted by rating\n9. Generate website")


def main():
    while True:
        print_menu()
        choice = input("\nEnter choice (0-9): ")
        if choice == "1":
            command_list_movies()
        elif choice == "2":
            command_add_movie()
        elif choice == "3":
            command_delete_movie()
        elif choice == "4":
            command_update_movie()
        elif choice == "5":
            command_statistics()
        elif choice == "6":
            command_random_movie()
        elif choice == "7":
            command_search_movie()
        elif choice == "8":
            command_sort_movies()
        elif choice == "9":
            command_generate_website()
        elif choice == "0":
            break


if __name__ == "__main__":
    main()