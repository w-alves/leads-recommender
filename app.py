import os
import streamlit as st
import pandas as pd
from src.features.build_features import build_portfolio, process_leads, load_data
from src.models.model import load_model, train_model
from src.models.recommender import colorize_df
from src.models.recommender import build_leads_df, save_leads, generate_leads
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
            with st.spinner('Gerando recomendações...'):
                processed_portfolio = build_portfolio(processed_market, portfolio)
                leads = generate_leads(processed_portfolio, processed_market, model)

                processed_leads = process_leads(leads, processed_market)
                raw_leads, df_leads = build_leads_df(raw_market, leads)
                save_leads(raw_leads, df_leads)

                df_leads_colorized = colorize_df(df_leads, processed_portfolio, processed_leads)

                st.header('Dashboard:')
                st.dataframe(df_leads_colorized)

                st.success('Recomendação concluída! Os resultados estão salvos na pasta "output".')

                st.subheader('Visualize dados importantes sobre as empresas recomendadas:')
                show_charts(build_charts(df_leads))


if __name__ == '__main__':
    main()
