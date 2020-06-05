import sys
import time
import pandas as pd
import fire
import src.features.build_features as ft
import src.models.model as mdl
import src.models.recommender as rec
import src.visualization.visualize as vis
from src.evaluation.evaluate import evaluate_knn


def read_portfolio(path):
    try:
        portfolio = pd.read_csv(path, index_col='id')
    except ValueError:
        print('\033[31m'+'ERRO: O portfólio selecionado não segue o padrão necessário. '
                         'Leia a documentação e faça as adequações.'+'\033[0;0m')
        sys.exit(0)
    return portfolio


def run(myportfolio):
    ft.check_data()
    raw_market, processed_market = ft.load_data()

    mdl.check_model()
    model = mdl.load_model()

    portfolio = read_portfolio('portfolios/'+myportfolio)

    start = time.time()

    processed_portfolio = ft.build_portfolio(processed_market, portfolio)

    print(f'Gerando recomendações para {myportfolio}...')
    leads = rec.generate_leads(processed_portfolio, processed_market, model)
    raw_leads, df_leads = rec.build_leads_df(raw_market, leads)
    processed_leads = ft.process_leads(leads, processed_market)

    print('Gerando gráficos sobre as recomendações...')
    vis.build_charts(df_leads)

    print('Salvando recomendações...')
    rec.save_leads(raw_leads, df_leads)

    end = time.time()

    print('='*50)
    print(f'Fim do processo. Tempo gasto: {round(end-start, 3)} segundos')
    print('=' * 50)
    extreme, high, medium = evaluate_knn(processed_portfolio, processed_leads)
    print(f'{round(extreme * 100, 1)}% dos resultados como EXTREMAMENTE RECOMENDADOS')
    print(f'{round(high * 100, 1)}% dos resultados como ALTAMENTE RECOMENDADOS')
    print(f'{round(medium * 100, 1)}% dos resultados como MEDIAMENTE RECOMENDADOS')
    print('=' * 50)
    print('Os resultados foram salvos na pasta "output".')


def cli():
    return fire.Fire(run)


if __name__ == '__main__':
    cli()
