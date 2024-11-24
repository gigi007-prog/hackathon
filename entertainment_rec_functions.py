import random
import requests
from config import *
from terminal_effects import *

# Entertainment suggestions
def recommend_movies():
    """
    This function asks the user to pick a genre, uses TheMovieDB API to get a list of popular movies within that genre, saves the movie names to a list and then selects a random  movie from the list to return to the user.
    """

    print("\nMovies sound like a great idea!")

    movie_recommendations = []

    # Asks the user to select a movie genre and saves the selection to a variable
    genre_num = int(input("\nWhat genre movie would you like? Input a number for a movie suggestion in the corresponding genre.\n1 - Action    2 - Comedy    3 - Drama    4 - Thriller\n5 - Horror    6 - Romance    7 - Science Fiction    8 - Fantasy\n"))

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

    try:
        # Call the API with the URL (and parameters) and keys
        response = requests.get(url, headers=headers)
        # Convert the URL into a queryable json format
        response_data = response.json()
    
        # Now push only the title of the movie recommendations into a list
        for movie in response_data["results"]:
            movie_recommendations.append(movie["title"])
    
        # Select a random title from the list
        print(f"\nWhy not watch '{random.choice(movie_recommendations)}'")
    except:
        print("\n--- Can not connect to TheMovieDB API. (ensure you are online and you've added the API keys to the config file) ---\n")

def get_calming_music():
    """
    Uses LastFM API to return a calming music playlist.
    """

    print("\nMusic it is! A calming tune can work wonders. Let me grab something for you…")

    music_recommendations = []
    
    # Parameters for calling the API (can update the parameters for different limits, tags etc.)
    params = {
        'method': 'tag.gettoptracks',
        'tag': 'meditation',
        'api_key': LASTFM_API,
        'format': 'json',
        'limit': 10
    }

    try:
        # Calling the API with the parameters
        response = requests.get('http://ws.audioscrobbler.com/2.0/', params=params)
        # Saving the response as JSON format
        response_data = response.json()
        # Getting specifically the track data (avoiding the excess data alongside the API response)
        tracks = response_data.get('tracks', {}).get('track', [])

        # Pushing just the relevant track data to a list
        for track in tracks:
            music_recommendations.append(f"{track['name']} by {track['artist']['name']} - {track['url']}")

        # Selecting a random track from the list to return to the user
        print(f"\nHere's a song for you: {random.choice(music_recommendations)}")
    except:
        print("\n--- Can not connect to LastFM API (ensure you are online and you've added the API keys to the config file). ---\n")

def suggest_recipe():
    """
    Connects to TheMealDB API for a random recipe.
    """

    print("\nCooking is a wonderful way to relax! Let me fetch a recipe for you…")

    try:
        # Calling the API for a random recipe
        response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')

        # saving the response as json format
        data = response.json()
        # getting specifically the meal data, avoiding any excess response info
        meal = data.get('meals', [])[0]
        # printing the relevant parts to the recipe
        print(f"\n\nHow about trying this: {meal['strMeal']}? Quick, easy, and oh-so-comforting.\n----------\n\n")
        print(f"Category: {meal['strCategory']}\n")
        print(f"Instructions: {meal['strInstructions']}\n")
        print(f"Recipe URL: {meal['strSource']}")
    except:
        print("\n--- Can not connect to TheMealDB API (ensure you are online and you've added the API keys to the config file). ---")

def breathing_exercises():
    """
    Guides the user through meditation to help relax them, uses terminal for instructions.
    """
    print("When times are tough, sometimes you just need to take a moment, focus on your breathing and try relax. Let's start a guided breathing session.")
    input("\nPress enter to start")
    
    for i in range(3): 
        # prints "breathe in", blinking for three seconds
        blinking_effect("Breathe In...", duration=5, interval=0.7)
        
        typewriter_effect("Hold your breath for 6 seconds...")
        # waits for 7 seconds
        time.sleep(6)
        
        typewriter_effect("Exhale slowly for 6 seconds...")
        time.sleep(6)
        
        typewriter_effect("Great job! Let's do that again.")
        time.sleep(2)

    typewriter_effect("You've completed the exercise. Feel better already, don't you? 😊")