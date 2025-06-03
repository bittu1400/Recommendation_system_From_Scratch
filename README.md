Movie Recommendation Chain System
Overview
The Movie Recommendation Chain System is a Python-based application that curates personalized, impactful movie recommendation chains using the Netflix Life Impact Dataset (NLID). By modeling movies as nodes in a Directed Acyclic Graph (DAG) and connecting them based on a multifaceted similarity metric, the system generates sequences of up to six movies that resonate emotionally and thematically with a user’s initial choice. Unlike traditional recommendation systems focused on ratings or popularity, this project prioritizes transformative viewing experiences, leveraging qualitative attributes like life advice and viewer sentiments.
The system employs robust data handling, object-oriented programming, and an optimized Depth-First Search (DFS) algorithm with memoization to ensure efficiency and scalability. It draws inspiration from analyses of exercise efficiency and world happiness reports, emphasizing intuitive design and emotional coherence.
Features

Graph-Based Recommendations: Models movies as a DAG, with edges weighted by similarity scores based on genre, life advice, review highlights, discovery method, and viewer recommendations.
Robust Data Processing: Parses the NLID CSV file, handling malformed rows, duplicates, and invalid data with comprehensive error logging.
Multifaceted Similarity Scoring:
Genre match: +12 points
Life advice keyword overlap: +5 per word
Review highlight overlap: +2 per word
Discovery method match: +6 points
Viewer suggestion: +2 points
Rating difference penalty: Subtracts half the absolute difference
No advice overlap penalty: -8 points
Bonus for keywords (e.g., resilience, growth): +4 points


Optimized Path Finding: Uses DFS with memoization to efficiently find the longest recommendation chain, limited to a configurable length (default: 6 movies).
User-Friendly Interface: Accepts a starting movie title and outputs a formatted recommendation chain, with error handling for invalid inputs.

Dataset
The system uses the Netflix Life Impact Dataset (NLID), a collection of 83 movie records with 10 attributes:

Title: Movie name
Genre: Primary genre (e.g., documentary, thriller)
Release Year: Year of release
Average Rating: Viewer-assigned rating
Number of Reviews: Total reviews
Review Highlights: Key phrases from reviews
Life Insight: Viewer-reported insights
Discovery Method: How viewers found the movie (e.g., word-of-mouth)
Life Advice: Practical advice inspired by the movie
Suggested: Whether viewers recommended the movie (Y/N)

The dataset is not included in this repository due to potential licensing restrictions. Users must obtain the NLID CSV file and place it in the project directory as Netflix Life Impact Dataset (NLID).csv.
Installation

Clone the Repository:git clone https://github.com/your-username/movie-recommendation-chain.git
cd movie-recommendation-chain


Set Up a Virtual Environment (optional but recommended):python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:No external libraries are required, as the system uses Python’s standard library (csv, collections).
Add the Dataset:Place the Netflix Life Impact Dataset (NLID).csv file in the project root directory.

Usage

Run the Application:python main.py


Enter a Starting Movie:When prompted, input a movie title (exact or partial match). The system will:
Load and validate the NLID dataset.
Construct a DAG based on similarity scores (threshold: 8.0).
Output a recommendation chain of up to six movies.


Example Output:Loaded 83 movies.
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


Error Handling:If the input movie is not found, the system lists available titles:Start movie not found. Available titles:
-> The Pursuit Of Happyness
-> The Shawshank Redemption
...



Project Structure
movie-recommendation-chain/
├── main.py                    # Main application script
├── Netflix Life Impact Dataset (NLID).csv  # Dataset file (user-provided)
├── README.md                  # Project documentation

Performance

Time Complexity:
Data Loading: $O(n)$, where $n$ is the number of movies (83).
Graph Construction: $O(n^2)$ for pairwise similarity comparisons.
Longest Path Search: $O(n + e)$, where $e$ is the number of edges, optimized by memoization.
Total: $O(n^2)$, suitable for the NLID’s size.


Space Complexity:
Graph Storage: $O(n + e)$, sparse due to threshold.
Memoization Cache: $O(n \times \text{max_depth})$, where max depth is 6.
Total: $O(n^2)$ worst-case, but typically lower.


Scalability: Efficient for small to medium datasets; future optimizations are planned for larger datasets.

Future Enhancements

Real-Time Updates: Integrate streaming data for dynamic graph updates.
Machine Learning: Use NLP models (e.g., BERT) for advanced similarity scoring.
Personalization: Incorporate user watch history for tailored chains.
Visualization: Develop an interactive graph interface to explore recommendation networks.
Scalability: Optimize graph construction with parallel processing for larger datasets.

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

Please ensure code follows PEP 8 style guidelines and includes relevant tests.
License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Netflix Life Impact Dataset (NLID): For providing a unique dataset to explore transformative cinematic experiences.
Inspiration: Exercise efficiency and world happiness report analyses for guiding robust data handling and analytical rigor.
Community: Thanks to the open-source community for tools and resources that made this project possible.

Contact
For questions or feedback, please open an issue on GitHub or contact [surajsah1400@gmail.com].
