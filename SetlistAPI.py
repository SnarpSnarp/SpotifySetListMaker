import requests
import xml.etree.ElementTree as ET
from Key import SETLIST_API_KEY

SETLIST_API_BASE_URL = 'https://api.setlist.fm/rest/1.0/'

def get_most_played_songs(artist_id):
    url = f"{SETLIST_API_BASE_URL}artist/{artist_id}/setlists"
    headers = {'x-api-key': SETLIST_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the XML response
        root = ET.fromstring(response.content)

        songs_counter = {}
        for setlist in root.findall('.//setlist'):
            setlist_artist_name = setlist.find('.//artist').get('name')
            for song in setlist.findall('.//song'):
                song_name = song.get('name')
                cover_artist = song.find('.//cover')
                if cover_artist is not None:
                    artist_name = cover_artist.get('name')
                else:
                    artist_name = setlist_artist_name  # Use the setlist artist name if there's no cover artist
                song_entry = f"{song_name} by {artist_name}"
                songs_counter[song_entry] = songs_counter.get(song_entry, 0) + 1

        sorted_songs = sorted(songs_counter.items(), key=lambda x: x[1], reverse=True)
        return sorted_songs

    except requests.exceptions.RequestException as e:
        print(f"Error while retrieving data from Setlist.fm: {e}")
        return None
    except Exception as e:
        print("Error parsing the API response:", e)
        return None

