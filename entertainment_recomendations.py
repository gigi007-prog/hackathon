import requests
import random

TMDB_API = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjZTIwZDU5MDQyM2ZkYTdhYjZiYTAzNzBhNzgxZWE2NSIsIm5iZiI6MTczMjIxMjI4NS42NDI2NTU0LCJzdWIiOiI2NzNmNzU5ODIxZGE0Mjk2N2ZjNDk5OGIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.Y4ujNx-dUqlIjR2oFFrpGZe7Kl14e57ux3IJ0RxU3us'

stress_level = 22

def recommend_movies():
    """
    This function asks the user to pick a genre, uses TheMovieDB API to get a list of popular movies within that genre, saves the movie names to a list and then selects a random  movie from the list to return to the user.
    """
    
    movie_recommendations = []

    # Asks the user to select a movie genre and saves the selection to a variable
    genre_num = int(input("What genre movie would you like? Input a number for the corresponding movies.\n1 - Action    2 - Comedy    3 - Drama    4 - Thriller\n5 - Horror    6 - Romance    7 - Science Fiction    8 - Fantasy\n"))

    # An empty variable we'll use to store the selected genre
    genre = ''

    # TheMovieDB attributes an id for each genre, this matches the correct genre id to the users input and then updates the genre variable with the appropriate value
    if genre_num == 1:
        genre = '28'
    elif genre_num == 2:
        genre = '35'
    elif genre_num == 3:
        genre = '53'
    elif genre_num == 4:
        genre = '27'
    elif genre_num == 5:
        genre = '10749'
    elif genre_num == 6:
        genre = '878'
    elif genre_num == 7:
        genre = '14'

    # The API URL with the user specified genre being passed as an argument
    url = f'https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc&with_genres={genre}'

    # The API keys from the account to enable the API to work
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_API}"
    }

    # Call the API with the URL (and parameters) and keys
    response = requests.get(url, headers=headers)
    # Convert the URL into a queryable json format
    response_data = response.json()
    
    # Now push only the title of the movie recommendations into a list
    for movie in response_data["results"]:
        movie_recommendations.append(movie["title"])
    
    # Select a random title from the list
    return(random.choice(movie_recommendations))

def music_playlist():
    """
    Uses SpotifyAPI to return a calming music playlist.
    """




def entertainment_recommendation(stress_level):

    if stress_level < 0 or stress_level > 10:
        print("Although times can be stressful and make it hard to focus, please input a number between  0 - 10 so we can provide proper help.")

    elif stress_level == 0:
        # They're officially stress free, nice message and maybe recommendation
        pass

    elif stress_level <3:
        # Low stress - Goal: light entertainment to relax further
        print("Why not watch a movie?")
        print(recommend_movies())
        # Simple suggestions like drinking tea, watching movie, eating favourite food etc.
        pass

    elif stress_level <6:
        # Medium stress level, suggest a video for meditation or a meditation technique
        pass

    elif stress_level <9:
        # Very high stress level. Make multiple suggestion as this is the highest stress/anxiety level. Something like breathing technique or some other more serious remedies
        pass

    elif stress_level == 10:
        # Super high, suggestions and tell to talk to someone or write things down.
        pass

entertainment_recommendation(int(input("On a scale of 1-10, how are you feeling?")))