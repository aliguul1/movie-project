import os
import random
import requests
from storage import movie_storage_sql as storage

API_KEY = "29bc9a20"
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
    except Exception as e:
        print(f"API Error: {e}")
    return None


def user_login():
    """User profile selection."""
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


def command_generate_website():
    """Option 9: Website generator with IMDB links and hover notes."""
    movies = storage.list_movies(current_user_id)
    if not movies:
        print("Add movies first!")
        return
    grid_html = ""
    for title, data in movies.items():
        poster = data.get('poster') or "https://via.placeholder.com/220x330"
        note = data.get('notes') or ""
        url = f"https://www.imdb.com/title/{data['imdb_id']}/"
        grid_html += f'''
        <li class="movie-card">
            <a href="{url}" target="_blank"><img src="{poster}"></a>
            <div class="movie-notes-overlay">{note}</div>
            <h3>{title}</h3><p>{data["year"]}</p>
        </li>\n'''

    root = os.path.dirname(os.path.abspath(__file__))
    t_path = os.path.join(root, "_static", "index_template.html")
    o_path = os.path.join(root, "_static", f"{current_user_name}.html")

    try:
        with open(t_path, "r", encoding="utf-8") as f:
            content = f.read().replace("__TEMPLATE_TITLE__", current_user_name)
            content = content.replace("__TEMPLATE_MOVIE_GRID__", grid_html)
        with open(o_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Website generated: {o_path}")
    except FileNotFoundError:
        print("Template file not found.")


def main():
    user_login()
    while True:
        print(f"\nMenu:")
        print("0. Exit\n1. List movies\n2. Add movie\n3. Delete movie\n4. Update movie")
        print("5. Stats\n6. Random movie\n7. Search movie\n8. Sort by rating")
        print("9. Generate website\n10. Switch User")

        choice = input("\nEnter choice (0-10): ")
        try:
            if choice == "1":
                movies = storage.list_movies(current_user_id)
                print(f"\n{len(movies)} movies in total:")
                for t, d in movies.items():
                    print(f"{t} ({d['year']}): {d['rating']}")
            elif choice == "2":
                t = input("Enter movie name: ")
                data = fetch_movie_from_api(t)
                if data:
                    storage.add_movie(current_user_id, **data)
                    print(f"Movie {data['title']} successfully added")
            elif choice == "3":
                t = input("Enter movie name to delete: ")
                storage.delete_movie(current_user_id, t)
                print(f"Movie {t} successfully deleted")
            elif choice == "4":
                t = input("Enter movie name: ")
                n = input("Enter movie note: ")
                storage.update_movie(current_user_id, t, n)
                print(f"Movie {t} successfully updated")
            elif choice == "5":
                movies = storage.list_movies(current_user_id)
                ratings = [m['rating'] for m in movies.values()]
                if ratings:
                    print(f"Average rating: {sum(ratings) / len(ratings):.2f}")
                    print(f"Best movie: {max(movies, key=lambda k: movies[k]['rating'])}")
            elif choice == "6":
                movies = storage.list_movies(current_user_id)
                if movies:
                    t = random.choice(list(movies.keys()))
                    print(f"Your movie for tonight: {t}")
            elif choice == "7":
                q = input("Enter part of movie name: ").lower()
                movies = storage.list_movies(current_user_id)
                for t in movies:
                    if q in t.lower(): print(t)
            elif choice == "8":
                movies = storage.list_movies(current_user_id)
                for t, d in sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True):
                    print(f"{t}: {d['rating']}")
            elif choice == "9":
                command_generate_website()
            elif choice == "10":
                user_login()
            elif choice == "0":
                print("Bye!")
                break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()