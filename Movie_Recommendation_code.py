
class Movie:
    def __init__(self, index, title, genre, release_year, avg_rating, num_reviews, review_highlights, life_insight, discovery_method, life_advice, suggested):
        self.index = index
        self.title = self._normalize_title(title)
        self.genre = genre.strip().lower()
        self.release_year = self._safe_int(release_year, f"Invalid release_year for {title}, defaulting to 0")
        self.avg_rating = self._safe_float(avg_rating, f"Invalid avg_rating for {title}, defaulting to 0.0")
        self.num_reviews = self._safe_int(num_reviews, f"Invalid num_reviews for {title}, defaulting to 0")
        self.review_highlights = review_highlights.lower()
        self.life_insight = life_insight.lower()
        self.discovery_method = discovery_method.lower()
        self.life_advice = life_advice.lower()
        self.suggested = suggested.strip().lower() == "y"

    def _normalize_title(self, text):
        return text.strip().lower().replace('“', '"').replace('”', '"').replace('’', "'")

    def _safe_int(self, value, warning):
        try:
            if value is None or str(value).strip().lower() in ["", "nan"]:
                raise ValueError
            return int(float(value))
        except (ValueError, TypeError):
            print(f"{value} Warning: {warning}")
            return 0

    def _safe_float(self, value, warning):
        try:
            return float(value)
        except (ValueError, TypeError):
            print(f"Warning: {warning}")
            return 0.0

def parse_csv_line(line):
    fields, field, in_quotes = [], '', False
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            fields.append(field.strip())
            field = ''
        else:
            field += char
    fields.append(field.strip())
    return fields

def load_dataset(filepath):
    if not filepath or not isinstance(filepath, str):
        print("Error: Invalid filepath provided")
        return []

    movies, seen_titles = [], set()
    try:
        with open(filepath, 'r') as file:
            next(file)  # Skip header
            for line_num, line in enumerate(file, start=2):
                parts = parse_csv_line(line.strip())
                if len(parts) != 10:
                    print(f"Skipping row at line {line_num}: incorrect field count ({len(parts)})")
                    continue
                title = parts[0]
                normalized_title = Movie(0, *parts)._normalize_title(title)
                if normalized_title in seen_titles:
                    print(f"Skipping duplicate movie at line {line_num}: {title}")
                    continue
                seen_titles.add(normalized_title)
                try:
                    # Use list index as movie.index
                    movie = Movie(len(movies), *parts)
                    movies.append(movie)
                except Exception as e:
                    print(f"Skipping row at line {line_num}: invalid data: {parts}, Error: {e}")
    except FileNotFoundError:
        print(f"Error: Dataset file not found: {filepath}")
    except Exception as e:
        print(f"Error loading dataset: {e}")
    return movies
def compute_similarity(m1, m2):
    score = 0
    advice1, advice2 = set(m1.life_advice.split()), set(m2.life_advice.split())
    review1, review2 = set(m1.review_highlights.split()), set(m2.review_highlights.split())

    if m1.genre == m2.genre:
        score += 12
    advice_overlap = len(advice1 & advice2)
    score += advice_overlap * 5
    if advice_overlap == 0:
        score -= 8

    if any(kw in m2.life_advice for kw in {"resilience", "character", "growth", "strength"}):
        score += 4

    score += len(review1 & review2) * 2

    if m1.discovery_method == m2.discovery_method:
        score += 6

    score -= abs(m1.avg_rating - m2.avg_rating) / 2

    if m2.suggested:
        score += 2

    return score

def build_graph(movies, threshold):
    graph, edges = {i: [] for i in range(len(movies))}, set()
    for i in range(len(movies)):
        for j in range(i + 1, len(movies)):
            score = compute_similarity(movies[i], movies[j])
            if score >= threshold:
                edge = tuple(sorted((i, j)))
                if edge not in edges:
                    graph[i].append((j, score))
                    graph[j].append((i, score))
                    edges.add(edge)
    return graph

def normalize_title(text):
    return str(text).strip().lower().replace('“', '"').replace('”', '"').replace('’', "'")

def find_start_index(movies, input_title):
    input_title_clean = normalize_title(input_title)
    for movie in movies:
        if input_title_clean == movie.title:
            return movie.index
    for movie in movies:
        if input_title_clean in movie.title:
            return movie.index
    return -1

def find_longest_path(movies, graph, start_title, max_length=6):
    if not movies:
        print("Error: Empty movie list")
        return []

    start = find_start_index(movies, start_title)
    if start == -1 or start >= len(movies):
        print(f"Error: Invalid start index for {start_title}")
        return []

    path, visited, current = [start], {start}, start
    while len(path) < max_length:
        neighbors = [(n, s) for n, s in graph.get(current, []) if n not in visited]
        if not neighbors:
            break
        next_node, score = max(neighbors, key=lambda x: x[1])
        if next_node < 0 or next_node >= len(movies):
            print(f"Error: Invalid neighbor index {next_node} for movie {movies[current].title.title()}")
            break
        path.append(next_node)
        visited.add(next_node)
        current = next_node

    return path
def find_longest_path_bfs(graph, movies, start, max_len=6):
    queue = [(start, [start], 0)]  # (current_node, path_so_far, total_score)
    best_path = []

    while queue:
        current, path, score = queue.pop(0)

        if len(path) > len(best_path):
            best_path = path

        if len(path) >= max_len:
            continue

        neighbors = graph.get(current, [])
        neighbors_sorted = sorted(neighbors, key=lambda x: x[1], reverse=True)

        for neighbor, edge_score in neighbors_sorted:
            if neighbor not in path:
                queue.append((neighbor, path + [neighbor], score + edge_score))

    return best_path

def main():
    filepath = "Netflix Life Impact Dataset (NLID).csv"
    movies = load_dataset(filepath)
    if not movies:
        print("No movies loaded.")
        return
    print(f"Loaded {len(movies)} movies.")

    threshold = 6.0
    graph = build_graph(movies, threshold)
    print("Graph constructed. Edges per node:")
    for node, edges in graph.items():
        if node < 0 or node >= len(movies):
            print(f"Error: Invalid graph node index {node}")
            continue
        print(f"Movie {movies[node].title.title()}: {len(edges)} edges")

    title_to_index = {movie.title: movie.index for movie in movies}
    start_title = input('\nEnter the starting movie: ').strip().lower()
    if start_title not in title_to_index:
        suggestions = [movie.title.title() for movie in movies if start_title in movie.title]
        if suggestions:
            print(f"Movie not found. Did you mean one of these? {', '.join(suggestions[:3])}")
        else:
            print("Start movie not found in dataset.")
        return
    start_index = title_to_index[start_title]

    while True:
        mode = input("\nChoose mode: (1) Greedy DFS  (2) BFS \nEnter 1 or 2: ").strip()
        if mode in ['1', '2']:
            break
        print("Invalid mode. Please enter 1 or 2.")

    if mode == '2':
        path = find_longest_path_bfs(graph, movies, start_index)
        label = "🔗 BFS-Based Recommendation Chain"
    else:
        path = find_longest_path(movies, graph, start_title)
        label = "🎬 Greedy DFS-Based Recommendation Chain"

    if not path:
        print("No recommendation chain found.")
        return

    print(f"\n{label}:")
    for idx in path:
        if idx < 0 or idx >= len(movies):
            print(f"Error: Invalid path index {idx}")
            continue
        print("->", movies[idx].title.title())
if __name__ == "__main__":
    main()
