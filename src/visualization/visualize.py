import os
import seaborn as sns
import matplotlib.pyplot as plt


def build_charts(df):
    """Generate, save and return charts."""

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
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=45, ha="right")
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
