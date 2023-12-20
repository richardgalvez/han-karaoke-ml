from flask import Flask, render_template, request, redirect
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from collections import defaultdict

def preprocess_data(df):
    # Drop unnecessary columns.
    dfd = df.drop(['track_id', 'artist_id', 'album_id', 'duration', 'release_date', 'mode', 'playlist_id', 'playlist_name'], axis=1)
    # Exclude non-numeric columns.
    numeric_cols = dfd.select_dtypes(include=['float64', 'int64']).columns
    dfd = dfd[numeric_cols]
    # Implement standard scaler for data.
    scaler = MinMaxScaler()
    model = scaler.fit(dfd)
    scaled_data = model.transform(dfd)

    return scaled_data

def apply_kmeans(scaled_data, num_clusters=15):
    # Use KMeans (descriptive, unsupervised method) with the same seed as Jupyter Notebook for consistency.
    kmeans = KMeans(n_clusters=num_clusters, random_state=75)
    kfit = kmeans.fit(scaled_data)
    # Predicting the clusters.
    predictions = kfit.labels_
    data_scaled = pd.DataFrame(scaled_data, columns=['popularity', 'danceability', 'energy', 'key', 'loudness',
                                                     'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                                                     'valence', 'tempo'])
    data_scaled['clusters'] = predictions

    return data_scaled

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

# Define a dictionary to store user song selections and their rates.
user_selections = defaultdict(int)

@app.route('/')
def home():
    # Calculate the overall percentages.
    overall_counts = defaultdict(int)
    total_selections = sum(user_selections.values())

    for song, count in user_selections.items():
        cluster = clusters[clusters['track_name'] == song]['clusters'].iloc[0]
        overall_counts[cluster] += count

    overall_percentages = {cluster: (count / total_selections) * 100 if total_selections > 0 else 0 for cluster, count in overall_counts.items()}

    # Sort the overall_percentages dictionary by percentage in descending order so it can be seen upon loading.
    sorted_cluster_percentages = {cluster: percentage for cluster, percentage in sorted(overall_percentages.items(), key=lambda item: item[1], reverse=True)}

    return render_template('index.html', selected_song=None, selected_song_artist=None, user_selections=user_selections, cluster_percentages=sorted_cluster_percentages, clusters=clusters)


@app.route('/select_song', methods=['POST'])
def select_song():
    selected_song = request.form['selected_song']
    selected_song_artist = clusters[clusters['track_name'] == selected_song]['artist_name'].iloc[0]

    user_selections[selected_song] += 1

    # Calculate the percentage rate for each cluster based on the number of songs chosen in each cluster.
    cluster_counts = defaultdict(int)
    total_selections = sum(user_selections.values())

    for song, count in user_selections.items():
        cluster = clusters[clusters['track_name'] == song]['clusters'].iloc[0]
        cluster_counts[cluster] += count

    cluster_percentages = {cluster: (count / total_selections) * 100 for cluster, count in cluster_counts.items()}

    # Sort the cluster_percentages dictionary by percentage within each cluster in descending order.
    sorted_cluster_percentages = {cluster: percentage for cluster, percentage in sorted(cluster_percentages.items(), key=lambda item: item[1], reverse=True)}

    return render_template('index.html', songs=clusters['track_name'].tolist(), selected_song=selected_song, selected_song_artist=selected_song_artist, user_selections=user_selections, cluster_percentages=sorted_cluster_percentages, clusters=clusters)

@app.route('/refresh')
def refresh_songs():
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
