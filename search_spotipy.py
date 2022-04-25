from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from dotenv import load_dotenv
import os

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


def get_artist_albums(artist_id: str) -> dict:
    search_result = sp.artist_albums(artist_id)['items']
    info = []
    for album in search_result:
        info.append({'name': album['name'],
                     'id': album['id'],
                     'release_date': album['release_date'],
                     'total_tracks': album['total_tracks'],
                     'image': album['images'][0]['url'],
                     # 'markets': album['available_markets']
                     })
    return info


def get_album_tracks(album_id: str) -> dict:
    search_result = sp.album_tracks(album_id)['items']
    info = []
    for song in search_result:
        song_features = sp.audio_features(song['id'])[0]
        info.append({'name': song['name'],
                     'id': song['id'],
                     'disc_number': song['disc_number'],
                     'duration_ms': song['duration_ms'],
                     'danceability': song_features['danceability'],
                     'energy': song_features['energy'],
                     'loudness': song_features['loudness'],
                     'speechiness': song_features['speechiness'],
                     'acousticness': song_features['acouticness'],
                     'instrumentalness': song_features['instrumentalness'],
                     'liveness': song_features['liveness'],
                     'tempo': song_features['tempo']
                     })


if __name__ == '__main__':
    search = sp.audio_features('spotify:track:2gVhfX2Gy1T9kDuS9azrF7')
    print(search)
