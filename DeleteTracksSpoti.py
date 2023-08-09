import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Key import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_USERNAME

def delete_tracks_from_playlist():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='playlist-modify-public,playlist-modify-private'))
    
    playlists = sp.current_user_playlists()['items']

    for idx, playlist in enumerate(playlists):
        print(f"{idx + 1}. {playlist['name']} ({playlist['tracks']['total']} tracks)")

    while True:
        try:
            selected_playlist_idx = int(input("Enter the number of the playlist you want to edit (or 0 to exit): ")) - 1
            if selected_playlist_idx == -1:
                return
            selected_playlist = playlists[selected_playlist_idx]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please choose a valid playlist number.")

    tracks = sp.playlist_items(selected_playlist['id'])['items']

    for idx, track in enumerate(tracks):
        print(f"{idx + 1}. {track['track']['name']} by {track['track']['artists'][0]['name']}")

    while True:
        tracks_to_delete = input("Enter track numbers to delete separated by commas (e.g., 1,4,5), or type 'back' to return to playlist selection: ")

        if tracks_to_delete.lower() == 'back':
            delete_tracks_from_playlist()
            return

        try:
            track_ids_to_delete = [tracks[int(idx) - 1]['track']['id'] for idx in tracks_to_delete.split(",")]
            break
        except (ValueError, IndexError):
            print("Invalid track number(s). Please enter valid numbers separated by commas.")

    confirm = input(f"Are you sure you want to delete {len(track_ids_to_delete)} tracks from {selected_playlist['name']}? (y/n) ")

    if confirm.lower() == 'y':
        sp.playlist_remove_all_occurrences_of_items(playlist_id=selected_playlist['id'], items=track_ids_to_delete)
        print(f"Successfully deleted {len(track_ids_to_delete)} tracks from {selected_playlist['name']}!")
    else:
        print("No tracks were deleted.")