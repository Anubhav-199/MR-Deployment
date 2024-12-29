import streamlit as st
import pickle
import pandas as pd
import os
import requests


def fetch_poster(movie_id):
    """Fetches the movie poster URL using TMDb API."""
    api_key = os.getenv("TMDB_API_KEY")  # Fetch the API key from environment variables
    if not api_key:
        raise ValueError("TMDB_API_KEY environment variable is not set or accessible.")

    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    try:
        response = requests.get(url, timeout=10)  # Timeout set to 10 seconds
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"


def recommend(movie):
    """Recommends similar movies based on the selected movie."""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        recommended_movies_posters.append(poster_url)
    return recommended_movies, recommended_movies_posters


# Load the movie dataset and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Ensure that the DataFrame has the correct structure
if 'movie_id' not in movies.columns:
    raise ValueError("The DataFrame must include a 'movie_id' column.")

similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set the title for the Streamlit app
st.title('Movie Recommender System')

# User selects a movie
selected_movie_name = st.selectbox('Search your Movie', movies['title'].values)

# When the user clicks 'Recommend', show the recommended movies and their posters
if st.button('Recommend'):
    if not selected_movie_name:
        st.error("Please select a movie.")
    else:
        names, posters = recommend(selected_movie_name)

        if len(names) == 0 or len(posters) == 0:
            st.error("No recommendations found for the selected movie.")
        else:
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(names[0])
                st.image(posters[0])
            with col2:
                st.text(names[1])
                st.image(posters[1])
            with col3:
                st.text(names[2])
                st.image(posters[2])
            with col4:
                st.text(names[3])
                st.image(posters[3])
            with col5:
                st.text(names[4])
                st.image(posters[4])





















