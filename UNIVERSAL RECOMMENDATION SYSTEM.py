import math


items = {
    # Movies
    101: {"title": "The Matrix", "type": "movie", "genres": ["Sci-Fi", "Action"], "price": 9.99},
    102: {"title": "Inception", "type": "movie", "genres": ["Sci-Fi", "Thriller"], "price": 8.99},
    103: {"title": "Interstellar", "type": "movie", "genres": ["Sci-Fi", "Adventure"], "price": 7.99},

    # Books
    201: {"title": "Harry Potter and the Sorcerer's Stone", "type": "book", "genres": ["Fantasy", "Adventure"], "price": 12.99},
    202: {"title": "The Hobbit", "type": "book", "genres": ["Fantasy", "Adventure"], "price": 10.99},
    203: {"title": "The Da Vinci Code", "type": "book", "genres": ["Mystery", "Thriller"], "price": 9.99},

    # Products
    301: {"title": "Wireless Headphones", "type": "product", "category": "Electronics", "price": 59.99},
    302: {"title": "Smart Watch", "type": "product", "category": "Electronics", "price": 129.99},
    303: {"title": "Coffee Maker", "type": "product", "category": "Home Appliances", "price": 49.99},
    304: {"title": "Yoga Mat", "type": "product", "category": "Fitness", "price": 24.99},
    305: {"title": "Bluetooth Speaker", "type": "product", "category": "Electronics", "price": 39.99},
}


user_ratings = {
    "Alice": {101: 5, 102: 4, 201: 5, 301: 4},
    "Bob": {103: 5, 202: 4, 302: 5, 304: 3},
    "Charlie": {102: 5, 203: 4, 303: 5, 305: 4}
}


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    common = set(vec1) & set(vec2)
    if not common:
        return 0

    dot_product = sum(vec1[i] * vec2[i] for i in common)
    magnitude1 = math.sqrt(sum(r ** 2 for r in vec1.values()))
    magnitude2 = math.sqrt(sum(r ** 2 for r in vec2.values()))

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot_product / (magnitude1 * magnitude2)

def get_similar_users(target_user, all_ratings):
    similarities = {}
    target = all_ratings.get(target_user, {})
    if not target:
        return []

    for user, ratings in all_ratings.items():
        if user != target_user:
            sim = cosine_similarity(target, ratings)
            if sim > 0:
                similarities[user] = sim

    return sorted(similarities.items(), key=lambda x: x[1], reverse=True)

def recommend_items(target_user, all_ratings, items_db, n=5, item_type=None):
    ratings = all_ratings.get(target_user, {})
    if not ratings:
        # Recommend most rated items for new user
        popularity = [
            (i, sum(i in r for r in all_ratings.values()))
            for i, info in items_db.items()
            if not item_type or info["type"] == item_type
        ]
        popularity.sort(key=lambda x: x[1], reverse=True)
        return [
            {**items_db[i], "id": i, "reason": "Popular item"}
            for i, _ in popularity[:n]
        ]

    recommendations = {}
    for user, sim in get_similar_users(target_user, all_ratings):
        for i, r in all_ratings[user].items():
            if i in ratings or (item_type and items_db[i]["type"] != item_type):
                continue
            if i not in recommendations:
                recommendations[i] = {"weighted_sum": 0, "similarity_sum": 0}
            recommendations[i]["weighted_sum"] += sim * r
            recommendations[i]["similarity_sum"] += sim

    predicted = [
        (i, rec["weighted_sum"] / rec["similarity_sum"])
        for i, rec in recommendations.items() if rec["similarity_sum"] > 0
    ]
    predicted.sort(key=lambda x: x[1], reverse=True)
    return [
        {**items_db[i], "id": i, "predicted_rating": round(r, 2), "reason": "Recommended based on similar users"}
        for i, r in predicted[:n]
    ]


def display_items(db, item_type=None):
    print("\nAvailable Items:")
    print("ID   | Type      | Title")
    print("-----------------------------")
    for i, info in db.items():
        if item_type and info["type"] != item_type:
            continue
        desc = ", ".join(info.get("genres", [])) if "genres" in info else info.get("category", "")
        print(f"{i:<4} | {info['type']:<9} | {info['title']} ({desc}) ${info['price']}")

def display_user_ratings(user, ratings, db):
    print(f"\n{user}'s Ratings:")
    for i, r in ratings.get(user, {}).items():
        info = db.get(i, {"title": "Unknown", "type": "unknown"})
        print(f"- {info['title']} ({info['type']}): {r}/5")


def create_new_user(ratings, db):
    print("\nCreate New User Profile")
    name = input("Enter your name: ").strip()
    if not name:
        print("Invalid name!")
        return None

    if name in ratings:
        print(f"Welcome back, {name}!")
        return name

    ratings[name] = {}
    print("Rate some items to get recommendations.")
    while True:
        display_items(db)
        try:
            i = int(input("\nEnter item ID to rate (0 to stop): "))
            if i == 0:
                break
            if i not in db:
                print("Invalid ID.")
                continue
            r = int(input(f"Your rating for '{db[i]['title']}' (1-5): "))
            if 1 <= r <= 5:
                ratings[name][i] = r
                print(f"Recorded: {db[i]['title']} - {r}/5")
            else:
                print("Rating must be 1-5.")
        except ValueError:
            print("Enter a valid number.")
    return name


# Main Program Loop

def main_menu():
    print("\nUNIVERSAL RECOMMENDATION SYSTEM")
    print("1. View all items")
    print("2. View movies")
    print("3. View books")
    print("4. View products")
    print("5. Create new user profile")
    print("6. Login as existing user")
    print("7. Get recommendations")
    print("8. View my ratings")
    print("9. Exit")
    try:
        return int(input("Choose an option: "))
    except ValueError:
        return -1


# Entry Point

if __name__ == "__main__":
    current_user = None
    print("Welcome to the Universal Recommendation System!")

    while True:
        choice = main_menu()

        if choice == 1:
            display_items(items)
        elif choice == 2:
            display_items(items, "movie")
        elif choice == 3:
            display_items(items, "book")
        elif choice == 4:
            display_items(items, "product")
        elif choice == 5:
            current_user = create_new_user(user_ratings, items)
        elif choice == 6:
            name = input("Enter username: ").strip()
            if name in user_ratings:
                current_user = name
                print(f"Welcome back, {current_user}!")
            else:
                print("User not found.")
        elif choice == 7:
            if not current_user:
                print("Please login or create a profile.")
                continue
            print("What would you like recommendations for?")
            print("1. All items\n2. Movies\n3. Books\n4. Products")
            try:
                t = int(input("Choice: "))
                type_map = {2: "movie", 3: "book", 4: "product"}
                t_type = type_map.get(t)
                recs = recommend_items(current_user, user_ratings, items, 5, t_type)
                if not recs:
                    print("Please rate more items.")
                else:
                    for r in recs:
                        print(f"- {r['title']} ({r['type']}) ${r['price']} - {r['reason']}")
            except ValueError:
                print("Invalid input.")
        elif choice == 8:
            if current_user:
                display_user_ratings(current_user, user_ratings, items)
            else:
                print("Please login or create a profile.")
        elif choice == 9:
            print("Thank you for using the system!")
            break
        else:
            print("Invalid option. Please choose 1–9.")
