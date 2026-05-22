import pandas as pd
import json

def load_data():
    df = pd.read_csv("tmdb_5000_movies.csv")

    # Keep only useful columns
    df = df[['title', 'genres', 'original_language', 'release_date', 'vote_average', 'overview', 'popularity']]

    # Rename columns
    df.rename(columns={
        'original_language': 'language',
        'vote_average': 'rating',
        'release_date': 'year',
        'overview': 'description'
    }, inplace=True)

    # Extract year from date
    df['year'] = pd.to_datetime(df['year'], errors='coerce').dt.year

    # Parse genres from JSON string → comma separated
    def parse_genres(genre_str):
        try:
            genres = json.loads(genre_str)
            return ', '.join([g['name'] for g in genres])
        except:
            return ''

    df['genre'] = df['genres'].apply(parse_genres)
    df.drop(columns=['genres'], inplace=True)

    # Map mood based on genre
    def assign_mood(genre):
        genre = genre.lower()
        if any(g in genre for g in ['comedy', 'family', 'animation']):
            return 'Happy'
        elif any(g in genre for g in ['drama', 'romance']):
            return 'Sad'
        elif any(g in genre for g in ['action', 'thriller', 'science fiction', 'adventure']):
            return 'Action'
        else:
            return 'Happy'

    df['mood'] = df['genre'].apply(assign_mood)

    # Clean up
    df.dropna(subset=['title', 'description'], inplace=True)
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0)
    df['year'] = df['year'].fillna(0).astype(int)
    df['language'] = df['language'].fillna('en')

    # Map language codes to full names
    language_map = {
        'en': 'English',
        'hi': 'Hindi',
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ar': 'Arabic',
        'ta': 'Tamil',
        'te': 'Telugu',
        'ml': 'Malayalam',
        'bn': 'Bengali',
        'tr': 'Turkish',
        'nl': 'Dutch',
        'sv': 'Swedish',
        'pl': 'Polish',
        'da': 'Danish',
        'fi': 'Finnish',
        'no': 'Norwegian',
        'th': 'Thai',
        'id': 'Indonesian',
        'ro': 'Romanian',
        'hu': 'Hungarian',
        'cs': 'Czech',
        'uk': 'Ukrainian',
        'he': 'Hebrew',
        'fa': 'Persian',
    }
    df['language'] = df['language'].map(language_map).fillna('Other')

    return df


def filter_data(df, language=None, year_range=None, min_rating=0):
    if language and language != 'All':
        df = df[df['language'] == language]
    if year_range:
        df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
    df = df[df['rating'] >= min_rating]
    return df


def get_weekend_or_weekday():
    from datetime import datetime
    day = datetime.today().weekday()
    # 0=Monday ... 4=Friday, 5=Saturday, 6=Sunday
    if day >= 5:
        return 'weekend'
    return 'weekday'


def smart_mood(mood):
    time = get_weekend_or_weekday()
    if time == 'weekend':
        # Push towards fun on weekends
        if mood == 'Sad':
            return 'Happy'
    else:
        # Weekday → lighter content
        if mood == 'Action':
            return 'Happy'
    return mood