import os
import pandas as pd
from src.evaluation.evaluate import similarity_metric

usefull_cols = ['sg_uf', 'nm_meso_regiao', 'nm_micro_regiao', 'fl_rm', 'setor', 'nm_segmento',
                'de_natureza_juridica', 'de_nivel_atividade', 'idade_empresa_anos', 'vl_faturamento_estimado_aux']


def generate_leads(processed_portfolio, processed_market, model):
    """Generate recommendations via kneighbors, remove duplicates and
    ids already included in portfolio.

    Args:
        processed_portfolio (pandas.core.frame.DataFrame): Processed portfolio dataframe.
        processed_market (pandas.core.frame.DataFrame): Processed market dataframe.
        model (sklearn.neighbors._unsupervised.NearestNeighbors): NN model.

    Returns:
        Panda Series with recommended ids
    """

    dist, indices = model.kneighbors(processed_portfolio.dropna())

    leads = pd.DataFrame(list(zip(processed_market.index[indices.flatten()], dist.flatten())),
                         columns=['COMPANY ID', 'DISTANCE'])
    leads = leads.sort_values('DISTANCE').set_index('COMPANY ID')

    leads = leads.loc[~leads.index.duplicated(keep='first')]
    leads = leads.drop([x for x in leads.index if x in processed_portfolio.index])

    return leads


def build_leads_df(raw_market, leads):
    """Build raw dataframe and a fancy dataframe(with the usefulls columns).
    The fancy dataframe  makes the viewing / decision-making experience more user-friendly,
    since only columns with relevance to these processes are displayed.

    Args:
        raw_market (pandas.core.frame.DataFrame): Processed portfolio dataframe.
        leads (pandas.core.series.Series): Leads ids.

    Returns:
        A raw dataframe and a dataframe proper to visualization, both composed by the recommended companies.
    """

    raw_leads = raw_market.reindex(leads.index)

    # Build leads dataframe with usefull columns
    df_leads = raw_market[usefull_cols].reindex(raw_leads.index)
    df_leads.reset_index(level=0, inplace=True)  # Reset index
    df_leads.index = pd.RangeIndex(1, df_leads.shape[0]+1)  # Set start at 1
    df_leads.columns = ['ID', 'UF', 'MESO REGIAO', 'MICRO REGIAO', 'RM', 'SETOR', 'SEGMENTO',
                        'NATUREZA JURIDICA', 'NIVEL DE ATIVIDADE', 'IDADE', 'FATURAMENTO ESTIMADO']

    return raw_leads, df_leads


def color_reliability(val):
    """Returns different shades of green for different levels of similarity."""

    if val == 'EXTREMA':
        color='#1f7a1f'
        return f'background-color: {color}'
    elif val == 'ALTA':
        color='#85e085'
        return f'background-color: {color}'
    elif val == 'MÉDIA':
        color='#d8ebb5'
        return f'background-color: {color}'
    else:
        pass


def colorize_df(df, processed_portfolio, processed_leads):
    """Calculates similariry metric and make a stylized dataframe, with a new column
    colorized according the levels of similarity"""

    df['CONFIABILIDADE'] = similarity_metric(processed_portfolio, processed_leads)
    return df.style.applymap(color_reliability, subset=['CONFIABILIDADE'])


def save_leads(raw_leads, df_leads):
    """Save raw and fancy leads dataframe as .csv. Also save just the IDs in a .txt file"""

    if not os.path.exists('output'):
        os.mkdir('output')

    raw_leads.to_csv('output/raw_leads.csv')
    df_leads.to_csv('output/leads.csv')
    with open('output/leads_id.txt', 'w') as f:
        for item in df_leads['ID']:
            f.write("%s\n" % item)
