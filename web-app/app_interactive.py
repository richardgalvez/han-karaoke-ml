from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import random
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def preprocess_data(df):
    # Drop unnecessary columns.
    dfd = df.drop(['track_id', 'artist_id', 'album_id', 'duration', 'release_date', 'mode', 'playlist_id', 'playlist_name'], axis=1)
     # Exclude non-numeric columns
    numeric_cols = dfd.select_dtypes(include=['float64', 'int64']).columns
    dfd = dfd[numeric_cols]
    # Implement standard scaler for data.
    scaler = MinMaxScaler()
    model = scaler.fit(dfd)
    scaled_data = model.transform(dfd)

    return scaled_data

def apply_kmeans(scaled_data, num_clusters=15):
    # Use KMeans (non-descriptive method) with same seed as Jupyter notebook for consistency.
    kmeans = KMeans(n_clusters=num_clusters, random_state=75)
    kfit = kmeans.fit(scaled_data)
    # Predicting the clusters.
    predictions = kfit.labels_
    data_scaled = pd.DataFrame(scaled_data, columns=['popularity', 'danceability', 'energy', 'key', 'loudness',
                                                     'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                                                     'valence', 'tempo'])
    data_scaled['clusters'] = predictions

    return data_scaled

    # Use Principal Component Analysis (PCA) to gather results.
def apply_pca(data_scaled):
    pca = PCA(n_components=2)
    pca_data = pd.DataFrame(pca.fit_transform(data_scaled.drop(['clusters'], axis=1)), columns=['PC1', 'PC2'])
    pca_data['clusters'] = data_scaled['clusters']

    return pca_data

app = Flask(__name__)

# Load karaoke song data.
df = pd.read_csv('karaoke_playlist_tracks_data.csv')

# Preprocess data.
scaled_data = preprocess_data(df)

# Apply KMeans.
data_scaled = apply_kmeans(scaled_data)

# Apply PCA.
pca_data = apply_pca(data_scaled)

# Merge the original DataFrame with the clustered data.
clusters = pd.merge(df[['track_name', 'artist_name']], data_scaled[['clusters']], left_index=True, right_index=True)

@app.route("/", methods=['GET', 'POST'])
def index():
    selected_song = None

    if request.method == 'POST':
        cluster_id = int(request.form.get('cluster_id'))
        selected_song_index = int(request.form.get('selected_song_index'))

        # Retrieve the selected song.
        selected_song = clusters[clusters['clusters'] == cluster_id].iloc[selected_song_index]

        # Pass the selected song information to the /song route directly.
        return render_template('song.html', selected_song_title=selected_song['track_name'].values[0], selected_song_artist=selected_song['artist_name'].values[0])

    return render_template('index.html', clusters=clusters, selected_song=selected_song)


@app.route("/song", methods=['GET', 'POST'])
def song():
    # Retrieve form inputs
    cluster_id_str = request.form.get('cluster_id')
    selected_song_index_str = request.form.get('selected_song_index')

    # Check if cluster_id and selected_song_index are not empty
    if cluster_id_str and selected_song_index_str:
        # Convert to integers
            cluster_id = int(cluster_id_str)
            selected_song_index = int(selected_song_index_str)

            # Retrieve the selected song.
            selected_song_title = request.form.get('selected_song_title')
            selected_song_artist = request.form.get('selected_song_artist')

            # Retrieve the next 3 similar songs from the same cluster.
            next_songs = clusters[clusters['clusters'] == cluster_id].sample(3)

            return render_template('song.html', selected_song_title=selected_song_title, selected_song_artist=selected_song_artist, next_songs=next_songs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
