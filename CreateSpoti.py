import spotipy
import re
from spotipy.oauth2 import SpotifyOAuth
from Key import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_USERNAME

def clean_song_name(song_name):
    if isinstance(song_name, str):
        cleaned_name = re.sub(r"[^a-zA-Z0-9\s]", "", song_name)
        return re.sub(r"\s+", " ", cleaned_name).strip()
    return str(song_name)

def get_spotify_track_id(sp, song_name, artist_name, not_found_count):
    query = f"track:{song_name} artist:{artist_name}"
    result = sp.search(q=query, type='track', limit=1)

    if result['tracks']['items']:
        return result['tracks']['items'][0]['id'], not_found_count

    print(f"Spotify track ID not found for '{song_name}' by '{artist_name}'.")
    return None, not_found_count + 1

def create_spotify_playlist(songs):
    # Authenticate the user and create a new playlist
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='playlist-modify-public'))
    not_found_count = 0
    
    try:
        user_id = sp.me()['id']
        playlist_name = f"Most played songs"
        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
        
        track_ids = []
        for song_entry, _ in songs:
            song_name, artist_name = song_entry.rsplit(' by ', 1)
            
            if not song_name.strip():  # Check if the song name is empty or contains only spaces
                print(f"Skipping empty song entry with artist: {artist_name}")
                continue

            track_id, not_found_count = get_spotify_track_id(sp, song_name, artist_name, not_found_count)
            if track_id:
                track_ids.append(track_id)



        song_uris_or_ids = [f"spotify:track:{song_id}" for song_id in track_ids]
        if song_uris_or_ids:
            sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris_or_ids)
        else:
            print("No valid songs found to add to the playlist.")
        
        songs_added = len(track_ids)
        songs_failed = len(songs) - songs_added
        print(f"Playlist '{playlist_name}' created with {songs_added} tracks.")
        print(f"{songs_failed} songs failed to be found on Spotify")
        print(f"View the playlist here: {playlist['external_urls']['spotify']}")
    
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error creating the playlist: {e}")
        print("Make sure you have the correct Spotify API credentials and permissions.")
