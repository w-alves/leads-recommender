import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from scipy.spatial.distance import cdist


def similarity_metric(processed_portfolio, processed_leads):
    # Count how many recommended leads have 95% or more of similarity with  at least one company of portfolio
    reliability_list = []

    for lead in processed_leads.values:
        similarities = 1 - cdist([lead], processed_portfolio.dropna().values, metric='cosine')

        if similarities[similarities >= 0.925].shape[0] > 0:
            reliability_list.append('EXTREMA')
        elif similarities[(similarities >= 0.825) & (similarities < 0.925)].shape[0] > 0:
            reliability_list.append('ALTA')
        else:
            reliability_list.append('MÉDIA')

    return reliability_list


def evaluate_knn(processed_portfolio, processed_leads):
    reliability_list = similarity_metric(processed_portfolio, processed_leads)

    extreme_reliability = reliability_list.count('EXTREMA') / processed_leads.shape[0]
    high_reliability = reliability_list.count('ALTA') / processed_leads.shape[0]
    medium_reliability = reliability_list.count('MÉDIA') / processed_leads.shape[0]

    return extreme_reliability, high_reliability, medium_reliability
