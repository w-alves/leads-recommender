import base64
import os
import streamlit as st
import pandas as pd
from src.features.build_features import build_portfolio, load_data
from src.models.model import load_model, train_model
from src.models.recommender import build_leads_df, save_leads, recommender
from src.visualization.visualize import build_charts


def show_charts(charts):
    for fig in charts:
        st.pyplot(fig)


def main():
    raw_market, processed_market = load_data()

    if not os.path.exists('model/leads-recommender-model.pkl'):
        with st.spinner('Não encontremos o modelo pré-treinado no seu diretório, vamos treiná-lo novamente...'):
            train_model()
        st.success('Modelo treinado! Nas próximas execuções essa tarefa não precisará ser realizada novamente.')

    st.title('Leads recommender')
    fileup = st.file_uploader('Faça o upload de seu portfólio')

    model = load_model()

    if fileup is not None:
        try:
            portfolio = pd.read_csv(fileup, index_col='id')
            flag = 1
        except ValueError:
            st.error('O portfólio selecionado não segue o padrão necessário, adeque-o e tente novamente. \n'
                     'Para saber mais, consulte a documentação.')
            flag = 0

        if flag == 1:
            st.success('Recomendação concluída! Os resultados estão salvos na pasta "output".')

            processed_portfolio = build_portfolio(processed_market, portfolio)
            leads = recommender(processed_portfolio, processed_market, model)
            raw_leads, df_leads = build_leads_df(raw_market, leads)
            save_leads(raw_leads, df_leads)

            st.header('Dashboard:')
            slider = st.slider('Número de leads exibidos:', min_value=10, max_value=df_leads.shape[0])
            multi = st.multiselect('Colunas exibidas:', tuple(df_leads.columns), list(df_leads.columns))
            showing_leads = df_leads[multi].head(slider)

            st.dataframe(showing_leads)

            st.text('Visualize dados importantes sobre as empresas recomendadas:')
            show_charts(build_charts(df_leads))


if __name__ == '__main__':
    main()
