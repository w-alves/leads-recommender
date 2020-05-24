import os
import time
import streamlit as st
import pickle
from sklearn.neighbors import NearestNeighbors
import src.features.build_features as ft


def train_model():
    _, processed_market = ft.load_data()
    model_knn = NearestNeighbors(algorithm='ball_tree', n_neighbors=6, n_jobs=-1)
    model_knn.fit(processed_market)

    if not os.path.exists('model'):
        os.mkdir('model')

    with open('model/leads-recommender-model.pkl', 'wb') as file:
        pickle.dump(model_knn, file)


@st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
def load_model():
    with open('model/leads-recommender-model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model


def check_model():
    if not os.path.exists('model/leads-recommender-model.pkl'):
        start = time.time()
        print('Não encontremos o modelo pré-treinado no seu diretório, vamos treiná-lo novamente...')
        train_model()
        end = time.time()
        print('Treinamento finalizado.')
        print(f'Tempo gasto treinando o modelo: {round(end-start, 3)} segundos')
        print('=' * 50)
