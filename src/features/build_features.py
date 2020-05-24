import sys
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import streamlit as st


@st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
def load_data():
    raw_market = pd.read_csv('data/estaticos_market.csv', index_col='id')
    processed_market = pd.read_csv('data/processed_market.csv', index_col='id')

    return raw_market, processed_market


def build_portfolio(processed_market, portfolio):
    return processed_market.reindex(portfolio.index)


def process_market(df):
    df = df.set_index('id').drop(columns='Unnamed: 0')

    threshold = 0.70
    df = df.loc[:, df.notnull().mean() > threshold]

    categorical_columns = df.select_dtypes(exclude=['int64', 'float64']).columns.tolist()
    numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    df_processed = pd.get_dummies(data=df, columns=categorical_columns)

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[numerical_columns])
    df_processed[numerical_columns] = scaled_data

    return df_processed


def check_data():
    if not os.path.exists('data/estaticos_market.csv'):
        print('\033[31m'+"ERRO: O arquivo 'estaticos_market.csv' não foi encontrado."+'\033[0;0m')
        sys.exit(0)
    elif not os.path.exists('data/processed_market.csv'):
        df = pd.read_csv('data/estaticos_market.csv')
        process_market(df)
