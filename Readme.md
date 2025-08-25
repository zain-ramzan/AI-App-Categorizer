## 3. Categorization Methodology

This section delineates the comprehensive methodology developed for the automated assignment of digital applications to predefined categories. Recognizing the heterogeneity of metadata across various application distribution platforms, our approach integrates a sequence of analytical techniques designed to leverage diverse sources of information and achieve high-confidence categorization. The entire process is orchestrated within the `categorization_processing/processor.py` module, utilizing configuration parameters specified in `config.py` and utility functions housed in `utils/helpers.py`.

### 3.1 Definition of the Static Category Set

The foundation of our categorization system is a meticulously curated set of static categories. This set, enumerated within the `STATIC_CATEGORIES` list in `config.py`, represents a controlled vocabulary of broad application domains. The selection of these categories was informed by an extensive analysis of existing classification schemes employed by major application stores and digital distribution platforms, aiming for a balance between specificity and generality to ensure applicability across diverse sources. These static categories serve as the exclusive target classes for the categorization process.

### 3.2 Data Acquisition and Preprocessing

Raw application metadata, comprising application names and associated descriptive tags or keywords, is programmatically acquired from various digital distribution platforms. This acquisition is facilitated by dedicated data source modules (e.g., `data_sources/apple-store.py`, `data_sources/gog.py`), each tailored to the specific API or scraping requirements of its respective platform.

Subsequent to data acquisition, a critical preprocessing phase is undertaken to standardize the input data and prepare it for the categorization pipeline:

*   **Text Normalization:** All textual data, including application names and tags, undergoes normalization. This involves converting text to lowercase, removing leading/trailing whitespace, and potentially handling variations in punctuation or special characters. The `normalize_category` function within `utils/helpers.py` is a key component of this step, ensuring uniformity in textual representations.
*   **Tag Aggregation:** Tags and keywords provided by the source platform are collected and aggregated into a unified list for each application. This aggregated list serves as a rich source of descriptive terms for subsequent analysis.

### 3.3 Hierarchical Categorization Pipeline

Our methodology employs a hierarchical pipeline structure, where different categorization techniques are applied sequentially. This allows for leveraging high-precision methods first, falling back to more generalized approaches only when a definitive category cannot be assigned at an earlier stage.

#### 3.3.1 Direct Keyword Mapping

The initial stage of the pipeline involves a direct mapping of specific, high-signal keywords or tags to static categories. A predefined dictionary or mapping structure, potentially managed within `config.py` or accessible via `utils/helpers.py` (e.g., through a `keyword_mapping` function), associates certain terms with specific static categories. If an application's name or its aggregated tags contain a term present in this mapping, the corresponding static category is assigned. This step is designed for high recall and precision for applications with clear, descriptive metadata that directly aligns with known category indicators.

#### 3.3.2 Source-Specific Heuristics

Leveraging the domain expertise associated with certain platforms, a set of source-specific heuristics is applied. For platforms primarily dedicated to a particular type of content, a direct categorization rule can be implemented. For instance, as observed in the analysis, applications originating from platforms like GOG, Itch.io, and MyAbandonware are frequently games. Consequently, if an application is sourced from one of these platforms, it is automatically assigned to the "Game" category. This heuristic exploits the inherent nature of the data source to provide a confident categorization where applicable.

#### 3.3.3 Fuzzy String Matching

For applications that remain uncategorized after the initial mapping and source-specific rules, fuzzy string matching is employed. This technique assesses the similarity between the application's name and its aggregated tags against the names of the static categories using algorithms that tolerate minor variations (e.g., typographical errors, slight phrasing differences). Libraries like `rapidfuzz` are utilized to calculate similarity scores. If the similarity score between the application's descriptive text and a static category name exceeds a predefined threshold (a tunable parameter, likely in `config.py`), that category is considered a potential match. The category with the highest similarity score above the threshold is selected. This stage addresses variations in how categories or content are described across different platforms.

#### 3.3.4 Semantic Similarity Analysis

The final stage of the pipeline utilizes a sophisticated semantic similarity analysis for applications still lacking a category assignment. This step moves beyond lexical matching to understand the conceptual relationship between the application's description and the static categories.

1.  **Text Embedding:** The application's name and aggregated tags are combined into a single descriptive text string. This string is then transformed into a high-dimensional vector representation (embedding) using a pre-trained sentence transformer model, specifically the `all-MiniLM-L6-v2` model. This model is chosen for its balance of performance and computational efficiency.
2.  **Category Embedding:** The names of all static categories are similarly embedded into the same vector space using the same model.
3.  **Similarity Calculation:** The cosine similarity is calculated between the application's embedding and the embedding of each static category. Cosine similarity measures the angle between two vectors, providing a metric of their semantic relatedness.
4.  **Category Selection:** The static category whose embedding has the highest cosine similarity with the application's embedding is selected as the most semantically relevant category. A minimum similarity threshold may be applied here as well, ensuring that only sufficiently strong semantic relationships result in a categorization. This stage is crucial for categorizing applications whose descriptions may use synonyms, related terms, or broader concepts that do not directly match static category names through simple string matching.

### 3.4 Default Assignment

Should an application fail to be assigned a category through any of the preceding stages (due to lack of matching keywords, inapplicability of source-specific rules, or failing to meet the similarity thresholds in fuzzy or semantic matching), it is assigned to a default category, typically labeled "Others." This ensures that all applications are processed and assigned a category, providing a complete output dataset, albeit with an "Others" category for those that do not fit neatly into the defined static categories.

### 3.5 Refinement and Evaluation

The efficacy of this multi-stage methodology is subject to continuous evaluation and refinement. This involves:

*   **Manual Inspection:** Random sampling of categorized applications to identify instances of misclassification and understand the reasons behind them.
*   **Threshold Tuning:** Adjusting the similarity thresholds used in the fuzzy matching and semantic similarity stages to optimize the trade-off between precision and recall.
*   **Static Category Review:** Periodically reviewing and potentially revising the set of static categories based on analysis of the "Others" category and evolving application landscapes.
*   **Keyword Mapping Expansion:** Continuously updating and expanding the direct keyword mapping based on new data and observed patterns.

By employing this layered approach, the categorization methodology leverages the strengths of different techniques to provide a robust and adaptable solution for categorizing applications from a variety of digital distribution sources.
