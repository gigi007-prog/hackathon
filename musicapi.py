import requests

# Replace with your API key
API_KEY = 
BASE_URL = 

def get_calming_tracks():
    params = {
        'method': 'tag.gettoptracks',
        'tag': 'meditation',
        'api_key': API_KEY,
        'format': 'json',
        'limit': 10  # Adjust the limit as needed
    }

    response = requests.get('http://ws.audioscrobbler.com/2.0/', params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = data.get('tracks', {}).get('track', [])
        if not tracks:
            print("No tracks found for the given tag.")
            return
        
        print("Top Calming Tracks:")
        for track in tracks:
            name = track['name']
            artist = track['artist']['name']
            url = track['url']
            print(f"{name} by {artist} - {url}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

# Run the function
get_calming_tracks()
