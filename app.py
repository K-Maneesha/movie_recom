import streamlit as st
import pandas as pd
import plotly.express as px
from recommender import recommend_by_mood, recommend_similar, recommend_for_group, recommend_by_genre
from chatbot import chat_response, init_chat_history, add_to_history
from utils import load_data

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="🎬 AI Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ─────────────────────────────────────────
# LANGUAGE CODE TO FULL NAME MAP
# ─────────────────────────────────────────
language_map = {
    'en': 'English', 'hi': 'Hindi', 'fr': 'French',
    'es': 'Spanish', 'de': 'German', 'it': 'Italian',
    'ja': 'Japanese', 'ko': 'Korean', 'zh': 'Chinese',
    'pt': 'Portuguese', 'ru': 'Russian', 'ar': 'Arabic',
    'ta': 'Tamil', 'te': 'Telugu', 'ml': 'Malayalam',
    'bn': 'Bengali', 'tr': 'Turkish', 'nl': 'Dutch',
    'sv': 'Swedish', 'pl': 'Polish', 'da': 'Danish',
    'fi': 'Finnish', 'no': 'Norwegian', 'th': 'Thai',
    'id': 'Indonesian', 'ro': 'Romanian', 'hu': 'Hungarian',
    'cs': 'Czech', 'uk': 'Ukrainian', 'he': 'Hebrew',
    'fa': 'Persian',
}

def get_full_language_name(code):
    return language_map.get(code, code.upper())

# Map language codes in dataframe to full names
df['language'] = df['language'].apply(
    lambda x: language_map.get(x, x) if isinstance(x, str) else x
)

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
st.sidebar.title("🎬 Movie AI")
st.sidebar.markdown("---")

page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "🎭 Mood Recommender",
    "🤖 AI Chatbot",
    "👥 Group Recommender",
    "📊 Analytics Dashboard"
])

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filters")

# Full language names in dropdown
languages = ['All'] + sorted(df['language'].dropna().unique().tolist())
selected_language = st.sidebar.selectbox("Language", languages)

year_min = int(df['year'].min()) if df['year'].min() > 0 else 1990
year_max = int(df['year'].max())
year_range = st.sidebar.slider("Year Range", year_min, year_max, (2000, year_max))

min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0, 0.5)

# ─────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────
if page == "🏠 Home":
    st.title("🎬 AI Movie Recommendation System")
    st.markdown("### Welcome! Discover your next favourite movie using AI 🤖")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎬 Total Movies", len(df))
    col2.metric("🌍 Languages", df['language'].nunique())
    col3.metric("⭐ Avg Rating", f"{df['rating'].mean():.1f}")
    col4.metric("📅 Year Range", f"{year_min} - {year_max}")

    st.markdown("---")
    st.subheader("🔥 Top 10 Highest Rated Movies")
    top10 = df.sort_values('rating', ascending=False).head(10)[
        ['title', 'genre', 'language', 'year', 'rating']
    ]
    st.dataframe(top10, use_container_width=True)

    st.markdown("---")
    st.subheader("🎭 Browse by Genre")
    selected_genre = st.selectbox("Pick a Genre", [
        'Action', 'Comedy', 'Drama', 'Romance',
        'Thriller', 'Science Fiction', 'Animation', 'Family'
    ])
    genre_results = recommend_by_genre(
        selected_genre,
        language=selected_language if selected_language != 'All' else None,
        year_range=year_range,
        min_rating=min_rating
    )
    if not genre_results.empty:
        st.dataframe(genre_results, use_container_width=True)
    else:
        st.warning("No movies found. Try adjusting filters.")


# ─────────────────────────────────────────
# MOOD RECOMMENDER
# ─────────────────────────────────────────
elif page == "🎭 Mood Recommender":
    st.title("🎭 Mood-Based Movie Recommender")
    st.markdown("Tell us how you feel and we'll find the perfect movie!")
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("😊 Happy", use_container_width=True):
            st.session_state['mood'] = 'Happy'
    with col2:
        if st.button("😢 Sad", use_container_width=True):
            st.session_state['mood'] = 'Sad'
    with col3:
        if st.button("🔥 Action", use_container_width=True):
            st.session_state['mood'] = 'Action'

    if 'mood' in st.session_state:
        mood = st.session_state['mood']
        st.success(f"Showing movies for **{mood}** mood!")
        st.markdown("---")

        results = recommend_by_mood(
            mood,
            language=selected_language if selected_language != 'All' else None,
            year_range=year_range,
            min_rating=min_rating
        )

        if not results.empty:
            for _, row in results.iterrows():
                with st.expander(f"🎬 {row['title']} ⭐ {row['rating']}"):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"**Genre:** {row['genre']}")
                        st.markdown(f"**Language:** {row['language']}")
                        st.markdown(f"**Year:** {row['year']}")
                        st.markdown(f"**Rating:** {row['rating']}")
                    with col2:
                        st.markdown(f"**Description:**")
                        st.write(row['description'])
        else:
            st.warning("No movies found. Try adjusting the filters!")


# ─────────────────────────────────────────
# AI CHATBOT
# ─────────────────────────────────────────
elif page == "🤖 AI Chatbot":
    st.title("🤖 AI Movie Chatbot")
    st.markdown("Ask me anything! Try: *'Movies like Interstellar'* or *'I want something funny'*")
    st.markdown("---")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = init_chat_history()

    # Display chat history
    for item in st.session_state['chat_history']:
        if item['role'] == 'user':
            with st.chat_message("user"):
                st.write(item['message'])
        else:
            with st.chat_message("assistant"):
                st.write(item['message'])
                if item.get('data') is not None:
                    st.dataframe(item['data'], use_container_width=True)

    # Chat input
    user_input = st.chat_input("Type your movie request here...")

    if user_input:
        st.session_state['chat_history'] = add_to_history(
            st.session_state['chat_history'], 'user', user_input
        )

        response_text, response_data = chat_response(user_input)

        st.session_state['chat_history'].append({
            'role': 'bot',
            'message': response_text,
            'data': response_data
        })

        st.rerun()


# ─────────────────────────────────────────
# GROUP RECOMMENDER
# ─────────────────────────────────────────
elif page == "👥 Group Recommender":
    st.title("👥 Group Movie Recommender")
    st.markdown("Add multiple users with different moods and get combined recommendations!")
    st.markdown("---")

    if 'group_moods' not in st.session_state:
        st.session_state['group_moods'] = []

    col1, col2 = st.columns([2, 1])
    with col1:
        user_name = st.text_input("User Name", placeholder="e.g. Alice")
    with col2:
        user_mood = st.selectbox("Their Mood", ['Happy', 'Sad', 'Action'])

    if st.button("➕ Add User"):
        if user_name:
            st.session_state['group_moods'].append({
                'name': user_name,
                'mood': user_mood
            })
            st.success(f"Added {user_name} ({user_mood})")

    if st.session_state['group_moods']:
        st.markdown("### 👥 Current Group")
        for i, member in enumerate(st.session_state['group_moods']):
            col1, col2, col3 = st.columns([2, 2, 1])
            col1.write(f"👤 {member['name']}")
            col2.write(f"🎭 {member['mood']}")
            if col3.button("❌", key=f"remove_{i}"):
                st.session_state['group_moods'].pop(i)
                st.rerun()

        st.markdown("---")
        if st.button("🎬 Get Group Recommendations", use_container_width=True):
            mood_list = [m['mood'] for m in st.session_state['group_moods']]
            results = recommend_for_group(mood_list)

            if not results.empty:
                st.success(f"Found {len(results)} movies everyone might enjoy!")
                st.dataframe(results, use_container_width=True)
            else:
                st.warning("No results found. Try different moods!")

        if st.button("🗑️ Clear Group"):
            st.session_state['group_moods'] = []
            st.rerun()


# ─────────────────────────────────────────
# ANALYTICS DASHBOARD
# ─────────────────────────────────────────
elif page == "📊 Analytics Dashboard":
    st.title("📊 Movie Analytics Dashboard")
    st.markdown("Insights from the TMDB movie dataset")
    st.markdown("---")

    # Filter data for charts
    chart_df = df.copy()
    if selected_language != 'All':
        chart_df = chart_df[chart_df['language'] == selected_language]
    chart_df = chart_df[
        (chart_df['year'] >= year_range[0]) &
        (chart_df['year'] <= year_range[1]) &
        (chart_df['rating'] >= min_rating)
    ]

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Top Genres")
        genre_counts = chart_df['genre'].str.split(', ').explode().value_counts().head(10)
        fig1 = px.bar(
            x=genre_counts.values,
            y=genre_counts.index,
            orientation='h',
            labels={'x': 'Count', 'y': 'Genre'},
            color=genre_counts.values,
            color_continuous_scale='Viridis'
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("🥧 Mood Distribution")
        mood_counts = chart_df['mood'].value_counts()
        fig2 = px.pie(
            values=mood_counts.values,
            names=mood_counts.index,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📈 Ratings Trend Over Years")
        yearly_rating = chart_df.groupby('year')['rating'].mean().reset_index()
        yearly_rating = yearly_rating[yearly_rating['year'] > 1980]
        fig3 = px.line(
            yearly_rating,
            x='year',
            y='rating',
            labels={'year': 'Year', 'rating': 'Avg Rating'},
            color_discrete_sequence=['#00CC96']
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("🌍 Movies by Language")
        lang_counts = chart_df['language'].value_counts().head(10)
        fig4 = px.bar(
            x=lang_counts.index,
            y=lang_counts.values,
            labels={'x': 'Language', 'y': 'Count'},
            color=lang_counts.values,
            color_continuous_scale='Blues'
        )
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    # Row 3 - Full width
    st.subheader("⭐ Rating Distribution")
    fig5 = px.histogram(
        chart_df,
        x='rating',
        nbins=20,
        labels={'rating': 'Rating', 'count': 'Number of Movies'},
        color_discrete_sequence=['#636EFA']
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")
    st.subheader("📋 Full Dataset Preview")
    st.dataframe(chart_df.head(50), use_container_width=True)