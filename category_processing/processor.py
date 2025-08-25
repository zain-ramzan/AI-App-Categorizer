"""
Category processing logic for the App Category Analyzer.
"""

from config import ENERGY_TAGS, STATIC_CATEGORIES
from utils.helpers import normalize_category, keyword_mapping


from sentence_transformers import SentenceTransformer, util

# Load lightweight model once
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def select_main_category(app_name, raw_categories, static_categories, confidence_threshold=0.3):
    """
    AI-enhanced categorization with confidence threshold:
    1. Immediately mark Gog, Itch.io, and My Abandonware sources as Game.
    2. Normalize and keyword map all other sources. Prioritize direct keyword mapping,
       but use AI if multiple direct matches occur.
    3. If a single direct mapping yields a clear category, return it.
    4. If multiple direct mappings or no direct mapping, use semantic similarity (AI).
    5. Fallback to Game if confidence is low and a game source exists, otherwise Others.
    """

    print(f"{app_name}: {raw_categories}")

    processed_categories = {}
    game_detected = False

    # STEP 1: Immediately mark known game sources
    for source, tags in raw_categories.items():
        if source in ["Gog", "Itch.io", "My Abandonware"]:
            processed_categories[source] = ["Game"]
            game_detected = True
        else:
            processed_categories[source] = tags

    # STEP 2: Normalize and keyword map for other sources, and prioritize direct mapping
    all_keywords = []
    direct_matches = [] # To store direct matches found in static categories

    for source, tags in processed_categories.items():
        if source in ["Gog", "Itch.io", "My Abandonware"]:
            continue

        normalized_tags = [normalize_category(tag) for tag in tags]
        mapped_tags = [keyword_mapping.get(tag, tag) for tag in normalized_tags]
        # Assuming you still want to title case the mapped tags as in your example
        mapped_tags = [tag.title() if isinstance(tag, str) else tag for tag in mapped_tags]


        print(f"[NORMALIZATION] Source: {source}")
        print(f"Raw Tags: {tags}")
        print(f"Normalized Tags: {normalized_tags}")
        print(f"Mapped Tags: {mapped_tags}")

        # Check for direct keyword mapping in static categories
        for mapped_tag in mapped_tags:
            if mapped_tag in static_categories:
                direct_matches.append(mapped_tag)
                print(f"[DIRECT MATCH] Found direct mapping to '{mapped_tag}' in static categories")


        all_keywords.extend(mapped_tags) # Always add mapped tags to all_keywords for potential AI step


    # Check the number of unique direct matches
    unique_direct_matches = list(set(direct_matches))

    if len(unique_direct_matches) == 1:
        # If exactly one direct match, return it
        print(f"[FINAL DECISION] Found single direct mapping to '{unique_direct_matches[0]}', returning it.")
        return unique_direct_matches[0]
    elif len(unique_direct_matches) > 1:
        # If multiple direct matches, proceed to AI step
        print(f"[MULTIPLE DIRECT MATCHES] Found multiple direct matches: {unique_direct_matches}. Proceeding to AI semantic similarity.")
        # Continue to STEP 3 (AI semantic similarity)
    else:
        # If no direct matches, proceed to AI step (as before)
        print("[NO DIRECT MATCHES] No direct matches found. Proceeding to AI semantic similarity.")
        # Continue to STEP 3 (AI semantic similarity)


    # STEP 3: AI semantic similarity (only if no single direct mapping was found)
    # Ensure all_keywords is not empty before proceeding to AI
    if not all_keywords and game_detected:
        print("[GAME FALLBACK] No keywords for AI, returning 'Game'")
        return "Game"
    elif not all_keywords:
        print("[FALLBACK] No keywords for AI, returning 'Others'")
        return "Others"

    # Eliminate duplicate keywords
    unique_keywords = list(set(all_keywords))
    print(f"[AI SEMANTIC MATCH] Unique keywords for AI: {unique_keywords}")


    query_text = f"{app_name} {' '.join(unique_keywords)}" # Use unique_keywords
    query_embedding = model.encode(query_text, convert_to_tensor=True)
    category_embeddings = model.encode(list(static_categories), convert_to_tensor=True)

    similarities = util.cos_sim(query_embedding, category_embeddings)[0]

    # Calculate and print confidence for every category
    print("[AI SEMANTIC MATCH] Confidence scores for each static category:")
    category_confidence = {}
    for i, category in enumerate(static_categories):
        confidence = similarities[i].item()
        category_confidence[category] = confidence
        # print(f"  {category}: {confidence:.4f}")

    # Find the best category and confidence (highest-ranking)
    best_index = similarities.argmax().item()
    best_category = list(static_categories)[best_index]
    confidence = similarities[best_index].item()


    print(f"[AI SEMANTIC MATCH] Highest-ranking category: '{best_category}' with confidence {confidence:.4f}")
    print(best_category)

    # STEP 4: Apply confidence threshold
    if confidence >= confidence_threshold:
        print(f"[FINAL DECISION] Using AI-selected category '{best_category}' (confidence above threshold)")
        return best_category
    elif game_detected:
        print("[FINAL DECISION] Confidence below threshold, fallback to 'Game'")
        return "Game"
    else:
        print("[FINAL DECISION] Confidence below threshold, fallback to 'Others'")
        return "Others"



def assign_energy_tag(main_category):
    """
    Assign an energy tag based on main category.

    Args:
        main_category (str): Selected main category

    Returns:
        str: Energy tag
    """
    for key, energy_tag in ENERGY_TAGS.items():
        if key == main_category:
            return energy_tag

    # Fallback for categories not found in ENERGY_TAGS (should ideally not happen with the static categories)
    return "Low/Medium Energy Consumption" # Default to Low/Medium as per your note for "Others"
