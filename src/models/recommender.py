import pandas as pd

usefull_cols = ['sg_uf', 'nm_meso_regiao', 'nm_micro_regiao', 'fl_rm', 'setor', 'nm_segmento',
                'de_natureza_juridica', 'de_nivel_atividade', 'idade_empresa_anos', 'vl_faturamento_estimado_aux']


def recommender(processed_portfolio, processed_market, model):
    # Finds the neighbors for each company of portfolio
    dist, indices = model.kneighbors(processed_portfolio.dropna())

    # Build a dataframe with dist and indices
    leads = pd.DataFrame(list(zip(processed_market.index[indices.flatten()], dist.flatten())),
                         columns=['COMPANY ID', 'DISTANCE'])

    # Sort values by distance
    leads = leads.sort_values('DISTANCE').set_index('COMPANY ID')

    # Remove duplicates and companies already included in portfolio
    leads = leads.loc[~leads.index.duplicated(keep='first')]
    leads = leads.drop([x for x in leads.index if x in processed_portfolio.index])

    return leads


def build_leads_df(raw_market, leads):
    # Build a dataframe with usefull cols and change the index for the rank
    raw_leads = raw_market.reindex(leads.index)

    df_leads = raw_market[usefull_cols].reindex(leads.index)
    df_leads.reset_index(level=0, inplace=True)  # Reset index
    df_leads.index = pd.RangeIndex(1, df_leads.shape[0]+1)  # Set start at 1
    df_leads.columns = ['ID', 'UF', 'MESO REGIAO', 'MICRO REGIAO', 'RM', 'SETOR', 'SEGMENTO',
                        'NATUREZA JURIDICA', 'NIVEL DE ATIVIDADE', 'IDADE', 'FATURAMENTO ESTIMADO']

    return raw_leads, df_leads


def save_leads(raw_leads, df_leads):
    raw_leads.to_csv('output/raw_leads.csv')
    df_leads.to_csv('output/leads.csv')
    with open('output/leads_id.txt', 'w') as f:
        for item in df_leads['ID']:
            f.write("%s\n" % item)
