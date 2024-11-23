import requests
import random

TMDB_API = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjZTIwZDU5MDQyM2ZkYTdhYjZiYTAzNzBhNzgxZWE2NSIsIm5iZiI6MTczMjIxMjI4NS42NDI2NTU0LCJzdWIiOiI2NzNmNzU5ODIxZGE0Mjk2N2ZjNDk5OGIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.Y4ujNx-dUqlIjR2oFFrpGZe7Kl14e57ux3IJ0RxU3us'
LASTFM_API = 'd6f35ef82e0c36cd064c1b6d5c47ed9b'

stress_level = 22

def recommend_movies():
    """
    This function asks the user to pick a genre, uses TheMovieDB API to get a list of popular movies within that genre, saves the movie names to a list and then selects a random  movie from the list to return to the user.
    """

    print("Movies sound like a great idea!")

    movie_recommendations = []

    # Asks the user to select a movie genre and saves the selection to a variable
    genre_num = int(input("What genre movie would you like? Input a number for a movie suggestion in the corresponding genre.\n1 - Action    2 - Comedy    3 - Drama    4 - Thriller\n5 - Horror    6 - Romance    7 - Science Fiction    8 - Fantasy\n"))

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
    print(f"Why not watch '{random.choice(movie_recommendations)}'")

def get_calming_music():
    """
    Uses LastFM API to return a calming music playlist.
    """

    print("Music it is! A calming tune can work wonders. Let me grab something for you…")

    music_recommendations = []
    
    # Parameters for calling the API (can update the parameters for different limits, tags etc.)
    params = {
        'method': 'tag.gettoptracks',
        'tag': 'meditation',
        'api_key': LASTFM_API,
        'format': 'json',
        'limit': 10
    }
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
    print(f"Here's a song for you: {random.choice(music_recommendations)}")

def suggest_recipe():
    """
    Connects to TheMealDB API for a random recipe.
    """

    print("Cooking is a wonderful way to relax! Let me fetch a recipe for you…")

    # Calling the API for a random recipe
    response = requests.get('https://www.themealdb.com/api/json/v1/1/random.php')

    # saving the response as json format
    data = response.json()
    # getting specifically the meal data, avoiding any excess response info
    meal = data.get('meals', [])[0]
    # printing the relevant parts to the recipe
    print(f"How about trying this: {meal['strMeal']}? Quick, easy, and oh-so-comforting.")
    print(f"Category: {meal['strCategory']}")
    print(f"Instructions: {meal['strInstructions']}")
    print(f"Recipe URL: {meal['strSource']}")

def entertainment_recommendation(stress_level):

    if stress_level < 0 or stress_level > 10:
        print("Although times can be stressful and make it hard to focus, please input a number between  0 - 10 so we can provide proper help.")

    elif stress_level == 0:
        # They're officially stress free, nice message and maybe recommendation
        pass

    elif stress_level <=3:
        # Low stress - Goal: light entertainment to relax further
        print("Hey there! It seems like you might need a little boost. Let's make your day a bit brighter! I have three great suggestions for you:\n\t1 - Watch a relaxing movie to unwind\n\t2 - Listen to some calming music to lift your spirits\n\t3 - Try a fun recipe for some therapeutic cooking\n")

        suggest_entertainment = True
        something_else = True

        while suggest_entertainment == True:
            entertainment_selection = (input("Which one sounds good to you? Please type `movie`, `music`, or `recipe` to choose!\n"))

            if entertainment_selection == "movie":
                suggest_entertainment = False
                something_else = True
                recommend_movies()
                
                while something_else == True:
                    something_else_input = input("Would you like a different recommendation? Input 'yes' if so, or anything else if not.")
                    if something_else_input == 'yes':
                        recommend_movies()
                    else:
                        something_else = False
                        print("Looks like you've decided on your movie, enjoy!")

            elif entertainment_selection == "music":
                suggest_entertainment = False
                something_else = True
                get_calming_music()

                while something_else == True:
                    something_else_input = input("Would you like a different recommendation? Input 'yes' if so, or anything else if not.")
                    if something_else_input == 'yes':
                        get_calming_music()
                    else:
                        something_else = False
                        print("Looks like you've decided on your music, enjoy!")

            elif entertainment_selection == "recipe":
                suggest_entertainment = False
                something_else = True
                suggest_recipe()

                while something_else == True:
                    something_else_input = input("Would you like a different recommendation? Input 'yes' if so, or anything else if not.")
                    if something_else_input == 'yes':
                        suggest_recipe()
                    else:
                        something_else = False
                        print("Looks like you've decided on your recipe, bon apetit!")
            else:
                print("Whoops! That wasn't a valid input. Let's try that again.")

    elif stress_level <=6:
        # Medium stress level, suggest a video for meditation or a meditation technique
        pass

    elif stress_level <=9:
        # Very high stress level. Make multiple suggestion as this is the highest stress/anxiety level. Something like breathing technique or some other more serious remedies
        pass

    elif stress_level == 10:
        # Super high, suggestions and tell to talk to someone or write things down.
        pass

entertainment_recommendation(int(input("On a scale of 1-10, how are you feeling?")))