import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Key import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_USERNAME

def delete_whole_playlist():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope='playlist-modify-public,playlist-modify-private,playlist-read-private'))
    playlists = sp.current_user_playlists()['items']

    # Show the user's playlists
    for idx, playlist in enumerate(playlists):
        print(f"{idx + 1}. {playlist['name']} ({playlist['tracks']['total']} tracks)")

    # User selects playlists
    selected_playlist_indices = input("Enter the numbers of the playlists you want to delete, separated by commas (or 0 to exit): ")

    selected_playlist_indices = selected_playlist_indices.split(',')
    selected_playlists = []

    try:
        for idx in selected_playlist_indices:
            index = int(idx.strip()) - 1
            if index == -1:
                return
            selected_playlists.append(playlists[index])
    except (ValueError, IndexError):
        print("Invalid selection. Please choose valid playlist numbers.")
        return

    # Confirm deletions
    for selected_playlist in selected_playlists:
        confirmation = input(f"Are you sure you want to delete the playlist '{selected_playlist['name']}'? Type the name of the playlist or 'CONFIRM' to proceed, or anything else to cancel: ")

        if confirmation == selected_playlist['name'] or confirmation.upper() == 'CONFIRM':
            sp.user_playlist_unfollow(user=sp.me()['id'], playlist_id=selected_playlist['id'])
            print(f"Successfully deleted the playlist '{selected_playlist['name']}'")
        else:
            print(f"Playlist '{selected_playlist['name']}' deletion cancelled.")
