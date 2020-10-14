import os
import sys
import spotipy
import spotipy.oauth2 as oauth2

CLI_ID = "c031db81e9e841c382309dac036c36ae"
CLI_KEY = os.environ.get("spotifyDiscordBotSecret")
if CLI_KEY is None:
    print("You have not added the spotify Client secret as an environment variable. Exiting.")
    sys.exit()

def get_token():
    """ Returns an access token that is to be sent to the spotify Web API upon every request."""
    credentials = oauth2.SpotifyClientCredentials(
        client_id = CLI_ID, 
        client_secret = CLI_KEY)
    token = credentials.get_access_token()
    return token 

def get_songs_from_album(playlist_url):
    """ Given an ALBUM_URL, this function will query the spotify API (via the spotipy library) 
    and return a list of all the songs present in that album"""
    
    # First, we must tell the spotify API who we are
    token = get_token()
    spotify = spotipy.Spotify(auth=token)
    playlist = spotify.playlist("2HcHxIscwRkffP1ITeGsLN")
    tracks = playlist["tracks"]
    song_artist_lst = list()
    for item in tracks["items"]:
        song_name = item["track"]["name"]
        artist_name = item["track"]["artists"][0]["name"]
        song_artist_lst.append((song_name, artist_name))
    print(song_artist_lst)
    return song_artist_lst

get_songs_from_album("")




