import pandas as pd
from dash import dcc, html
import plotly.express as px


def ler_csv():
    colunas_desejadas = [
        "NO_MUNICIPIO_ESC",
        "SG_UF_ESC",
        "NU_NOTA_MT",
        "NU_NOTA_REDACAO"
    ]

    resultados = []

    chunksize = 10000

    for chunk in pd.read_csv(
        "./data/MICRODADOS_ENEM_2022.csv",
        usecols=colunas_desejadas,
        chunksize=chunksize,
        sep=";",
        encoding='latin-1'
    ):
        chunk_filtrado = chunk[chunk["SG_UF_ESC"] == "RJ"]
        resultados.append(chunk_filtrado)

    dados_selecionados = pd.concat(resultados)

    return dados_selecionados


def agrupar_e_ordenar_dados(df):
    df['nota'] = df['NU_NOTA_REDACAO'] + df['NU_NOTA_MT']

    media_notas_por_municipio = df.groupby(
        'NO_MUNICIPIO_ESC')['nota'].mean().reset_index()

    municipios_ordenados = media_notas_por_municipio.sort_values(
        by='nota', ascending=False)

    top_10_maiores_notas = municipios_ordenados.head(10)
    top_10_menores_notas = municipios_ordenados.tail(10).sort_values(by='nota', ascending=True)

    return (top_10_maiores_notas, top_10_menores_notas)


def gerar_graficos(app, top_10_maiores_notas, top_10_menores_notas):
    fig_maiores = px.bar(top_10_maiores_notas, x='nota', y='NO_MUNICIPIO_ESC', orientation='h',
                         title='Top 10 Municípios com Maiores Notas',
                         labels={'nota': 'Nota Média',
                                 'NO_MUNICIPIO_ESC': 'Município'},
                         color='NO_MUNICIPIO_ESC')
    fig_menores = px.bar(top_10_menores_notas, x='nota', y='NO_MUNICIPIO_ESC', orientation='h',
                         title='Top 10 Municípios com Menores Notas',
                         labels={'nota': 'Nota Média',
                                 'NO_MUNICIPIO_ESC': 'Município'},
                         color='NO_MUNICIPIO_ESC')

    app.layout = html.Div([
        html.H1("Dashboard Notas do ENEM por Município"),
        html.Div([
            dcc.Graph(figure=fig_maiores)
        ]),
        html.Div([
            dcc.Graph(figure=fig_menores)
        ])
    ])


def exibir_dashboard(app):
    df = ler_csv()
    top_10_maiores_notas, top_10_menores_notas = agrupar_e_ordenar_dados(df)
    gerar_graficos(app, top_10_maiores_notas, top_10_menores_notas)
