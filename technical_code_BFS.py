# class Movie:
#     def __init__(self, index, title, genre, release_year, avg_rating, num_reviews, review_highlights, life_insight, discovery_method, life_advice, suggested):
#         self.index = index
#         self.title = self._normalize_title(title)
#         self.genre = genre.strip().lower()
#         self.release_year = int(release_year) if release_year.isdigit() else 0
#         self.avg_rating = float(avg_rating) if self._is_number(avg_rating) else 0.0
#         self.num_reviews = int(num_reviews) if num_reviews.isdigit() else 0
#         self.review_highlights = review_highlights.lower()
#         self.life_insight = life_insight.lower()
#         self.discovery_method = discovery_method.lower()
#         self.life_advice = life_advice.lower()
#         self.suggested = suggested.strip().lower() == "y"

#     def _normalize_title(self, text):
#         return text.strip().lower().replace('“', '"').replace('”', '"').replace('’', "'")

#     def _is_number(self, s):
#         try:
#             float(s)
#             return True
#         except ValueError:
#             return False

# def parse_csv_line(line):
#     fields, field, in_quotes = [], '', False
#     for char in line:
#         if char == '"':
#             in_quotes = not in_quotes
#         elif char == ',' and not in_quotes:
#             fields.append(field.strip())
#             field = ''
#         else:
#             field += char
#     fields.append(field.strip())
#     return fields

# def load_dataset(filepath):
#     movies, seen_titles = [], set()
#     try:
#         with open(filepath, 'r', encoding='utf-8') as file:
#             next(file)  # Skip header
#             for index, line in enumerate(file):
#                 parts = parse_csv_line(line.strip())
#                 if len(parts) != 10:
#                     continue
#                 title, genre, release_year, avg_rating, num_reviews, review_highlights, life_insight, discovery_method, life_advice, suggested = parts
#                 normalized_title = title.strip().lower()
#                 if normalized_title in seen_titles:
#                     continue
#                 seen_titles.add(normalized_title)
#                 movies.append(Movie(index, title, genre, release_year, avg_rating, num_reviews, review_highlights, life_insight, discovery_method, life_advice, suggested))
#     except Exception as e:
#         print(f"Error loading dataset: {e}")
#     return movies

# def compute_similarity(m1, m2):
#     score = 0
#     advice1, advice2 = set(m1.life_advice.split()), set(m2.life_advice.split())
#     review1, review2 = set(m1.review_highlights.split()), set(m2.review_highlights.split())

#     if m1.genre == m2.genre:
#         score += 12
#     advice_overlap = len(advice1 & advice2)
#     score += advice_overlap * 5
#     if advice_overlap == 0:
#         score -= 8
#     if any(kw in m2.life_advice for kw in {"resilience", "character", "growth", "strength"}):
#         score += 4
#     score += len(review1 & review2) * 2
#     if m1.discovery_method == m2.discovery_method:
#         score += 6
#     score -= abs(m1.avg_rating - m2.avg_rating) / 2
#     if m2.suggested:
#         score += 2
#     return score

# def build_graph(movies, threshold):
#     graph = {i: [] for i in range(len(movies))}
#     for i in range(len(movies)):
#         for j in range(i + 1, len(movies)):
#             score = compute_similarity(movies[i], movies[j])
#             if score >= threshold:
#                 graph[i].append((j, score))
#                 graph[j].append((i, score))
#     return graph

# def normalize_title(text):
#     return text.strip().lower().replace('“', '"').replace('”', '"').replace('’', "'")

# def find_start_index(movies, title):
#     norm_title = normalize_title(title)
#     title_to_index = {movie.title: movie.index for movie in movies}
#     if norm_title in title_to_index:
#         return title_to_index[norm_title]
#     for movie in movies:
#         if norm_title in movie.title:
#             return movie.index
#     return -1

# def dfs_longest_path(graph, current, visited, depth, max_depth, path_cache):
#     if (current, depth) in path_cache:
#         return path_cache[(current, depth)]
#     if depth >= max_depth:
#         return [current]
#     max_path = [current]
#     for neighbor, _ in sorted(graph[current], key=lambda x: -x[1]):
#         if neighbor not in visited:
#             path = dfs_longest_path(graph, neighbor, visited | {neighbor}, depth + 1, max_depth, path_cache)
#             if len(path) + 1 > len(max_path):
#                 max_path = [current] + path
#     path_cache[(current, depth)] = max_path
#     return max_path

# def find_longest_chain(movies, graph, start_title, max_length=6):
#     start = find_start_index(movies, start_title)
#     if start == -1:
#         print("Start movie not found. Available titles:")
#         for m in movies:
#             print("-", m.title.title())
#         return []
#     path = dfs_longest_path(graph, start, {start}, 1, max_length, {})
#     return [movies[i].title.title() for i in path]

# def main():
#     filepath = "Netflix Life Impact Dataset (NLID).csv"
#     movies = load_dataset(filepath)
#     if not movies:
#         return
#     graph = build_graph(movies, threshold=8.0)
#     print(f"Loaded {len(movies)} movies. Graph built.")
#     start_title = input("Enter the starting movie: ")
#     path = find_longest_chain(movies, graph, start_title)
#     if path:
#         print("\n🎬 Recommended Movie Chain:")
#         for title in path:
#             print("->", title)

# if __name__ == "__main__":
#     main()


# def _safe_int(val):
#     try:
#         return int(val)
#     except:
#         return 0

# def _safe_float(val):
#     try:
#         return float(val)
#     except:
#         return 0.0

# def _normalize_title(title):
#     return title.strip().lower().replace('“', '"').replace('”', '"').replace('’', "'").replace("‘", "'")

# def _similar_genre(g1, g2):
#     return g1.lower() in g2.lower() or g2.lower() in g1.lower()

# def _keyword_overlap(a, b):
#     if not a or not b:
#         return 0
#     a_keywords = set(a.lower().split())
#     b_keywords = set(b.lower().split())
#     return len(a_keywords & b_keywords)

# def compute_similarity(movie1, movie2):
#     score = 0

#     genre1 = movie1.get('Genre', '').lower()
#     genre2 = movie2.get('Genre', '').lower()

#     if genre1 == genre2:
#         score += 10
#     elif _similar_genre(genre1, genre2):
#         score += 5

#     score += _safe_float(movie2.get('Rating', '0')) * 2
#     score += _keyword_overlap(movie1.get('Review Highlights', ''), movie2.get('Review Highlights', '')) * 2
#     score += _keyword_overlap(movie1.get('Advice Taken', ''), movie2.get('Advice Taken', '')) * 2

#     discover1 = movie1.get('How Discovered', '').strip().lower()
#     discover2 = movie2.get('How Discovered', '').strip().lower()
#     if discover1 == discover2:
#         score += 1

#     year1 = _safe_int(movie1.get('Release Year', '0'))
#     year2 = _safe_int(movie2.get('Release Year', '0'))
#     if abs(year1 - year2) <= 1:
#         score += 1

#     score += _safe_int(movie2.get('Review Count', '0')) * 0.01
#     score += _safe_int(movie2.get('Suggested To', '0')) * 0.5

#     return score

# def build_graph(movies):
#     graph = {}
#     edges = set()
#     for i in range(len(movies)):
#         graph[i] = []

#     for i in range(len(movies)):
#         for j in range(i + 1, len(movies)):
#             sim = compute_similarity(movies[i], movies[j])
#             if sim > 0:
#                 graph[i].append(j)
#                 edges.add((i, j))

#     return graph

# def find_longest_path_bfs(graph, start):
#     queue = [(start, [start])]
#     max_path = []

#     while queue:
#         current, path = queue.pop(0)
#         if len(path) > len(max_path):
#             max_path = path
#         for neighbor in graph.get(current, []):
#             if neighbor not in path:
#                 queue.append((neighbor, path + [neighbor]))

#     return max_path

# def find_start_index(start_title, movies):
#     normalized = _normalize_title(start_title)
#     title_map = {_normalize_title(m.get('Title', '')): i for i, m in enumerate(movies)}
#     return title_map.get(normalized, -1)

# def find_recommendation_chain_bfs(start_title, filename):
#     try:
#         with open(filename, encoding='utf-8') as f:
#             lines = f.readlines()
#     except Exception as e:
#         print(f"Error reading file: {e}")
#         return

#     header = [h.strip() for h in lines[0].split(',')]
#     movies = []
#     seen_titles = set()

#     for line in lines[1:]:
#         parts = line.strip().split(',')
#         if len(parts) != len(header):
#             continue
#         movie = dict(zip(header, parts))
#         norm_title = _normalize_title(movie.get("Title", ""))
#         if norm_title not in seen_titles:
#             seen_titles.add(norm_title)
#             movies.append(movie)

#     start_index = find_start_index(start_title, movies)
#     if start_index == -1:
#         print("Start movie not found.")
#         return

#     graph = build_graph(movies)
#     path = find_longest_path_bfs(graph, start_index)

#     print("\n🔗 BFS-Based Recommendation Chain:\n")
#     for i, idx in enumerate(path):
#         print(f"{i+1}. {movies[idx].get('Title', 'Unknown')} ({movies[idx].get('Genre', '').strip()}, Rating: {movies[idx].get('Rating', '')})")


# if __name__ == "__main__":
#     start_movie = "The Pursuit of Happyness"
#     dataset_path = "Netflix Life Impact Dataset (NLID).csv"
#     find_recommendation_chain_bfs(start_movie, dataset_path)
