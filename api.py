import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #ここ以降にいろいろ追加
import pandas as pd


my_id = 'API Client ID'
my_secret = 'API Client secret'


ccm = SpotifyClientCredentials(client_id = my_id, client_secret = my_secret)
sp = spotipy.Spotify(client_credentials_manager = ccm)



# プレイリストから曲を取得
def get_to_playlist(playlist_id):
    playlist = sp.playlist(playlist_id)
    # print(playlist)
    # exit
    track_ids = []
    for item in playlist['tracks']['items']:
        track = item['track']
        if not track['id'] in track_ids:
            track_ids.append(track['id'])
        else:
            for item in playlist['tracks']['items']:
                track = item['track']
                if not track['id'] in track_ids:
                    track_ids.append(track['id'])
    return track_ids


# アルバムから曲を取得
def get_to_album_tracks(playlist_id):
    
    playlist = sp.album_tracks(playlist_id)
    # print(playlist)
    # exit
    track_ids = []
    
    # print(playlist)
    for item in playlist['items']:
        # track = item['track']
        track = item
        if not track['id'] in track_ids:
            track_ids.append(track['id'])
        else:
            for item in playlist['items']:
            # for item in playlist['tracks']['items']:
                # track = item['track']
                track = item
                if not track['id'] in track_ids:
                    track_ids.append(track['id'])
    return track_ids

def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)

    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    length = meta['duration_ms']
    popularity = meta['popularity']
    key = features[0]['key']
    mode = features[0]['mode']
    danceability = features[0]['danceability']
    acousticness = features[0]['acousticness']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    valence = features[0]['valence']

    track = [name, album, artist, length,  key, popularity,danceability, acousticness,
             energy, instrumentalness, liveness, tempo, valence]
    return track


def id_to_csv(track_ids):
    tracks = []
    for track_id in track_ids:
        track = getTrackFeatures(track_id)
        tracks.append(track)

    df = pd.DataFrame(tracks, columns=['name', 'album', 'artist', 'length',  'key(キー)','popularity(相対的人気度)', 'danceability(ダンスに適しているか)',
                      'acousticness(アコースティック感)', 'energy(エネルギッシュか)', 'instrumentalness(インスト感（歌声がない割合))', 'liveness(ライブ感（聴衆がいるか）)', 'tempo(テンポ)', 'valence(曲の陽性度)'])
    df.head()

    df.to_csv('myalbum.csv', encoding='utf-8', index=False)
    print("CSVファイルが作成されました。")

    return df

if __name__ == '__main__':
    # ids = get_to_playlist("プレイリストID") #プレイリストから整形したい場合こっち使用
    ids = get_to_album_tracks("アルバムID") 
    id_to_csv(ids)
