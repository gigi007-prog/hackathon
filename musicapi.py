import requests

# Replace with your API key
API_KEY = 'd6f35ef82e0c36cd064c1b6d5c47ed9b'
BASE_URL = 'http://ws.audioscrobbler.com/2.0/'

def get_calming_tracks():
    params = {
        'method': 'tag.gettoptracks',
        'tag': 'meditation',
        'api_key': API_KEY,
        'format': 'json',
        'limit': 10  # Adjust the limit as needed
    }

    response = requests.get(BASE_URL, params=params)
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
