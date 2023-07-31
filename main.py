from SetlistAPI import get_most_played_songs
from Spoti import create_spotify_playlist

def ask_MBID():
    if __name__ == '__main__':
        artist_id = input("Enter the MBID of the artist: ")
        most_played_songs = get_most_played_songs(artist_id)
        if most_played_songs:
            print("Most played songs:")
            for song, count in most_played_songs:
                print(f"{song}: {count} times")
        else:
            print("No setlist data found for this artist.")
ask_MBID()

input("Press any key to exit...")