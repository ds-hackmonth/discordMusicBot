import os
import sys
import spotipy
import spotipy.oauth2 as oauth2
import re

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

def extract_playlist_id(playlist_url):
    # If the user passes in an html link
    if playlist_url.startswith("https") or playlist_url.startswith("open.spotify"):
        playlist_id = re.search("playlist\/(.*)\?", playlist_url).group(1)
        return playlist_id

    # The user passes in a spotify URI  
    if playlist_url.startswith("spotify:playlist"):
        playlist_id = re.search("playlist:(.*)", playlist_url).group(1)
        return playlist_id
    
    # Else, the playlist_url is invalid
    return None

def get_songs_from_album(playlist_url):
    """ Given an ALBUM_URL, this function will query the spotify API (via the spotipy library) 
    and return a list of all the songs present in that album"""
    
    # First, we must tell the spotify API who we are
    token = get_token()
    spotify = spotipy.Spotify(auth=token)
    playlist_id = extract_playlist_id(playlist_url)

    # Return None if the playlist_url was invalid
    if playlist_id is None:
        return None

    playlist = spotify.playlist(playlist_id)
    tracks = playlist["tracks"]
    song_artist_lst = list()

    for item in tracks["items"]:
        song_name = item["track"]["name"]
        artist_name = item["track"]["artists"][0]["name"]
        song_artist_lst.append((song_name, artist_name))

    print(song_artist_lst)
    return song_artist_lst

get_songs_from_album("https://open.spotify.com/playlist/0Ud0ulpKwlMDnDyYGKlJlh?si=cSc_RZUwS-Sunw6gKgNjRg")




