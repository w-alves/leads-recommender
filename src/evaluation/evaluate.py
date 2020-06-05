from scipy.spatial.distance import cdist


def similarity_metric(processed_portfolio, processed_leads):
    """Find the similarity level of a recommended company with a company
    that is already included in original portfolio.

    Args:
        processed_portfolio (pandas.core.frame.DataFrame): Processed portfolio dataframe.
        processed_leads (pandas.core.frame.DataFrame): Processed leads dataframe.

    Returns:
        A list with the maximum similarity level found for each lead in processed_leads.
    """

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
    """Call Similarity_metric functions and calculates the
    percentage of each similarity level.

    Args:
        processed_portfolio (pandas.core.frame.DataFrame): Processed portfolio dataframe.
        processed_leads (pandas.core.frame.DataFrame): Processed leads dataframe.

    Returns:
        Percentage of recommended companies classified as EXTREMELY RECOMMENDED
        Percentage of recommended companies classified as HIGHLY RECOMMENDED
        Percentage of recommended companies classified as MEDIUM RECOMMENDED
    """

    reliability_list = similarity_metric(processed_portfolio, processed_leads)

    extreme_reliability = reliability_list.count('EXTREMA') / processed_leads.shape[0]
    high_reliability = reliability_list.count('ALTA') / processed_leads.shape[0]
    medium_reliability = reliability_list.count('MÉDIA') / processed_leads.shape[0]

    return extreme_reliability, high_reliability, medium_reliability
