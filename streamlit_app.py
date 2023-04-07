from operator import index
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pickle

def create_playlist(p_name,name,model,data,token,username='11143699684'):

    # Connecting to API
    spotifyObject = spotipy.Spotify(auth=token)

    # Create empty playlist
    spotifyObject.user_playlist_create(user=username,name=p_name)
    # Get id of playlist
    pl = spotifyObject.user_playlists(user=username)
    playlist = pl['items'][0]['id']
    
    results = spotifyObject.audio_features(spotifyObject.search(name)['tracks']['items'][0]['uri'])[0]
    resdata = pd.DataFrame(results,index=[0])
    resdata = resdata.drop(['id','uri','type','key','mode','track_href','analysis_url','time_signature'],axis=1)
    
    cluster = model.predict(resdata)[0]
    plist = data[data['cluster_label']==cluster]
    plist = plist.sort_values('song_popularity',ascending=False).iloc[:50].reset_index(drop=True)
    
    # Get track id of songs
    list_of_tracks = [('spotify:track:'+t) for t in plist['track_id']]
    # Add tracks to empty playlist
    spotifyObject.user_playlist_add_tracks(user=username,playlist_id = playlist,tracks=list_of_tracks)
    return spotifyObject.user_playlists(user=username)['items'][0]['external_urls']['spotify']
    
def create_similar_songs_pl(token,cluster,data,username='11143699684'):
    
    spotifyObject = spotipy.Spotify(auth=token)
    
    # Create empty playlist
    spotifyObject.user_playlist_create(user=username,name=f"Cluster-{cluster}")
    # Get id of playlist
    pl = spotifyObject.user_playlists(user=username)
    # Get id of latest playlist
    playlist = pl['items'][0]['id']
    
    
    plist = data[data['cluster_label']==cluster]
    plist = plist.sort_values('song_popularity',ascending=False).iloc[:50].reset_index(drop=True)
  
    list_of_tracks = [('spotify:track:'+t) for t in plist['track_id']]
    # Add tracks to empty playlist
    spotifyObject.user_playlist_add_tracks(user=username,playlist_id = playlist,tracks=list_of_tracks)
    return spotifyObject.user_playlists(user=username)['items'][0]['external_urls']['spotify']
  
def will_song_be_hit(datas,
                     classification_model,
                     clustering_model,
                     label_encoder,
                     cluster_data,
                     token,
                     username='11143699684'):

    
    # Cols for predict data
    

    # The data types have been changed as it must be the same as the training set   
    datas['genres'] = label_encoder.transform(datas['genres'])
    datas[['genres','mode','key','time_signature']] = datas[['genres','mode','key','time_signature']].astype('category')
    datas.iloc[:,4:] = datas.iloc[:,4:].astype(float)
    try:
        result = classification_model.predict_proba(datas)[0][1]
    except:
        print('please enter sensible values.')
  
    cluster = clustering_model.predict(datas.iloc[:,4:])[0]
    link = create_similar_songs_pl(token=token,cluster=cluster,data=cluster_data,username=username)

    return result,link

c_df = pd.read_csv('c_data.csv',index_col=[0])
token = 'YOUR_TOKEN'
clustering_model = pickle.load(open('clustering_model.sav','rb'))
classification_model = pickle.load(open('lgbm_model.sav','rb'))
le = pickle.load(open('le.sav','rb'))

st.title('Prediction and Recommendations')
st.write('You can create a song from the left sidebar and check its popularity. '
         '\n You can create a similar playlist by entering the song and singer name below.')



p_name = st.text_input('Playlist Name')
title = st.text_input('Song')
artist = st.text_input('Artist')


button = st.button('Create Playlist')


if button:
    link = create_playlist(p_name=p_name,name=(title + ' '+ artist) ,model=clustering_model,data=c_df,token=token)
    components.iframe(link.replace('.com','.com/embed'), width=700, height=300)


def user_input_features():
    genre = st.sidebar.text_input('Genre')
    mode = st.sidebar.selectbox('Mode',[0,1])
    key = st.sidebar.selectbox('Key',[0,1,2,3,4,5,6,7,8,9,10,11])
    time_signature = st.sidebar.selectbox('Time Signature',[3,4,5,6,7])
    danceability = st.sidebar.slider('Danceability', 0.000000, 0.980000, 0.000000, 0.01)
    energy = st.sidebar.slider('Energy', 0.000281, 0.999000, 0.000281, 0.01)
    acousticness = st.sidebar.slider('Acousticness', 0.000002, 0.996000, 0.000002, 0.01)
    instrumentalness = st.sidebar.slider('Instrumentalness', 0.000000, 0.984000, 0.000000, 0.01)
    liveness = st.sidebar.slider('Liveness', 0.020600, 0.993000, 0.020600, 0.01)
    loudness = st.sidebar.slider('Loudness', -37.114000, -1.987000, -37.114000, 0.1)
    speechiness = st.sidebar.slider('Speechiness', 0.000000, 0.947000, 0.000000, 0.01)
    tempo = st.sidebar.slider('Tempo', 0.000000, 210.029000, 0.000000, 1.0)
    valence = st.sidebar.slider('Valence', 0.000000, 0.996000, 0.000000, 0.01)
    duration_ms = st.sidebar.slider('Duration (ms)',0,500000,200000,1)

    user_data = {'genres':genre,
    'mode':mode,
    'key':key,
    'time_signature':time_signature,
                'danceability': danceability,
                'energy': energy,
                'loudness': loudness,
                'speechiness': speechiness,
                'acousticness': acousticness,
                'instrumentalness': instrumentalness,
                'liveness': liveness,
                'valence': valence,
                'tempo': tempo,
                'duration_ms':duration_ms
                }

    features = pd.DataFrame(user_data, index=[0])
    return features

df_user = user_input_features()
button1 = st.sidebar.button('Predict Popularity')

if button1:
    r,l = will_song_be_hit(df_user,classification_model=classification_model,
    clustering_model=clustering_model,label_encoder=le,cluster_data=c_df,token=token)
    if r < 0.5:
        st.markdown(f"Predicted Popularity : {r} \n Your song may not be hit.")
    else: 
        st.markdown(f"Predicted Popularity : {r} \n Your song may be hit.")
    st.markdown('A playlist with songs similar to your song was created:')
    components.iframe(l.replace('.com','.com/embed'), width=700, height=300)
