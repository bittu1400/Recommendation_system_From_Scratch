class Movie:
    def __init__(self, index, title, genre, release_year, avg_rating, num_reviews, review_highlights, life_insight, discovery_method, life_advice, suggested):
        self.index = index
        self.title = self._normalize_title(title)
        self.genre = genre.strip().lower()
        self.release_year = int(release_year) if release_year.isdigit() else 0
        self.avg_rating = float(avg_rating) if self._is_number(avg_rating) else 0.0
        self.num_reviews = int(num_reviews) if num_reviews.isdigit() else 0
        self.review_highlights = review_highlights.lower()
        self.life_insight = life_insight.lower()
        self.discovery_method = discovery_method.lower()
        self.life_advice = life_advice.lower()
        self.suggested = suggested.strip().lower() == "y"

    def _normalize_title(self, text):
        return text.strip().lower().replace('“', '"').replace('”', '"').replace('’', "'")

    def _is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

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
    movies, seen_titles = [], set()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            next(file)  # Skip header
            for index, line in enumerate(file):
                parts = parse_csv_line(line.strip())
                if len(parts) != 10:
                    continue
                title, genre, release_year, avg_rating, num_reviews, review_highlights, life_insight, discovery_method, life_advice, suggested = parts
                normalized_title = title.strip().lower()
                if normalized_title in seen_titles:
                    continue
                seen_titles.add(normalized_title)
                movies.append(Movie(index, title, genre, release_year, avg_rating, num_reviews, review_highlights, life_insight, discovery_method, life_advice, suggested))
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
    graph = {i: [] for i in range(len(movies))}
    for i in range(len(movies)):
        for j in range(i + 1, len(movies)):
            score = compute_similarity(movies[i], movies[j])
            if score >= threshold:
                graph[i].append((j, score))
                graph[j].append((i, score))
    return graph

def normalize_title(text):
    return text.strip().lower().replace('“', '"').replace('”', '"').replace('’', "'")

def find_start_index(movies, title):
    norm_title = normalize_title(title)
    title_to_index = {movie.title: movie.index for movie in movies}
    if norm_title in title_to_index:
        return title_to_index[norm_title]
    for movie in movies:
        if norm_title in movie.title:
            return movie.index
    return -1

def dfs_longest_path(graph, current, visited, depth, max_depth, path_cache):
    if (current, depth) in path_cache:
        return path_cache[(current, depth)]
    if depth >= max_depth:
        return [current]
    max_path = [current]
    for neighbor, _ in sorted(graph[current], key=lambda x: -x[1]):
        if neighbor not in visited:
            path = dfs_longest_path(graph, neighbor, visited | {neighbor}, depth + 1, max_depth, path_cache)
            if len(path) + 1 > len(max_path):
                max_path = [current] + path
    path_cache[(current, depth)] = max_path
    return max_path

def find_longest_chain(movies, graph, start_title, max_length=6):
    start = find_start_index(movies, start_title)
    if start == -1:
        print("Start movie not found. Available titles:")
        for m in movies:
            print("-", m.title.title())
        return []
    path = dfs_longest_path(graph, start, {start}, 1, max_length, {})
    return [movies[i].title.title() for i in path]

def main():
    filepath = "Netflix Life Impact Dataset (NLID).csv"
    movies = load_dataset(filepath)
    if not movies:
        return
    graph = build_graph(movies, threshold=8.0)
    print(f"Loaded {len(movies)} movies. Graph built.")
    start_title = input("Enter the starting movie: ")
    path = find_longest_chain(movies, graph, start_title)
    if path:
        print("\n🎬 Recommended Movie Chain:")
        for title in path:
            print("->", title)

if __name__ == "__main__":
    main()
