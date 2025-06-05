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
            return int(value)
        except (ValueError, TypeError):
            print(f"Warning: {warning}")
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
        raise ValueError("Invalid filepath provided")

    movies, seen_titles = [], set()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            next(file)  # Skip header
            for index, line in enumerate(file, start=0):
                parts = parse_csv_line(line.strip())
                if len(parts) != 10:
                    print(f"Skipping row at line {index + 2} due to incorrect field count: {len(parts)} fields, expected 10")
                    continue
                title = parts[0]
                normalized_title = Movie(0, title, "", "", 0, 0, "", "", "", "", "")._normalize_title(title)
                if normalized_title in seen_titles:
                    print(f"Skipping duplicate movie at line {index + 2}: {title}")
                    continue
                seen_titles.add(normalized_title)
                try:
                    movie = Movie(index, *parts)
                    movies.append(movie)
                except Exception as e:
                    print(f"Skipping row at line {index + 2} due to invalid data: {parts}, Error: {e}")
    except FileNotFoundError:
        print(f"Dataset file not found: {filepath}")
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
    return text.strip().lower().replace('“', '"').replace('”', '"').replace('’', "'")

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
    start = find_start_index(movies, start_title)
    if start == -1:
        print("❌ Start movie not found.")
        return []

    path, visited, current, step = [start], {start}, start, 0
    while len(path) < max_length:
        neighbors = [(n, s) for n, s in graph.get(current, []) if n not in visited]
        if not neighbors:
            break
        if step < 3:
            next_node, _ = max(neighbors, key=lambda x: x[1])
        else:
            next_node, _ = max(
                [(n, s - 6 if movies[current].discovery_method == movies[n].discovery_method else s) for n, s in neighbors],
                key=lambda x: x[1]
            )
        path.append(next_node)
        visited.add(next_node)
        current = next_node
        step += 1

    return [movies[i].title.title() for i in path]

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
        print(f"Movie {movies[node].title.title()}: {len(edges)} edges")

    title_to_index = {movie.title: movie.index for movie in movies}
    start_title = input('\nEnter the starting movie: ').strip().lower()
    if start_title not in title_to_index:
        print("Start movie not found in dataset.")
        return
    start_index = title_to_index[start_title]

    mode = input("\nChoose mode: (1) Greedy DFS-like  (2) BFS \nEnter 1 or 2: ").strip()

    if mode == '2':
        path = find_longest_path_bfs(graph, movies, start_index)
        label = "🔗 BFS-Based Recommendation Chain"
    else:
        path = find_longest_path(movies, graph, start_index)
        label = "🎬 Greedy Longest Recommendation Chain"

    if path:
        print(f"\n{label}:")
        for idx in path:
            print("->", movies[idx].title.title())
    else:
        print("No recommendation chain found.")

if __name__ == "__main__":
    main()
