from flask import Flask, render_template
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

    # Use Principal Component Analysis (PCA) to gather results
def apply_pca(data_scaled):
    pca = PCA(n_components=2)
    pca_data = pd.DataFrame(pca.fit_transform(data_scaled.drop(['clusters'], axis=1)), columns=['PC1', 'PC2'])
    pca_data['clusters'] = data_scaled['clusters']

    return pca_data

# Flask application instance
app = Flask(__name__)

@app.route("/")
def index():
    # Load karaoke song data.
    df = pd.read_csv('karaoke_playlist_tracks_data.csv')

    # Preprocess data.
    scaled_data = preprocess_data(df)

    # Apply KMeans.
    data_scaled = apply_kmeans(scaled_data)

    # Apply PCA.
    pca_data = apply_pca(data_scaled)

    # Merge the original DataFrame with the clustered data
    clustered_df = pd.merge(df[['track_name', 'artist_name']], data_scaled[['clusters']], left_index=True, right_index=True)

    return render_template('index.html', clusters=clustered_df)

@app.route("/song-select")
def song_select():
    return f"Hello, world!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)