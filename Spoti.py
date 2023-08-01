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

def create_spotify_playlist(songs, artist_name):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='playlist-modify-public'))
    try:
        user_id = sp.me()['id']
        playlist_name = (f"{artist_name} Most played songs")
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        cleaned_songs = [(clean_song_name(song), count) for song, count in songs]
        track_ids = []
        for song, _ in cleaned_songs:
            track_id = get_spotify_track_id(sp, song, artist_name)
            if track_id:
                track_ids.append((track_id, 1))
        song_uris_or_ids = [f"spotify:track:{song_id}" for song_id, _ in track_ids]
        sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris_or_ids)
        print(f"Playlist '{playlist_name}' created with {len(songs)} tracks.")
        print(f"View the playlist here: {playlist['external_urls']['spotify']}")
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error creating the playlist: {e}")
        print("Make sure you have the correct Spotify API credentials and permissions.")