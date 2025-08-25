import re


keyword_mapping = {
    "games": "Game",
    "game": "Game",
    "3d graphic": "Graphics & Design",
    "graphic": "Graphics & Design",
    "graphics": "Graphics & Design",
    "photo": "Photo & Video",
    "audio": "Music",
    "photography": "Photo & Video",
    "video": "Photo & Video",
    "video conference": "Photo & Video",
    "network": "Utilities",
    "utility": "Utilities",
    "tools": "Utilities",
    "health fitness": "Health & Fitness",
    "food drink": "Food & Drink",
    "social": "Social Networking",
    "development": "Developer Tool",
    "magazines newspapers": "Magazines & Newspapers",
}


def normalize_category(category_string):
    """
    Normalize a category or tag string by lowercasing, removing special characters,
    and applying specific replacement rules.
    """
    # Use regular expression to find capital letters not at the start of the string
    # and add a space before them
    normalized_string = re.sub(r'(?<!\s)(?=[A-Z])', ' ', category_string)

    # Lowercase the string
    normalized_string = normalized_string.lower().replace('-', ' ').replace('_', ' ')

    # Remove special characters (keep letters, numbers, and spaces)
    normalized_string = re.sub(r'[^a-zA-Z0-9\s&]', '', normalized_string)

    # Remove leading/trailing whitespace and reduce multiple spaces to a single space
    normalized_string = re.sub(r'\s+', ' ', normalized_string).strip()

    return normalized_string

