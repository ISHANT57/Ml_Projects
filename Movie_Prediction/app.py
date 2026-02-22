import pickle
import streamlit as st
import requests
import pandas as pd
# ----------------------------
# Fetch Poster from OMDb API
# ----------------------------
def fetch_poster(title):
    try:
        url = f"http://www.omdbapi.com/?t={title}&apikey=5eafd59c"
        response = requests.get(url)
        data = response.json()

        if data['Response'] == "True" and data['Poster'] != "N/A":
            return data['Poster']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"


# ----------------------------
# Recommendation Function
# ----------------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(fetch_poster(movie_title))

    return recommended_movie_names, recommended_movie_posters


# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender System (OMDb Powered)")

# Load pickle files
movies_dict = pickle.load(open('model/movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie",
    movie_list
)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])