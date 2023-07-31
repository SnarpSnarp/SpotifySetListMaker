import spotipy
import re
from spotipy.oauth2 import SpotifyOAuth
from Key import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_USERNAME

def clean_song_name(song_name):
    if isinstance(song_name, str):
        cleaned_name = re.sub(r"[^a-zA-Z0-9\s]", "", song_name)
        return re.sub(r"\s+", " ", cleaned_name).strip()
    return str(song_name)

def get_spotify_track_id(sp, song_name, artist_name):
    query = f"track:{song_name} artist:{artist_name}"
    result = sp.search(q=query, type='track', limit=1)

    if result['tracks']['items']:
        return result['tracks']['items'][0]['id']

    print(f"Spotify track ID not found for '{song_name}' by '{artist_name}'.")
    return None


def create_spotify_playlist(songs, playlist_name):
    # Authenticate the user and create a new playlist
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,                                                   client_secret=SPOTIPY_CLIENT_SECRET,                                                  redirect_uri=SPOTIPY_REDIRECT_URI,                                                   scope='playlist-modify-public'))
    try:
        # Get the user ID
        user_id = sp.me()['id']

        # Create the playlist
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        # Get the track URIs or IDs from the songs list
        song_uris_or_ids = [f"spotify:track:{song_id}" for song_id, _ in songs]
        # Add the tracks to the playlist
        sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris_or_ids)
        print(f"Playlist '{playlist_name}' created with {len(songs)} tracks.")
        print(f"View the playlist here: {playlist['external_urls']['spotify']}")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error creating the playlist: {e}")
        print("Make sure you have the correct Spotify API credentials and permissions.")
