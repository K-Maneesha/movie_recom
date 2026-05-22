# 🎬 WatchGenie - AI Movie Recommendation System

## 🧾 Project Description

WatchGenie is an AI-based movie recommendation system built using Python and Streamlit. It recommends movies based on movie content, mood, genre, group preferences, and chatbot interaction.

The system uses **TF-IDF Vectorization** and **Cosine Similarity** to recommend similar movies based on movie descriptions.

---

# 🔗 Deployment Link

https://movierecom-ah8rx5x5uevbiydcwsadj9.streamlit.app/

---

# ⚙️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Plotly
- Regex
- JSON
- VS Code

---

# 🧠 ML Techniques Used

- Content-Based Filtering
- TF-IDF Vectorization
- Cosine Similarity
- Rule-Based Chatbot
- Mood-Based Filtering
- Genre-Based Filtering

---

# 🚀 Main Features

- Similar movie recommendation
- Mood-based movie suggestions
- Genre-based recommendation
- Group movie recommendation
- AI chatbot interaction
- Language, year, and rating filters
- Analytics dashboard
- Interactive Streamlit UI

---

# 📦 Modules

## 📂 Data Processing Module

- Loads TMDB movie dataset
- Handles missing values
- Extracts release year
- Converts genre JSON into readable format
- Maps movie genres to moods

---

## 🎯 Recommendation Module

- Recommends movies using TF-IDF and cosine similarity
- Suggests movies by mood
- Suggests movies by genre
- Provides group recommendations

---

## 🤖 Chatbot Module

- Detects user intent
- Understands inputs like “movies like Interstellar”
- Suggests movies based on mood, genre, or similarity

---

## 📊 Dashboard Module

- Shows top-rated movies
- Displays genre analysis
- Shows mood distribution
- Displays rating trends

---

# 🗄️ Dataset

The system uses the **TMDB 5000 Movies Dataset**.

### Dataset File
```bash
tmdb_5000_movies.csv
```

### Dataset Includes

- Movie title
- Genre
- Language
- Release year
- Rating
- Overview / description
- Popularity

---

# ▶️ Project Setup

## Step 1: Clone Repository

```bash
git clone https://github.com/K-Maneesha/movie_recom.git
```

---

## Step 2: Open Project Folder

```bash
cd movie_recom
```

---

## Step 3: Install Required Libraries

```bash
python -m pip install -r requirements.txt
```

### Or install manually

```bash
python -m pip install pandas numpy scikit-learn streamlit plotly
```

---

## Step 4: Run the Application

```bash
python -m streamlit run app.py
```

---

# 👩‍💻 Team Members

- Dhasamashri N
- Harshini Durga V
- Madhumitha V
- Maneesha K
- Manju Mahalakshmi P

---

# 🏁 Conclusion

WatchGenie improves movie discovery by using content-based filtering, TF-IDF vectorization, cosine similarity, mood-based recommendation, and chatbot interaction.

It provides a simple and interactive way for users to find suitable movies.

---

# 🔮 Future Enhancement

- User login and profile management
- Deep learning-based recommendations
- Advanced NLP chatbot
- Voice-based chatbot assistant
- IMDb / Netflix API integration
- Movie poster display
- Mobile app deployment

---
