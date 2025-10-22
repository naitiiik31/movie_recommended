import streamlit as st
import pickle
import pandas as pd
import requests 

def fetch_poster(movie_title):
    api_key = "3c99009e" 
    
    url = f"https://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    
    try:
        data = requests.get(url)
        data.raise_for_status()  
        data = data.json()
        
        poster_path = data.get('Poster', '')
        
        if poster_path == 'N/A' or poster_path == '':
            return "https://via.placeholder.com/500x750.png?text=Poster+Not+Found"
        else:
            return poster_path
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for {movie_title}: {e}")
        return "https://via.placeholder.com/500x750.png?text=API+Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_names = []
    recommended_movies_posters = [] 

    for i in movies_list:
        title = movies.iloc[i[0]].title
        
        recommended_movies_posters.append(fetch_poster(title))
        
        recommended_movies_names.append(title)
        
    return recommended_movies_names, recommended_movies_posters

try:
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error: 'movies_dict.pkl' or 'similarity.pkl' not found. Make sure the files are in the same directory as app.py.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred loading pickle files: {e}")
    st.stop()


st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies['title'].values)

if st.button('Recommend'):
    with st.spinner('Finding recommendations...'):
        names, posters = recommend(selected_movie_name)

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