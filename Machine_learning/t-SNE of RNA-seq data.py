import pandas as pd
import os
import gzip
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.stats import ttest_ind
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns
from sklearn.manifold import TSNE
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster
from sklearn.metrics import silhouette_score

# Hyperparameter constants
DATA_DIR = "GSE99531_RAW"
PCA_COMPONENTS = 2
KMEANS_NUM_CLUSTERS = 3
KMEANS_RANDOM_STATE = 0
TSNE_PERPLEXITY = 200
TSNE_N_ITER = 1000
TSNE_RANDOM_STATE = 42
TSNE_LEARNING_RATE = 1000
DBSCAN_EPS = 0.5
DBSCAN_MIN_SAMPLES = 10
HIERARCHICAL_METHOD = 'ward'
SILHOUETTE_RANGE_START = 2
SILHOUETTE_RANGE_END = 10

def load_and_preprocess(file_path):
    """
    Load and preprocess the data from a .txt.gz file.

    Parameters:
    file_path (str): The path to the .txt.gz file to be loaded.

    Returns:
    DataFrame: A pandas DataFrame containing the loaded data.
    """
    with gzip.open(file_path, 'rt') as file:
        data = pd.read_csv(file, sep='\t')
    return data

def normalize_data(data):
    """
    Normalize the data using log-transformation.

    Parameters:
    data (DataFrame): The pandas DataFrame containing the 'RawCounts' column.

    Returns:
    DataFrame: The input DataFrame with an additional column 'NormalizedExpression'
               containing the log2 transformed 'RawCounts'.
    """
    data['NormalizedExpression'] = np.log2(data['RawCounts'] + 1)
    return data

def perform_tsne(data, perplexity=TSNE_PERPLEXITY, n_iter=TSNE_N_ITER, random_state=TSNE_RANDOM_STATE, learning_rate=TSNE_LEARNING_RATE):
    """
    Perform t-SNE dimensionality reduction on the given data.

    Parameters:
    data (array-like): The high-dimensional data to be reduced.
    perplexity (float): The perplexity parameter for the t-SNE algorithm.
    n_iter (int): The number of iterations for optimization.
    random_state (int): The seed for the random number generator.
    learning_rate (float): The learning rate for t-SNE.

    Returns:
    array: The transformed data in two dimensions.
    """
    tsne = TSNE(n_components=2, learning_rate=learning_rate, perplexity=perplexity, n_iter=n_iter, random_state=random_state)
    tsne_results = tsne.fit_transform(data)  # Use the entire dataset
    return tsne_results

def perform_hierarchical_clustering(data):
    """
    Perform hierarchical clustering on the given data.

    Parameters:
    data (array-like): The data to cluster.

    Returns:
    ndarray: The hierarchical clustering encoded as a linkage matrix.
    """
    Z = linkage(data, HIERARCHICAL_METHOD)
    return Z

def main():
    # Load all data files
    datasets = []
    gene_sets = []
    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith(".txt.gz"):
            file_path = os.path.join(DATA_DIR, file_name)
            dataset = load_and_preprocess(file_path)
            normalized_dataset = normalize_data(dataset)
            datasets.append(normalized_dataset)
            gene_sets.append(set(dataset['ID']))  # Collect gene IDs

    # # Find common genes across all datasets
    common_genes = set.intersection(*gene_sets)

    # Filter each dataset to include only common genes
    filtered_datasets = []
    for dataset in datasets:
        filtered_datasets.append(dataset[dataset['ID'].isin(common_genes)])

    ID_indexed_datasets = [dataset.set_index('ID')['NormalizedExpression'] for dataset in filtered_datasets]
    transposed_datasets = [dataset.transpose() for dataset in ID_indexed_datasets]

    # Combine reshaped datasets
    combined_data = pd.concat(transposed_datasets, axis=1)

    # Handle missing values
    combined_data = combined_data.fillna(0)

    # Standardize the data
    scaler = StandardScaler()
    standardized_combined_data = scaler.fit_transform(combined_data)

    # Perform PCA
    pca = PCA(n_components=PCA_COMPONENTS)
    principal_components_combined = pca.fit_transform(standardized_combined_data)
    principal_df_combined = pd.DataFrame(data=principal_components_combined, columns=['PC1', 'PC2'])

    # Clustering the PCA-transformed data using KMeans
    kmeans = KMeans(n_clusters=KMEANS_NUM_CLUSTERS, random_state=KMEANS_RANDOM_STATE)
    cluster_labels = kmeans.fit_predict(principal_df_combined)

    # Adding cluster labels to the PCA DataFrame
    principal_df_combined['Cluster'] = cluster_labels

    # Plotting the PCA results with cluster assignments
    plt.figure(figsize=(8,6))
    sns.scatterplot(x='PC1', y='PC2', hue='Cluster', palette="bright", data=principal_df_combined)
    plt.title('PCA of Combined Dataset with KMeans Clustering')
    plt.show()

    # Perform t-SNE
    tsne_results = perform_tsne(standardized_combined_data)

    # Perform K-Means clustering on the t-SNE results
    number_of_clusters = 2  # This is an example; you'll need to determine the appropriate number of clusters
    kmeans = KMeans(n_clusters=number_of_clusters, random_state=TSNE_RANDOM_STATE)
    cluster_labels = kmeans.fit_predict(tsne_results)

    # Add the cluster labels to your plot
    plt.figure(figsize=(10, 8))
    plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=cluster_labels, cmap='viridis')
    plt.title('t-SNE with K-Means Clustering')
    plt.xlabel('t-SNE 1')
    plt.ylabel('t-SNE 2')
    plt.colorbar()  # Show color scale
    plt.show()

    # Perform DBSCAN clustering
    dbscan = DBSCAN(eps=DBSCAN_EPS, min_samples=DBSCAN_MIN_SAMPLES)
    dbscan_labels = dbscan.fit_predict(tsne_results)

    # Plot the DBSCAN results
    plt.figure(figsize=(10, 8))
    plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=dbscan_labels, cmap='viridis')
    plt.title('t-SNE with DBSCAN Clustering')
    plt.xlabel('t-SNE 1')
    plt.ylabel('t-SNE 2')
    plt.colorbar()  # Show color scale
    plt.show()

    # # Perform Hierarchical Clustering
    # Z = perform_hierarchical_clustering(standardized_combined_data)

    # # Plot dendrogram
    # plt.figure(figsize=(14, 7))
    # dendrogram(Z, truncate_mode='lastp', p=12, leaf_rotation=45., leaf_font_size=15., show_contracted=True)
    # plt.title('Hierarchical Clustering Dendrogram')
    # plt.xlabel('Cluster Size')
    # plt.ylabel('Distance')
    # plt.show()

    # Silhouette analysis to find the optimal number of clusters (optional)
    # Uncomment the following lines to run silhouette analysis
    # silhouette_scores = []
    # for n_clusters in range(SILHOUETTE_RANGE_START, SILHOUETTE_RANGE_END):
    #     cluster_labels = fcluster(Z, n_clusters, criterion='maxclust')
    #     silhouette_avg = silhouette_score(standardized_combined_data, cluster_labels)
    #     silhouette_scores.append(silhouette_avg)
    #     print(f"Silhouette Score for {n_clusters} clusters: {silhouette_avg}")
        
if __name__ == "__main__":
    main()