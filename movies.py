import movie_storage_sql as storage


def command_list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()

    if not movies:
        print("No movies found.")
        return

    print(f"{len(movies)} movies in total:")
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def command_add_movie():
    """Prompt user for movie data and add it to the database."""
    title = input("Enter movie title: ").strip()
    
    while True:
        try:
            year = int(input("Enter release year: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for the year.")

    while True:
        try:
            rating = float(input("Enter rating (0-10): "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for the rating.")

    storage.add_movie(title, year, rating)


def command_delete_movie():
    """Delete a movie from the database."""
    title = input("Enter movie title to delete: ").strip()
    storage.delete_movie(title)


def command_update_movie():
    """Update a movie's rating."""
    title = input("Enter movie title to update: ").strip()
    
    while True:
        try:
            rating = float(input("Enter new rating: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for the rating.")

    storage.update_movie(title, rating)


def command_statistics():
    """Display basic movie statistics."""
    movies = storage.list_movies()

    if not movies:
        print("No movies available.")
        return

    ratings = [data["rating"] for data in movies.values()]

    avg_rating = sum(ratings) / len(ratings)
    highest = max(ratings)
    lowest = min(ratings)

    print(f"Average rating: {avg_rating:.2f}")
    print(f"Highest rating: {highest}")
    print(f"Lowest rating: {lowest}")


def print_menu():
    """Display the command menu."""
    print("\nMovie App Menu")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Statistics")
    print("0. Exit")


def main():
    """Main program loop."""
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
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
# Movies list1

# In the Name of the Father (1993): 8.1
# Titanic (1997): 6.6
# Venom (2018): 6.6
# Fallout (2024): 8.7
# Baby Reindeer (2024): 8.2
# Civil War (2024): 8.7
# Law Abiding Citizen (2009): 7.4
# Law & Order (1990): 7.8
# Law & Order: Special Victims Unit (1999): 8.1
# To Wong Foo, Thanks for Everything! Julie Newmar (1995): 6.7
# Emily in Paris (2020): 6.9
# 21 (2008): 6.8