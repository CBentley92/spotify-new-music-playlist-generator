import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

import requests
from bs4 import BeautifulSoup
import json


# Spotify credentials and scope
SPOTIPY_CLIENT_ID = os.getenv("CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("REDIRECT_URI")

scope = "playlist-modify-private"

def create_metal_album_list(start_date:str, end_date:str, minimum_rating:int, output_dir:str = ''):
    """
    Fetches album reviews from metal-temple.com based on input criteria and saves them to a JSON file.

    Parameters
    ----------
    start_date : str
        Start date for album reviews in format 'YYYY-MM-DD'
    end_date : str
        End date for album reviews in format 'YYYY-MM-DD'
    minimum_rating : int
        Minimum rating for album reviews to be included (1-10)
    output_dir : str, optional
        Directory to save JSON file to, by default ''
    """

    page = 1
    url = f"https://metal-temple.com/reviews/?_rating={str(minimum_rating)}%2C10&_review_date={start_date}%2C{end_date}&_pagination={page}"
    response = requests.get(url)

    if response.status_code != 200:
        return print("Error: Unable to fetch data from website, check date format")
    
    web_list = []

    while response.status_code == 200:
        
        soup = BeautifulSoup(response.content, 'html.parser')

        reviews = soup.find_all('div', class_="ct-div-block review-item__title")

        if len(reviews) == 0:
            if page == 1:
                return print("Error: No reviews found for the given criteria")
            break

        for review in reviews:
            web_list.append(
                {
                    'artist': review.find_all('h6')[1].find('span').get_text(strip=True),
                    'album': review.find_all('h6')[0].find('span').get_text(strip=True),
                    'review': review.find('div', class_='review-item__title__reveal').find('span').get_text(strip=True),
                }
            )
        
        page += 1
        url = f"https://metal-temple.com/reviews/?_rating={str(minimum_rating)}%2C10&_review_date={start_date}%2C{end_date}&_pagination={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error: Could not access page {page}")
    
    file_name = os.path.join(output_dir, f"albumlist_metal-temple_{start_date}_{end_date}.json")

    with open(file_name, 'w') as json_file:
        json.dump(web_list, json_file, indent=4) 

    return print(f"Saved to {file_name}")


def confirm_artist(artist_list, artist):
    return artist in [artist_item['name'] for artist_item in artist_list]


def create_playlist(album_list_file:str, songs_per_album:int=2, randomise_order:bool=False, custom_name:str=None):
    # Authenticate with Spotify
    """
    Creates a Spotify playlist based on a list of albums in a JSON file

    Parameters
    ----------
    album_list_file : str
        Path to the JSON file containing the album list
    songs_per_album : int, optional
        Number of songs to include for each album, by default 2
    randomise_order : bool, optional
        Whether to randomise the order of the tracks in the playlist, by default False

    Returns
    -------
    None
    """
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET,
                redirect_uri=SPOTIPY_REDIRECT_URI,
                scope=scope
            ),
            requests_timeout=30,
        )
    except:
        return print("Error: Unable to authenticate with Spotify")

    df = pd.read_json(album_list_file)

    track_list = []
    for _, row in df.iterrows():
        query = f"artist:{row['artist']} album:{row['album']}"
        results = sp.search(q=query, type='track')
        df_results = pd.json_normalize(results['tracks']['items'])
        try:
            df_results['correct_artist'] = df_results['artists'].apply(lambda x: confirm_artist(x, row['artist']))
        except:
            continue
        df_results = df_results.loc[
            (df_results['album.name'] == row['album'])
            & (df_results['correct_artist'] == True)
        ]
        df_results = df_results.sort_values(by='popularity', ascending=False)[:songs_per_album]
        track_list = track_list + df_results['id'].to_list()

    # Create a new playlist
    user_id = sp.me()['id']
    if not custom_name == None:
        playlist_name = custom_name
    else:
        playlist_name = f"{album_list_file[:-5].split('_')[-3]} playlist for {album_list_file[:-5].split('_')[-2]} - {album_list_file[:-5].split('_')[-1]}"
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)

    # Add tracks to the playlist
    if len(track_list) > 0:
        if randomise_order:
            tracks_to_add = track_list.sample(frac=1).tolist()
        else:
            tracks_to_add = track_list
        for i in range(0, len(tracks_to_add), 100):
            sp.playlist_add_items(playlist_id=playlist['id'], items=tracks_to_add[i:i+100])

        return print(f"Playlist '{playlist['name']}' created with {len(tracks_to_add)} songs!")
    else:
        return print("No tracks to add to playlist!")