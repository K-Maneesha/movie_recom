import re
from recommender import recommend_similar, recommend_by_mood, recommend_by_genre

# ─────────────────────────────────────────
# KEYWORD MAPS
# ─────────────────────────────────────────

MOOD_KEYWORDS = {
    'Happy': ['happy', 'fun', 'funny', 'comedy', 'laugh', 'cheerful', 'light', 'feel good'],
    'Sad': ['sad', 'cry', 'emotional', 'drama', 'romance', 'love', 'heartbreak', 'touching'],
    'Action': ['action', 'thriller', 'fight', 'adventure', 'exciting', 'intense', 'sci-fi', 'scifi']
}

GENRE_KEYWORDS = [
    'comedy', 'drama', 'action', 'romance', 'thriller',
    'horror', 'animation', 'family', 'science fiction',
    'fantasy', 'mystery', 'documentary'
]

SIMILAR_PATTERNS = [
    r'movies? like (.+)',
    r'similar to (.+)',
    r'films? like (.+)',
    r'recommend.*like (.+)',
    r'suggest.*like (.+)',
    r'anything like (.+)',
]


# ─────────────────────────────────────────
# DETECT INTENT
# ─────────────────────────────────────────

def detect_intent(user_input):
    text = user_input.lower().strip()

    # Check for "movies like X" pattern
    for pattern in SIMILAR_PATTERNS:
        match = re.search(pattern, text)
        if match:
            movie_name = match.group(1).strip()
            return 'similar', movie_name

    # Check for genre keywords
    for genre in GENRE_KEYWORDS:
        if genre in text:
            return 'genre', genre

    # Check for mood keywords
    for mood, keywords in MOOD_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return 'mood', mood

    # Default fallback
    return 'unknown', None


# ─────────────────────────────────────────
# GENERATE RESPONSE
# ─────────────────────────────────────────

def chat_response(user_input):
    intent, value = detect_intent(user_input)

    if intent == 'similar':
        result = recommend_similar(value)
        if result is None or result.empty:
            return (
                f"Sorry, I couldn't find a movie called **'{value}'** in the database. "
                f"Try another title!",
                None
            )
        return (
            f"🎬 Here are movies similar to **{value.title()}**:",
            result
        )

    elif intent == 'genre':
        result = recommend_by_genre(value)
        if result is None or result.empty:
            return (
                f"Sorry, no movies found for genre **'{value}'**.",
                None
            )
        return (
            f"🎭 Here are top **{value.title()}** movies:",
            result
        )

    elif intent == 'mood':
        result = recommend_by_mood(value)
        if result is None or result.empty:
            return (
                f"Sorry, couldn't find movies for that mood right now.",
                None
            )
        return (
            f"😊 Here are some **{value}** mood movies for you:",
            result
        )

    else:
        return (
            "🤖 I didn't quite understand that. Try saying:\n"
            "- *'Movies like Interstellar'*\n"
            "- *'Suggest comedy movies'*\n"
            "- *'I want something fun'*",
            None
        )


# ─────────────────────────────────────────
# CHAT HISTORY MANAGER
# ─────────────────────────────────────────

def init_chat_history():
    return []


def add_to_history(history, role, message):
    history.append({'role': role, 'message': message})
    return history


def format_history(history):
    formatted = ''
    for item in history:
        if item['role'] == 'user':
            formatted += f"🧑 **You:** {item['message']}\n\n"
        else:
            formatted += f"🤖 **Bot:** {item['message']}\n\n"
    return formatted