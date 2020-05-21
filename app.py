import streamlit as st
import pandas as pd
import base64
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import os


@st.cache(suppress_st_warning=True, show_spinner=False)
def load_data():
    raw_market = pd.read_csv('data/estaticos_market.csv', index_col='id')
    processed_market = pd.read_csv('data/processed_market.csv', index_col='id')

    return raw_market, processed_market


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
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


def get_table_download_link(df, msg):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="{msg}.csv">{msg}</a>'


def build_charts(df):
    sns.set(style='whitegrid')
    sns.set(palette='Reds_r')
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

    return fig1, fig2, fig3


def show_charts(charts):
    for fig in charts:
        st.pyplot(fig)


def main():
    st.title('Leads recommender')
    fileup = st.file_uploader('Upload your portfolio here')

    if fileup is not None:
        portfolio = pd.read_csv(fileup, index_col='id').drop(columns='Unnamed: 0')
        processed_portfolio = processed_market.reindex(portfolio.index)
        raw_leads, df_leads = recommender(processed_portfolio, model)
        slider = st.slider('Number of leads:', min_value=10, max_value=df_leads.shape[0])
        multi = st.multiselect('Showing columns:', tuple(df_leads.columns), list(df_leads.columns))
        showing_leads = df_leads[multi].head(slider)
        st.dataframe(showing_leads)

        st.subheader('Download the leads:')
        st.markdown(get_table_download_link(showing_leads, 'Selected columns'), unsafe_allow_html=True)
        st.markdown(get_table_download_link(df_leads.ID, 'Just IDs'), unsafe_allow_html=True)
        st.markdown(get_table_download_link(raw_leads, 'Default'), unsafe_allow_html=True)
        st.header('Data Visualization:')
        show_charts(build_charts(df_leads))

if __name__ == '__main__':
    usefull_cols = ['sg_uf', 'nm_meso_regiao', 'nm_micro_regiao', 'fl_rm', 'setor', 'nm_segmento',
                    'de_natureza_juridica',
                    'de_nivel_atividade', 'idade_empresa_anos', 'vl_faturamento_estimado_aux']
    raw_market, processed_market = load_data()
    model = load_model()
    main()

