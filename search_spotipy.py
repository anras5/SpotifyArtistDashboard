import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dotenv import load_dotenv
import os
import pandas

load_dotenv()

sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                                        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')))


def get_artist_info(name: str) -> dict:
    search_result = sp.search(name, type='artist')['artists']['items'][0]
    return {'name': search_result['name'],
            'genres': search_result['genres'],
            'id': search_result['id'],
            'image': search_result['images'][0]['url'],
            'popularity': search_result['popularity'],
            'followers': search_result['followers']['total'],
            'type': search_result['type']}


def get_artist_albums(artist_id: str) -> pd.DataFrame:
    search_result = sp.artist_albums(artist_id)['items']
    albums = pd.DataFrame(columns=['name', 'id', 'release_date', 'total_tracks', 'image'])
    for album in search_result:
        albums = pd.concat([albums, pd.DataFrame([{'name': album['name'],
                                                   'id': album['id'],
                                                   'release_date': album['release_date'],
                                                   'total_tracks': album['total_tracks'],
                                                   'image': album['images'][0]['url'],
                                                   # 'markets': album['available_markets']
                                                   }])])
    albums.drop_duplicates(subset=['name'], inplace=True)
    return albums


def get_album_tracks(album_id: str) -> pd.DataFrame:
    search_result = sp.album_tracks(album_id)['items']
    songs = pd.DataFrame(columns=['name', 'id', 'duration_ms',
                                  'danceability', 'energy', 'loudness',
                                  'speechiness', 'acousticness', 'instrumentalness',
                                  'liveness', 'tempo'])
    for song in search_result:
        song_features = sp.audio_features(song['id'])[0]
        songs = pd.concat([songs, pd.DataFrame([{'name': song['name'],
                                                 'id': song['id'],
                                                 'disc_number': song['disc_number'],
                                                 'duration_s': round(song['duration_ms']/1000, 0),
                                                 'danceability': song_features['danceability'],
                                                 'energy': song_features['energy'],
                                                 'loudness': song_features['loudness'],
                                                 'speechiness': song_features['speechiness'],
                                                 'acousticness': song_features['acousticness'],
                                                 'instrumentalness': song_features['instrumentalness'],
                                                 'liveness': song_features['liveness'],
                                                 'tempo': song_features['tempo']
                                                 }])])
    return songs


if __name__ == '__main__':
    print(get_artist_albums('https://open.spotify.com/artist/3fMbdgg4jU18AjLCKBhRSm?si=29NwyusVTwuF7qwxWQDf6w'))
