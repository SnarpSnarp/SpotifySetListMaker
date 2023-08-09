import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Key import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_USERNAME

def delete_whole_playlist():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='playlist-modify-public,playlist-modify-private,playlist-read-private'))
    
    playlists = sp.current_user_playlists()['items']

    # Show the user's playlists
    for idx, playlist in enumerate(playlists):
        print(f"{idx + 1}. {playlist['name']} ({playlist['tracks']['total']} tracks)")

    # User selects a playlist
    while True:
        try:
            selected_playlist_idx = int(input("Enter the number of the playlist you want to delete (or 0 to exit): ")) - 1
            if selected_playlist_idx == -1:
                return
            selected_playlist = playlists[selected_playlist_idx]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please choose a valid playlist number.")

    # Confirm deletion
    confirmation = input(f"Are you sure you want to delete the playlist '{selected_playlist['name']}'? Type the name of the playlist or 'CONFIRM' to proceed, or anything else to cancel: ")

    if confirmation == selected_playlist['name'] or confirmation.upper() == 'CONFIRM':
        sp.user_playlist_unfollow(user=sp.me()['id'], playlist_id=selected_playlist['id'])
        print(f"Successfully deleted the playlist '{selected_playlist['name']}'")
    else:
        print("Playlist deletion cancelled.")
