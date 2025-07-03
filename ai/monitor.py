"""Simple anomaly detection and auto-scaling helpers."""
import numpy as np
from sklearn.cluster import KMeans
import boto3


def analyze_anomalies(region_issues):
    """Return anomaly labels (High/Normal) for each region."""
    counts = [len(issues) for regions in region_issues.values() for issues in regions.values()]
    if not counts:
        return {}
    X = np.array(counts).reshape(-1, 1)
    km = KMeans(n_clusters=2, n_init='auto').fit(X)
    high_cluster = int(np.argmax(km.cluster_centers_))
    labels = {}
    idx = 0
    for account, regions in region_issues.items():
        labels[account] = {}
        for region, issues in regions.items():
            labels[account][region] = 'High' if km.labels_[idx] == high_cluster else 'Normal'
            idx += 1
    return labels


def auto_scale(anomalies, function_name):
    """Scale Lambda concurrency if high anomalies detected."""
    high = any(level == 'High' for acct in anomalies.values() for level in acct.values())
    if high:
        boto3.client('lambda').put_function_concurrency(
            FunctionName=function_name, ReservedConcurrentExecutions=5
        )
