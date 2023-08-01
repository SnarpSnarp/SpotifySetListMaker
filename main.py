from SetlistAPI import get_most_played_songs
from Spoti import create_spotify_playlist

def ask_MBID():
    artist_name = input('Artist Name: ')
    artist_id = input('Artist MBID Number: ')
    most_played_songs = get_most_played_songs(artist_id)
    if most_played_songs:
        print("Most played songs:")
        for song, count in most_played_songs:
            print(f"{song}: {count} times")
        createplaylistquest = input('Create playlist? y/n ')
        if createplaylistquest.lower() == 'y':
            create_spotify_playlist(most_played_songs, artist_name)
    else:
        print("No setlist data found for this artist.")

if __name__ == '__main__':
    ask_MBID()
