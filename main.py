import spotipy
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(".env")

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
USER_ID = os.environ.get("USER_ID")
REDIRECT_URL = os.enivorn.get("REDIRECT_URL")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET,
                              redirect_uri=REDIRECT_URL,
                              scope="playlist-modify-private"))

date = input("Which year do you want to travel to? "
             "Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")

artist_songs = soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")
songs = [song.getText().strip() for song in artist_songs]
song_list = []

print("Generating Playlist...")
for song in songs:
    query_string = f"track: {song} year: {year}"
    query = sp.search(q=query_string, type="track")
    try:
        uri = f"{query['tracks']['items'][0]['uri']}"
        song_list.append(uri)
    except IndexError:
        print(f"{song} could not be found. Skipped.")


playlist = sp.user_playlist_create(user=USER_ID, name=f"{date} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_list)
