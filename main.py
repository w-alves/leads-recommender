from sklearn.neighbors import NearestNeighbors
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import fire
import time
import os

def load_data():
    raw_market = pd.read_csv('data/estaticos_market.csv', index_col='id')
    processed_market = pd.read_csv('data/processed_market.csv', index_col='id')

    return raw_market, processed_market


def train_model():

    model_knn = NearestNeighbors(algorithm='ball_tree', n_neighbors=6, n_jobs=-1)
    model_knn.fit(processed_market)

    if not os.path.exists('model'):
        os.mkdir('model')

    with open('model/leads-recommender-model.pkl', 'wb') as file:
        pickle.dump(model_knn, file)


def load_model():
    with open('model/leads-recommender-model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model


def recommender(portfolio, model):
    # Finds the neighbors for each companie of portfolio
    dist, indices = model.kneighbors(portfolio.dropna())

    # Build a dataframe with dist and indices
    leads = pd.DataFrame(list(zip(processed_market.index[indices.flatten()], dist.flatten())), columns=['COMPANY ID', 'DISTANCE'])

    # Sort values by distance
    leads = leads.sort_values('DISTANCE').set_index('COMPANY ID')

    # Remove duplicates and companies already included on portfolio
    leads = leads.loc[~leads.index.duplicated(keep='first')]
    leads = leads.drop([x for x in leads.index if x in portfolio.index])

    # Build a dataframe with usefull cols and change the index for the rank
    raw_leads = raw_market.reindex(leads.index)

    df_leads = raw_market[usefull_cols].reindex(leads.index)
    df_leads.reset_index(level=0, inplace=True) # Reset index
    df_leads.index = pd.RangeIndex(1, df_leads.shape[0]+1) # Set start at 1
    df_leads.columns = ['ID', 'UF', 'MESO REGIAO', 'MICRO REGIAO', 'RM', 'SETOR', 'SEGMENTO', 'NATUREZA JURIDICA', 'NIVEL DE ATIVIDADE', 'IDADE', 'FATURAMENTO ESTIMADO']

    return raw_leads, df_leads


def build_charts(df):
    sns.set(style='whitegrid')
    sns.set(palette='Reds_r')

    if not os.path.exists('output'):
        os.mkdir('output')

    fig1, axes = plt.subplots(1, 2, figsize=(10, 5))
    sns.kdeplot(df['FATURAMENTO ESTIMADO'], ax=axes[0], shade=True, bw=2, legend=False)
    axes[0].set(xlabel='Faturamento estimado')
    axes[0].set_title('Distribuição do faturamento estimado')
    sns.kdeplot(df['IDADE'], ax=axes[1], shade=True, legend=False)
    axes[1].set_title('Distribuição das idades')
    fig1.tight_layout()
    fig1.savefig('output/dist_faturamento_idade.png', bbox_inches='tight')

    fig2, axes = plt.subplots(1, 2, figsize=(10, 5))
    sns.countplot(df['UF'], ax=axes[0])
    axes[0].set_title('Número de empresas por estado')
    axes[0].set(xlabel='', ylabel='')
    sns.countplot(df['SETOR'], ax=axes[1])
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation = 45, ha="right")
    axes[1].set_title('Número de empresas por setor')
    axes[1].set(xlabel='', ylabel='')
    fig2.tight_layout()
    fig2.savefig('output/count_uf_setor.png', bbox_inches='tight')

    fig3, axes = plt.subplots(figsize=(15, 10))
    sns.countplot(y=df['SEGMENTO'], color='lightcoral')
    axes.set(xlabel='')
    axes.set_title('Número de empresas por segmento')
    fig3.tight_layout()
    fig3.savefig('output/count_segmento.png', bbox_inches='tight')


def run(myportfolio):
    print('Treinando o modelo...')
    start = time.time()
    if not os.path.exists('model/leads-recommender-model.pkl'):
        train_model()
    end = time.time()
    print('Treinamento finalizado.')
    print(f'Tempo gasto treinando o modelo: {round(end-start, 3)} segundos')
    print('=' * 50)

    model = load_model()

    start = time.time()
    path = 'portfolios/'+myportfolio
    portfolio = pd.read_csv(path, index_col='id').drop(columns='Unnamed: 0')
    processed_portfolio = processed_market.reindex(portfolio.index)
    print(f'Gerando recomendações para {myportfolio}...')
    raw_leads, df_leads = recommender(processed_portfolio, model)

    print('Gerando gráficos sobre as recomendações...')
    build_charts(df_leads)

    print('Salvando recomendações...')
    raw_leads.to_csv('output/raw_leads.csv')
    df_leads.to_csv('output/leads.csv')
    with open('output/leads_id.txt', 'w') as f:
        for item in df_leads.index:
            f.write("%s\n" % item)
    end = time.time()

    print('='*50)
    print(f'Fim do processo. Tempo gasto: {round(end-start, 3)} segundos')
    print('Os resultados foram salvos na pasta "output".')


def cli():
    return fire.Fire(run)

if __name__ == '__main__':
    usefull_cols = ['sg_uf', 'nm_meso_regiao', 'nm_micro_regiao', 'fl_rm', 'setor', 'nm_segmento',
                    'de_natureza_juridica',
                    'de_nivel_atividade', 'idade_empresa_anos', 'vl_faturamento_estimado_aux']
    raw_market, processed_market = load_data()
    cli()