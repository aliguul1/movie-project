import requests
import movie_storage_sql as storage

# Recommendation: Keep your API key in a constant or environment variable
API_KEY = "29bc9a20"


def fetch_movie_from_api(title):
    """
    Fetches movie details from OMDb API.
    Handles 'Movie not found' and connection errors.
    """
    # Use params dictionary for cleaner URL construction
    url = "http://www.omdbapi.com/"
    params = {"apikey": API_KEY, "t": title}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                # Extract year safely (handles '2024–' or '2024–2026')
                "year": int(data.get("Year")[:4]) if data.get("Year") else 0,
                # Convert 'N/A' ratings to 0
                "rating": float(data.get("imdbRating") if data.get("imdbRating") != "N/A" else 0),
                # Fetch the Poster URL
                "poster": data.get("Poster") if data.get("Poster") != "N/A" else None
            }
        else:
            print(f"API Error: {data.get('Error')}")
            return None

    except requests.exceptions.ConnectionError:
        print("Error: Internet connection lost. Please check your network.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None


def command_add_movie():
    """Fetches movie data from API and adds it to the database with poster."""
    title_input = input("Enter movie title: ").strip()
    if not title_input:
        return

    print(f"Searching OMDb for '{title_input}'...")
    movie_data = fetch_movie_from_api(title_input)

    if movie_data:
        print(f"Found: {movie_data['title']} ({movie_data['year']})")
        print(f"Rating: {movie_data['rating']} | Poster: {movie_data['poster']}")

        # In this version, we'll auto-add it (or keep your confirm prompt)
        storage.add_movie(
            movie_data['title'],
            movie_data['year'],
            movie_data['rating'],
            movie_data['poster']  # Pass the new poster field
        )
    else:
        print("Could not retrieve movie data.")


def command_list_movies():
    """Retrieve and display movies including posters."""
    movies = storage.list_movies()
    if not movies:
        print("No movies found.")
        return

    print(f"\n{len(movies)} movies in total:")
    for title, data in movies.items():
        # Displaying poster URL if it exists
        poster_info = f" [Poster: {data['poster']}]" if data['poster'] else ""
        print(f"{title} ({data['year']}): {data['rating']}{poster_info}")


# --- Statistics and Delete remain functionally the same ---

def command_delete_movie():
    title = input("Enter movie title to delete: ").strip()
    storage.delete_movie(title)


def command_update_movie():
    """Manual update - as requested, left as is."""
    title = input("Enter movie title to update: ").strip()
    while True:
        try:
            rating = float(input("Enter new rating: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    storage.update_movie(title, rating)


def command_statistics():
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return
    ratings = [data["rating"] for data in movies.values()]
    print(f"Average rating: {sum(ratings) / len(ratings):.2f}")
    print(f"Highest rating: {max(ratings)}")
    print(f"Lowest rating: {min(ratings)}")


def print_menu():
    print("\nMovie App Menu")
    print("1. List movies")
    print("2. Add movie (via API)")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Statistics")
    print("0. Exit")


def main():
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
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
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()