import pandas as pd
import numpy as np
import pickle
import streamlit as st

@st.cache_resource
def importall():
    df = pickle.load(open('pickle/df.pkl','rb'))
    X_scaled = pickle.load(open('pickle/X_scaled.pkl','rb'))
    knn = pickle.load(open('pickle/knn.pkl','rb'))
    return df,X_scaled,knn
df,X_scaled,knn=importall()

# lookup track by track_name
def get_song_index(song_name):
    return df[df["artist_track_name"] == song_name].index[0]

# get la neighbors for that song
def get_neighbors(song_name):
    index = get_song_index(song_name)
    song_vector = X_scaled[index].reshape(1,-1)
    distances, indices = knn.kneighbors(song_vector)

    return distances[0], indices[0]
def genre_bonus(index, song_A, song_B):
    genre_A = df[df["artist_track_name"] == song_A]["genre"].values[0]
    genre_B = df[df["artist_track_name"] == song_B]["genre"].values[0]

    genre_C = df.iloc[index]["genre"]

    bonus = 0

    if genre_C == genre_A:
        bonus += 0.1
    if genre_C == genre_B:
        bonus += 0.1

    return bonus

def bridge_recommendation(song_A, song_B, top_n=5): 
    dist_A, ind_A = get_neighbors(song_A) # the distance and the independent variables chosen
    dist_B, ind_B = get_neighbors(song_B)

    scores = {}

    # convert those distances into similarity
    for d, i in zip(dist_A, ind_A):
        # scores[i] = scores.get(i, 0) + (1 / (1 + d)) # without the added weight of genre(OneHotEncoding)
        scores[i] = scores.get(i, 0) + (1 / (1 + d)) + genre_bonus(i, song_A, song_B)

    for d, i in zip(dist_B, ind_B):
        # scores[i] = scores.get(i, 0) + (1 / (1 + d))
        scores[i] = scores.get(i, 0) + (1 / (1 + d)) + genre_bonus(i, song_A, song_B)

    # sort by combined score
    sorted_songs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    results = []
    for i, score in sorted_songs:
        name= df.iloc[i]["artist_track_name"]

        if name not in [song_A, song_B]:
            results.append((name, score))

    return results[:top_n]

def normalize_scores(results):
    if not results:
        return []
    
    max_score = max(score for _, score in results)

    output = []
    for name, score in results:
        confidence = score / max_score
        output.append((name, score, confidence))

    return output