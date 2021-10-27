import umap.umap_ as umap
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler

def plot_clusters(name, X, labels):
    sns.set(style='white', context='poster', rc={'figure.figsize':(18,14)})
    sns.set_color_codes()
    plot_kwds = {'alpha' : 0.5, 's' : 80, 'linewidths':0}
    
    reducer = umap.UMAP(n_components=3)
    
    #X = StandardScaler(with_mean=False).fit_transform(X)
    
    embedding = reducer.fit_transform(X)
    embedding = embedding.astype('float64')
    
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.scatter(embedding[:, 0], embedding[:, 1], **plot_kwds, c=labels, cmap="Spectral")
    #plt.setp(ax, xticks=[], yticks=[])
    plt.title(name + " 1st & 2nd", fontsize=18)
    plt.show()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.scatter(embedding[:, 0], embedding[:, 2],**plot_kwds, c=labels, cmap="Spectral")
    #plt.setp(ax, xticks=[], yticks=[])
    plt.title(name + " 1st & 3rd", fontsize=18)
    plt.show()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.scatter(embedding[:, 1], embedding[:, 2], **plot_kwds, c=labels, cmap="Spectral")
    #plt.setp(ax, xticks=[], yticks=[])
    plt.title(name + " 2nd & 3rd", fontsize=18)
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plot = ax.scatter(embedding[:,0], embedding[:,1], embedding[:,2], **plot_kwds, c=labels, cmap="Spectral")
    plt.title(name, fontsize=18)

    fig.colorbar(plot, ax = ax, shrink = 0.5, aspect = 5)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plot = ax.scatter(embedding[:,0], embedding[:,1], embedding[:,2], **plot_kwds, c=labels, cmap="Spectral")
    plt.title("TFIDF Vectors by UMAP - Azim (-30), Elevation (60)", fontsize=18)

    ax.azim = -30
    ax.elev = 60

    fig.colorbar(plot, ax = ax, shrink = 0.5, aspect = 5)

    