# Movie Recommendation Chain System

## Overview

The **Movie Recommendation Chain System** is a Python-based application that curates personalized, impactful movie recommendation chains using the **Netflix Life Impact Dataset (NLID)**. By modeling movies as nodes in a **Directed Acyclic Graph (DAG)** and connecting them based on a multifaceted similarity metric, the system generates sequences of up to six movies that resonate emotionally and thematically with a user’s initial choice.

Unlike traditional recommendation systems focused on ratings or popularity, this project prioritizes **transformative viewing experiences**, leveraging qualitative attributes like life advice and viewer sentiments.

The system uses object-oriented programming, robust data handling, and an optimized **Depth-First Search (DFS)** algorithm with memoization to ensure both efficiency and scalability. It draws inspiration from analyses of exercise efficiency and world happiness reports, emphasizing intuitive design and emotional coherence.

---

## Features

* **Graph-Based Recommendations**

  * Models movies as a DAG, with edges weighted by similarity scores based on:

    * Genre
    * Life advice
    * Review highlights
    * Discovery method
    * Viewer recommendations

* **Robust Data Processing**

  * Parses the NLID CSV file
  * Handles malformed rows, duplicates, and invalid data
  * Provides comprehensive error logging

* **Multifaceted Similarity Scoring**

  * Genre match: `+12 points`
  * Life advice keyword overlap: `+5 per word`
  * Review highlight overlap: `+2 per word`
  * Discovery method match: `+6 points`
  * Viewer suggestion: `+2 points`
  * Rating difference penalty: `-0.5 * abs(difference)`
  * No advice overlap penalty: `-8 points`
  * Bonus for keywords (e.g., resilience, growth): `+4 points`

* **Optimized Path Finding**

  * Uses DFS with memoization
  * Finds the longest recommendation chain (default limit: 6 movies)

* **User-Friendly Interface**

  * Accepts a starting movie title
  * Outputs a formatted recommendation chain
  * Handles invalid input gracefully

---

## Dataset

The system uses the **Netflix Life Impact Dataset (NLID)**, containing 83 movie records with the following attributes:

* `Title`: Movie name
* `Genre`: Primary genre (e.g., documentary, thriller)
* `Release Year`: Year of release
* `Average Rating`: Viewer-assigned rating
* `Number of Reviews`: Total reviews
* `Review Highlights`: Key phrases from reviews
* `Life Insight`: Viewer-reported insights
* `Discovery Method`: How viewers found the movie (e.g., word-of-mouth)
* `Life Advice`: Practical advice inspired by the movie
* `Suggested`: Whether viewers recommended the movie (Y/N)

**Note:** The dataset is **not included** in this repository due to potential licensing restrictions. You must obtain the CSV file and place it in the project directory as:

```
Netflix Life Impact Dataset (NLID).csv
```

---

## Installation

```bash
# Clone the Repository
git clone https://github.com/your-username/movie-recommendation-chain.git
cd movie-recommendation-chain

# Set Up a Virtual Environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Dependencies
# No external libraries required; uses standard Python libraries

# Add the Dataset
# Place the CSV file in the root directory as mentioned
```

---

## Usage

```bash
python main.py
```

* **Enter a Starting Movie** when prompted (exact or partial match).
* The system will:

  1. Load and validate the dataset
  2. Construct the DAG (threshold similarity: 8.0)
  3. Output a recommendation chain (max 6 movies)

#### Example Output

```
Loaded 83 movies.
Graph constructed. Edges per node:
Movie The Pursuit Of Happyness: 12 edges
...
Enter the starting movie: The Pursuit of Happyness

🎬 Recommended Movie Chain:
-> The Pursuit Of Happyness
-> The Shawshank Redemption
-> Forrest Gump
-> Life Is Beautiful
-> Dead Poets Society
-> Good Will Hunting
```

#### Error Handling

If movie is not found:

```
Start movie not found. Available titles:
-> The Pursuit Of Happyness
-> The Shawshank Redemption
...
```

---

## Project Structure

```
movie-recommendation-chain/
├── main.py                               # Main application script
├── Netflix Life Impact Dataset (NLID).csv  # Dataset file (user-provided)
├── README.md                             # Project documentation
```

---

## Performance

### Time Complexity

* **Data Loading**: \$O(n)\$
* **Graph Construction**: \$O(n^2)\$ for pairwise comparisons
* **Longest Path Search**: \$O(n + e)\$, optimized with memoization
* **Total**: \$O(n^2)\$ — efficient for NLID size (n = 83)

### Space Complexity

* **Graph Storage**: \$O(n + e)\$ (sparse graph)
* **Memoization Cache**: \$O(n \times \text{max\_depth})\$ (default depth = 6)
* **Total**: \$O(n^2)\$ in the worst case, typically much lower

---

## Future Enhancements

* **Real-Time Updates**: Support streaming data for dynamic graphs
* **Machine Learning**: Use NLP models (e.g., BERT) for smarter similarity
* **Personalization**: Tailor chains based on user history
* **Visualization**: Add interactive graph interface
* **Scalability**: Use parallelism for faster graph generation

---

## Contributing

Contributions are welcome! To contribute:

```bash
# Fork and Clone
# Create a feature branch
$ git checkout -b feature/your-feature

# Make Changes and Commit
$ git commit -m "Add your feature"

# Push and Open PR
$ git push origin feature/your-feature
```

Please follow **PEP 8** style guidelines and include tests where applicable.

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## Acknowledgments

* **Netflix Life Impact Dataset (NLID)** for the unique data
* **Inspiration** from exercise efficiency and world happiness reports
* **Community** for tools, insights, and open-source contributions

---

## Contact

Have a question or suggestion? Open an issue or contact:
📧 **[surajsah1400@gmail.com](mailto:surajsah1400@gmail.com)**
