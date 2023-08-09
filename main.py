from SetlistAPI import get_most_played_songs
from CreateSpoti import create_spotify_playlist
from DeleteTracksSpoti import delete_tracks_from_playlist
from DeletePlaylistSpoti import delete_whole_playlist

def AskFunction():
    while True:  # Keep the menu running until user decides to exit
        print('Please Choose a function:')
        print('1). Create Set List Playlist')
        print('2). Delete Tracks from a playlist')
        print('3). Delete Entire Playlist')
        print('0). Exit')
        try:
            FuncSelect = int(input('Choice: '))  # We expect an integer input
        except ValueError:
            print("Invalid choice. Please enter a number from the options.")
            continue

        if FuncSelect == 1:
            AskMBID()
        elif FuncSelect == 2:
            delete_tracks_from_playlist()
        elif FuncSelect == 3:
            delete_whole_playlist()
        elif FuncSelect == 0:
            break  # Exit the loop and program
        else:
            print("Invalid choice. Please select a valid option.")

def AskMBID():
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
    AskFunction()
    input("Press Enter to exit...")