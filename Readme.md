## 3. Categorization Methodology

This section describes the comprehensive methodology employed for the automated categorization of applications sourced from various digital distribution platforms. The approach integrates multiple techniques to enhance accuracy and robustness, addressing the inconsistencies and variations in metadata across different sources. The primary objective is to assign each application to a single, most relevant category from a predefined set of static categories.

### 3.1 Static Category Set

A foundational element of this methodology is a curated set of static categories. These categories represent broad classifications designed to encompass a wide range of application types. This set is defined in `config.py` as `STATIC_CATEGORIES` and serves as the target for all categorization efforts. The specific categories are determined through an initial analysis of common application classifications across major platforms and refined for clarity and distinctiveness.

### 3.2 Data Acquisition and Preprocessing

Application data, including application names and associated tags or keywords, is acquired from the digital distribution platforms via dedicated modules in the `data_sources` directory. Each module (`apple-store.py`, `flathub.py`, `gog.py`, `itch_io.py`, `myabandonware.py`, `snap.py`) is responsible for fetching and initially parsing data specific to its respective platform.

Following data acquisition, a preprocessing step is applied. This involves:

*   **Normalization:** Ensuring consistency in category and tag naming conventions where possible, including handling variations in capitalization and punctuation. The `normalize_category` function in `utils/helpers.py` is utilized for this purpose.
*   **Tag Extraction:** Identifying relevant tags or keywords associated with each application. The method for extracting tags varies depending on the structure of the data provided by each source.

### 3.3 Multi-Stage Categorization Process

The core of the methodology is a multi-stage process implemented in `category_processing/processor.py`. This process sequentially applies different techniques to determine the most appropriate category.

#### 3.3.1 Keyword Mapping

The initial stage involves a direct keyword mapping. A predefined mapping of specific tags or keywords to static categories is maintained, likely within `config.py` or accessible via `utils/helpers.py`. If an application's tags or name contain a keyword that has a direct, unambiguous mapping to a static category, that category is assigned immediately. This provides a high-confidence initial categorization for applications with clear descriptive metadata.

#### 3.3.2 Source-Based Rules

Certain digital distribution platforms specialize in specific types of content. For instance, platforms like GOG, Itch.io, and MyAbandonware are primarily focused on games. To leverage this platform-specific context, a rule is applied to automatically categorize applications originating from these sources as "Game," assuming this is a static category. This rule is applied after the keyword mapping stage and provides a strong signal for categorization based on the source's inherent nature.

#### 3.3.3 Fuzzy Matching

For applications not categorized in the preceding stages, fuzzy matching is employed. This technique uses algorithms like those provided by the `rapidfuzz` library to compare the application's name and extracted tags against the names of the static categories. A similarity score is calculated, and if a match exceeds a predefined threshold, the corresponding static category is considered a potential candidate. This stage helps in categorizing applications where the naming or tagging might not be an exact match to a static category name but is sufficiently similar.

#### 3.3.4 Semantic Similarity Analysis

The final stage for applications that remain uncategorized involves a more sophisticated approach based on semantic similarity. A pre-trained Sentence Transformer model, specifically `all-MiniLM-L6-v2`, is utilized. This model embeds the application's name and its associated tags into a vector space. Similarly, the names of the static categories are also embedded. The cosine similarity between the application's embedding and each static category's embedding is calculated. The static category with the highest cosine similarity is identified as the most semantically related category. This method allows for categorization even when there is no direct keyword or close string match, by understanding the underlying meaning of the text.

### 3.4 Conflict Resolution and Default Assignment

In cases where multiple stages might suggest different categories (although the sequential nature of the process prioritizes certain methods), a conflict resolution strategy is implicitly followed by the order of execution: keyword mapping has the highest priority, followed by source-based rules, then fuzzy matching, and finally semantic similarity. The first stage that yields a confident match (based on predefined thresholds for fuzzy and semantic similarity) determines the category.

If, after exhausting all stages, an application cannot be confidently assigned to any of the static categories, it is assigned to a default "Others" category. This ensures that every application receives a categorization, even if it cannot be precisely mapped to a specific predefined class.

### 3.5 Evaluation

The effectiveness of this methodology can be evaluated through a combination of automated metrics (e.g., precision and recall against a manually labeled test set) and manual inspection of categorized results. Iterative refinement of the static categories, keyword mappings, fuzzy matching thresholds, and the selection of the semantic model can further improve the accuracy of the categorization process.

By combining deterministic keyword mapping, platform-specific heuristics, statistical fuzzy matching, and advanced semantic analysis, this methodology aims to provide a robust and accurate automated categorization system for applications from diverse digital distribution platforms.
