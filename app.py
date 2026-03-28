import pandas as pd
import streamlit as st

# --- STEP 1: LOAD THE DATA ---
# I used pandas to read our Excel "Database"
def load_data():
    # creating a small sample of  1000+ entry logic
    data = {
        'Title': ['Inception', 'Interstellar', 'The Prestige', 'The Dark Knight', 'Avatar', 'Titanic'],
        'Director': ['Christopher Nolan', 'Christopher Nolan', 'Christopher Nolan', 'Christopher Nolan', 'James Cameron', 'James Cameron'],
        'Genre_1': ['Sci-Fi', 'Sci-Fi', 'Drama', 'Action', 'Sci-Fi', 'Drama'],
        'Genre_2': ['Action', 'Drama', 'Mystery', 'Crime', 'Adventure', 'Romance'],
        'Vibe': ['Mind-bending', 'Emotional', 'Mysterious', 'Dark', 'Visual', 'Romantic'],
        'Rating': ['PG-13', 'PG-13', 'PG-13', 'PG-13', 'PG-13', 'PG-13']
    }
    return pd.DataFrame(data)

df = load_data()

# --- STEP 2: DATA CLEANING ---
# I make everything lowercase so searching is "case-insensitive"
for col in ['Director', 'Genre_1', 'Genre_2', 'Vibe']:
    df[col] = df[col].str.lower().str.strip()

# --- STEP 3: THE RECOMMENDATION LOGIC (NON-ML) ---
def get_recommendations(selected_movie):
    # Get the attributes of the movie the user picked
    movie_row = df[df['Title'] == selected_movie].iloc[0]
    
    # Create a 'Score' column for all movies, starting at 0
    df['Score'] = 0
    
    for index, row in df.iterrows():
        if row['Title'] == selected_movie:
            continue # Skip the movie itself
        
        current_score = 0
        
        # Rule 1: Same Director? (Big match!)
        if row['Director'] == movie_row['Director']:
            current_score += 5
            
        # Rule 2: Primary Genre match?
        if row['Genre_1'] == movie_row['Genre_1']:
            current_score += 3
            
        # Rule 3: Secondary Genre match?
        if row['Genre_2'] == movie_row['Genre_2']:
            current_score += 2
            
        # Rule 4: Same Vibe?
        if row['Vibe'] == movie_row['Vibe']:
            current_score += 1
            
        df.at[index, 'Score'] = current_score

    # Sort movies by score (highest first) and return top 3
    return df.sort_values(by='Score', ascending=False).head(3)

# --- STEP 4: STREAMLIT UI (THE PRESENTATION) ---
st.title("🎬 Movie Recommendation")
st.write("A Logic-Based Recommendation System by **Anirban Bhowmik**")

user_choice = st.selectbox("Pick a movie you liked:", df['Title'].values)

if st.button('Find Recommendations'):
    results = get_recommendations(user_choice)
    
    st.subheader(f"Because you liked {user_choice}, you might enjoy:")
    for i, row in results.iterrows():
        st.write(f"**{row['Title']}** (Match Score: {row['Score']})")
        st.caption(f"Directed by {row['Director'].title()} | Genre: {row['Genre_1'].title()}")