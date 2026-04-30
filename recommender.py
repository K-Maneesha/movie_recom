import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import load_data, filter_data, smart_mood

# Load data once
df = load_data()

# Build TF-IDF matrix on descriptions
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['description'].fillna(''))

# Cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


# ─────────────────────────────────────────
# 1. MOOD BASED RECOMMENDATION
# ─────────────────────────────────────────
def recommend_by_mood(mood, language=None, year_range=None, min_rating=0, top_n=10):
    adjusted_mood = smart_mood(mood)
    filtered = filter_data(df.copy(), language, year_range, min_rating)
    result = filtered[filtered['mood'] == adjusted_mood]
    result = result.sort_values('rating', ascending=False)
    return result[['title', 'genre', 'language', 'year', 'rating', 'description']].head(top_n)


# ─────────────────────────────────────────
# 2. SIMILAR MOVIES (for chatbot)
# ─────────────────────────────────────────
def recommend_similar(movie_title, top_n=10):
    # Find movie index
    indices = pd.Series(df.index, index=df['title'].str.lower())

    movie_title = movie_title.lower()

    # Check if movie exists
    if movie_title not in indices:
        # Try partial match
        match = df[df['title'].str.lower().str.contains(movie_title)]
        if match.empty:
            return None
        idx = match.index[0]
    else:
        idx = indices[movie_title]

    # Get similarity scores
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    movie_indices = [i[0] for i in sim_scores]
    result = df.iloc[movie_indices]
    return result[['title', 'genre', 'language', 'year', 'rating', 'description']]


# ─────────────────────────────────────────
# 3. GROUP RECOMMENDATION
# ─────────────────────────────────────────
def recommend_for_group(mood_list, top_n=10):
    all_results = pd.DataFrame()

    for mood in mood_list:
        result = recommend_by_mood(mood, top_n=top_n)
        all_results = pd.concat([all_results, result])

    # Remove duplicates, sort by rating
    all_results = all_results.drop_duplicates(subset='title')
    all_results = all_results.sort_values('rating', ascending=False)

    return all_results.head(top_n)


# ─────────────────────────────────────────
# 4. GENRE BASED RECOMMENDATION
# ─────────────────────────────────────────
def recommend_by_genre(genre, language=None, year_range=None, min_rating=0, top_n=10):
    filtered = filter_data(df.copy(), language, year_range, min_rating)
    result = filtered[filtered['genre'].str.contains(genre, case=False, na=False)]
    result = result.sort_values('rating', ascending=False)
    return result[['title', 'genre', 'language', 'year', 'rating', 'description']].head(top_n)