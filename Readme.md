# AI Application Categorizer

## Project Overview

The AI Application Categorizer is a system designed to automatically determine the primary category and an associated energy consumption tag for software applications based on information gathered from various online data sources. In an increasingly complex digital landscape with a vast and ever-growing number of applications, efficient and accurate categorization is crucial for various purposes, including:

*   **Content Organization:** Helping users discover relevant applications in app stores and software repositories.
*   **Resource Management:** Estimating potential resource usage (like energy consumption) based on application type.
*   **Data Analysis:** Enabling large-scale analysis of application trends and usage patterns.
*   **Automated Curation:** Facilitating the automated curation and management of software libraries.

The scope of this system currently includes a predefined set of categories (e.g., Game, Utility, Development Tools, etc.) and assigns one of three energy labels (Low, Medium, High) based on the determined category. The primary intended use is for automated processing of application metadata to enrich existing software catalogs.

## Literature Review / Background

Application categorization has traditionally relied on manual tagging or simple rule-based systems based on keywords in application titles or descriptions. These approaches are often limited by the diversity of language used to describe applications and the subjective nature of categorization.

More advanced techniques have emerged, including:

*   **Keyword Mapping:** Employing keyword mapping techniques to find the most optimized meaningfull category with respect irregular tags.
*   **Semantic Similarity:** Leveraging pre-trained language models to understand the underlying meaning of text and determine similarity to category descriptions, even if exact keywords are not present.

This project fits within the realm of AI-enhanced categorization by combining rule-based methods, and semantic similarity. It distinguishes itself by prioritizing direct keyword mapping when clear and unambiguous, while employing a lightweight semantic similarity model (`sentence-transformers/all-MiniLM-L6-v2`) as a robust fallback and for handling cases with multiple potential keyword matches or no direct matches. This hybrid approach aims to balance accuracy with computational efficiency.

## Methodology

The application categorization process follows a multi-step pipeline:

1.  **Data Collection:** The system retrieves relevant categorization information (primarily tags and source information) for a given application from a variety of online data sources. As seen in the project structure, dedicated modules exist for sources like Apple Store, Flathub, Gog, Itch.io, My Abandonware, and Snap.
2.  **Preprocessing:** The raw category information obtained from different sources is normalized. This involves standardizing text, handling variations in capitalization and punctuation, and potentially removing irrelevant terms. The `normalize_category` function in `utils/helpers.py` is likely used for this purpose.
    *   **Example:** Input categories like "Action-Game", "action game", and "ACTION" would be normalized to a consistent format, potentially "action game" or "action".
3.  **Keyword Mapping:** The normalized categories are compared against a predefined list of keywords and their corresponding static categories. This step prioritizes direct matches. The `keyword_mapping` function in `utils/helpers.py` is likely responsible for this.
    *   **Example:** If a normalized category is "puzzle game" and there is a direct mapping for "puzzle game" to the "Game" static category, this mapping is considered.
4.  **Semantic Similarity:** If direct keyword mapping is ambiguous (multiple matches) or fails to yield a confident category, the system employs semantic similarity. The `sentence-transformers/all-MiniLM-L6-v2` model is loaded [1] and used to generate embeddings for the application's raw categories and the predefined static categories. The cosine similarity between these embeddings is then calculated to determine the most semantically similar category.
    *   **Example:** If the raw categories are "tool for developers" and "utility for coders", and keyword mapping is unclear, the semantic model would likely identify strong similarity to the "Development Tools" static category.
5.  **Decision Logic and Fallback:** A confidence threshold is applied during the AI-enhanced categorization [1]. If the semantic similarity score for the best match is below this threshold, a fallback strategy is implemented. As indicated in the code snippet [1], if a game source exists and confidence is low, the category defaults to "Game". Otherwise, it defaults to "Others". This layered approach ensures a category is assigned even when the initial methods are inconclusive.
6.  **Energy Tag Assignment:** Once the main category is determined, an energy consumption tag (Low, Medium, High) is assigned based on a mapping between categories and energy tags defined in `config.py`. This step is a direct lookup based on the finalized category.
    *   **Example:** If the main category is "Game", the system might assign a "High" energy tag based on the `ENERGY_TAGS` mapping in `config.py`.

The core logic of this pipeline, including data fetching, category selection, and energy tag assignment, is designed to be reusable for both single application processing and batch processing [3].

## Algorithms

The categorization process employs a combination of algorithms, each serving a specific purpose:

1.  **Rule-Based Mapping:**
    *   **Application:** Directly assigning categories based on specific, unambiguous rules, such as identifying "Game" for applications originating from sources like Gog, Itch.io, and My Abandonware [1].
    *   **Decision Logic:** Simple conditional checks based on predefined criteria.
    *   **Pseudocode:**

 ```python
    IF source is in ["Gog", "Itch.io", "My Abandonware"]:
        return "Game"


2.  **Keyword Mapping ():**
    *   **Application:** Matching normalized input categories to a predefined set of keywords associated with static categories.
    *   **Decision Logic:** Look up normalized input in a keyword-to-category map. If multiple matches occur, or no direct match is found, proceed to semantic similarity.
    *   **Pseudocode (Simplified):**

 ```python
    normalized_category = normalize(raw_category)
    potential_categories = lookup_in_keyword_map(normalized_category)

    IF count(potential_categories) == 1:
        return the single category
    ELSE IF count(potential_categories) > 1 OR count(potential_categories) == 0:
        proceed to Semantic Similarity

3.  **Semantic Similarity:**
    *   **Application:** Measuring the conceptual similarity between the input categories and the static categories using embeddings generated by a pre-trained language model (`sentence-transformers/all-MiniLM-L6-v2`).
    *   **Decision Logic:** Calculate cosine similarity between the embeddings. The static category with the highest similarity score above a defined `confidence_threshold` is selected.
    *   **Pseudocode (Simplified):**

 ```python
    input_embedding = model.encode(raw_categories)
    static_category_embeddings = {cat: model.encode(cat) for cat in static_categories}

    best_match_category = None
    highest_similarity = -1

    FOR each static_category, static_embedding in static_category_embeddings:
        similarity = cosine_similarity(input_embedding, static_embedding)
        IF similarity > highest_similarity:
            highest_similarity = similarity
            best_match_category = static_category

    IF highest_similarity >= confidence_threshold:
        return best_match_category
    ELSE:
        apply Fallback Strategy


4.  **Fallback Strategy:**
    *   **Application:** Providing a default category when the confidence from other methods is low.
    *   **Decision Logic:** If the confidence is below the threshold and a "game source" was identified, assign "Game". Otherwise, assign "Others".
    *   **Pseudocode:**

 ```python
    IF confidence < confidence_threshold:
        IF game_source_exists:
            return "Game"
        ELSE:
            return "Others"

## Evaluation

(This section requires specific data and results not fully present in the provided code snippets. The following is a template based on standard academic evaluation practices.)

Evaluation of the AI Application Categorizer was conducted on a dataset of [Describe the size and source of the dataset, e.g., 1000 applications with manually assigned gold-standard categories]. The dataset included a diverse range of applications spanning the defined categories.

The primary metrics used for evaluation were:

*   **Overall Accuracy:** The percentage of applications for which the system correctly predicted the main category.
*   **Per-Category Accuracy:** The accuracy of predictions for each individual category, highlighting strengths and weaknesses for specific application types.
*   **Confusion Matrix:** To visualize misclassifications between categories.

**Results:**

*   [Present key accuracy figures, e.g., "The system achieved an overall accuracy of X%."].
*   [Discuss per-category performance, e.g., "Accuracy was highest for 'Game' (Y%) and lowest for 'Others' (Z%)."].
*   [Analyze the confusion matrix to identify common misclassifications, e.g., "The most frequent misclassification was between 'Utility' and 'Productivity'"].

**Strengths:**

*   The hybrid approach effectively combines the efficiency of rule-based and keyword matching with the robustness of semantic similarity.
*   The use of a lightweight sentence transformer model balances performance with computational cost.
*   The fallback strategy ensures a category is always assigned.

**Limitations:**

*   Performance is dependent on the quality and coverage of the keyword mappings.
*   The confidence threshold requires tuning based on desired precision and recall trade-offs.
*   The semantic model's performance is limited by its training data and size.
*   The current dataset size for evaluation might not fully represent the diversity of real-world applications.

**Possible Improvements:**

*   Expand and refine the keyword mapping list.
*   Experiment with different confidence threshold values.
*   Investigate the use of larger or fine-tuned language models for semantic similarity.
*   Augment the evaluation dataset for broader coverage.

## How to Use

### For Single Application
python main.py "{application_name}
*   For detailed output with explanation, you need to uncomments all the prints

### For File 
python main.py -i {file name e.g app_list.txt} -o {desired output file name e.g categorized_app_list.csv}

