from sklearn import metrics
from prettytable import PrettyTable


def evaluate_clustering(name, X, true_labels, pred_labels):
    homogeneity = metrics.homogeneity_score(true_labels, pred_labels)
    completeness = metrics.completeness_score(true_labels, pred_labels)
    v_measure = metrics.v_measure_score(true_labels, pred_labels)
    
    adj_rand_score = metrics.adjusted_rand_score(true_labels, pred_labels)
    norm_mutual_score = metrics.normalized_mutual_info_score(true_labels, pred_labels)
    
    fowlkes_m = metrics.fowlkes_mallows_score(true_labels, pred_labels)
    #silhouette = metrics.silhouette_score(X, pred_labels, metric='euclidean')
    
    return [name, "{:.2f}".format(homogeneity), "{:.2f}".format(completeness), "{:.2f}".format(v_measure), "{:.2f}".format(adj_rand_score), "{:.2f}".format(norm_mutual_score), "{:.2f}".format(fowlkes_m)]


def tabulate_results(results):
    t = PrettyTable(['Name', 'Homogeneity', 'Completeness', 'V Measure', 'Adj Rand Score', 'Norm Mutual Score', 'Fowlkes Mallows'])
    for result in results:
        t.add_row(result)
    
    print(t)
    
def tab_results(header, results):
    t = PrettyTable(header)
    for result in results:
        t.add_row(result)
    
    print(t)
    
def evaluate_vmeasure(true_labels, pred_labels):
    return metrics.v_measure_score(true_labels, pred_labels)
    
def evaluate_fm(true_labels, pred_labels):
    return metrics.fowlkes_mallows_score(true_labels, pred_labels)