# Headers for Snapcraft API
SNAP_HEADERS = {
    "Snap-Device-Series": "16",
    "User-Agent": "SnapInfoCLI/1.0",
    "Accept": "application/json"
}

# General headers for other requests
GENERAL_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Predefined static categories
STATIC_CATEGORIES = {
    "Books",
    "Web Browser",
    "Business",
    "Developer Tool",
    "Education",
    "Entertainment",
    "Finance",
    "Food & Drink",
    "Game",
    "Graphics & Design",
    "Health & Fitness",
    "Kids",
    "Lifestyle",
    "Magazines & Newspapers",
    "Medical",
    "Music",
    "Navigation",
    "News",
    "Photo & Video",
    "Productivity",
    "Shopping",
    "Social Networking",
    "Sports",
    "Travel",
    "Utilities",
    "Weather"
}

# Energy tag mapping based on static category
ENERGY_TAGS = {
    "Game": "High Energy Consumption",
    "Graphics & Design": "High Energy Consumption",
    "Photo & Video": "High Energy Consumption",
    "Entertainment": "High Energy Consumption", # e.g., video streaming platforms
    "Navigation": "High Energy Consumption", # real-time GPS and maps
    "Social Networking": "High Energy Consumption", # constant background updates, media-heavy content

    "Developer Tool": "Medium Energy Consumption",
    "Productivity": "Medium Energy Consumption",
    "Health & Fitness": "Medium Energy Consumption",
    "Shopping": "Medium Energy Consumption",
    "Sports": "Medium Energy Consumption",
    "Travel": "Medium Energy Consumption",
    "Utilities": "Medium Energy Consumption",
    "Web Browser": "Medium Energy Consumption",
    "News": "Medium Energy Consumption",
    "Finance": "Medium Energy Consumption",
    "Food & Drink": "Medium Energy Consumption",

    "Books": "Low Energy Consumption",
    "Business": "Low Energy Consumption", # unless heavy analytics
    "Education": "Low Energy Consumption",
    "Kids": "Low Energy Consumption",
    "Lifestyle": "Low Energy Consumption",
    "Music": "Low Energy Consumption", # music streaming can be high, but local playback is low
    "Magazines & Newspapers": "Low Energy Consumption",
    "Medical": "Low Energy Consumption",
    "Weather": "Low Energy Consumption",
}