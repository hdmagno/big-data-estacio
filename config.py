import sqlite3
import pandas as pd
from dash import dcc, html
import plotly.express as px

from models.Estudante import CorRaca, Escola, FaixaEtaria, CriarEstudanteDTO


def conectar_banco_de_dados():
    return sqlite3.connect("./data/enem.db")


def criar_tabelas():
    conexao = conectar_banco_de_dados()
    cursor = conexao.cursor()

    sql = """
        CREATE TABLE IF NOT EXISTS estudantes
        (id INTEGER,
        inscricao TEXT,
        faixa_etaria TEXT,
        sexo TEXT,
        cor_raca TEXT,
        escola TEXT,
        municipio TEXT,
        uf TEXT,
        nota_ciencias_natureza REAL,
        nota_ciencias_humanas REAL,
        nota_linguagens_codigos REAL,
        nota_matematica REAL,
        nota_redacao REAL,
        
        PRIMARY KEY (id))
    """

    cursor.execute(sql)
    conexao.commit()
    conexao.close()


def ler_csv():
    colunas_desejadas = [
        "NU_INSCRICAO",
        "TP_FAIXA_ETARIA",
        "TP_SEXO",
        "TP_COR_RACA",
        "TP_ESCOLA",
        "NO_MUNICIPIO_ESC",
        "SG_UF_ESC",
        "NU_NOTA_CN",
        "NU_NOTA_CH",
        "NU_NOTA_LC",
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


def gerar_lista_estudantes(dados_csv):
    estudantes = []

    for _, row in dados_csv.iterrows():
        estudante_csv = {
            "inscricao": row["NU_INSCRICAO"],
            "faixa_etaria": FaixaEtaria(int(row["TP_FAIXA_ETARIA"])),
            "sexo": row["TP_SEXO"],
            "cor_raca": CorRaca(int(row["TP_COR_RACA"])),
            "escola": Escola(int(row["TP_ESCOLA"])),
            "municipio": row["NO_MUNICIPIO_ESC"],
            "uf": row["SG_UF_ESC"],
            "nota_ciencias_natureza": float(row["NU_NOTA_CN"]),
            "nota_ciencias_humanas": float(row["NU_NOTA_CH"]),
            "nota_linguagens_codigos": float(row["NU_NOTA_LC"]),
            "nota_matematica": float(row["NU_NOTA_MT"]),
            "nota_redacao": float(row["NU_NOTA_REDACAO"])
        }

        estudante = CriarEstudanteDTO(**estudante_csv)

        estudantes.append(estudante)

    return estudantes


def salvar_no_banco_de_dados(estudantes):
    conexao = conectar_banco_de_dados()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO estudantes (
            inscricao,
            faixa_etaria,
            sexo,
            cor_raca,
            escola,
            municipio,
            uf,
            nota_ciencias_natureza,
            nota_ciencias_humanas,
            nota_linguagens_codigos,
            nota_matematica,
            nota_redacao
        ) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """

    valores = [
        (
            estudante.inscricao,
            estudante.faixa_etaria.name,
            estudante.sexo,
            estudante.cor_raca.name,
            estudante.escola.name,
            estudante.municipio,
            estudante.uf,
            estudante.nota_ciencias_natureza,
            estudante.nota_ciencias_humanas,
            estudante.nota_linguagens_codigos,
            estudante.nota_matematica,
            estudante.nota_redacao,
        )
        for estudante in estudantes
    ]

    cursor.executemany(sql, valores)
    conexao.commit()
    conexao.close()

    print("Fim...")


def preparar_dados():
    criar_tabelas()
    dadosCSV = ler_csv()
    estudantes = gerar_lista_estudantes(dadosCSV)
    salvar_no_banco_de_dados(estudantes)


def acessar_banco_de_dados():
    conexao = conectar_banco_de_dados()

    sql = "SELECT municipio, nota_redacao, nota_matematica FROM estudantes"
    df = pd.read_sql_query(sql, conexao)
    conexao.close()

    return df


def agrupar_e_ordenar_dados(df):
    df['nota'] = df['nota_redacao'] + df['nota_matematica']

    media_notas_por_municipio = df.groupby(
        'municipio')['nota'].mean().reset_index()

    municipios_ordenados = media_notas_por_municipio.sort_values(
        by='nota', ascending=False)

    top_10_maiores_notas = municipios_ordenados.head(10)
    top_10_menores_notas = municipios_ordenados.tail(10)

    return (top_10_maiores_notas, top_10_menores_notas)


def gerar_dashboard(app, top_10_maiores_notas, top_10_menores_notas):
    fig_maiores = px.bar(top_10_maiores_notas, x='nota', y='municipio', orientation='h',
                         title='Top 10 Municípios com Maiores Notas',
                         labels={'nota': 'Nota Média',
                                 'municipio': 'Município'},
                         color='municipio')
    fig_menores = px.bar(top_10_menores_notas, x='nota', y='municipio', orientation='h',
                         title='Top 10 Municípios com Menores Notas',
                         labels={'nota': 'Nota Média',
                                 'municipio': 'Município'},
                         color='municipio')

    app.layout = html.Div([
        html.H1("Dashboard de Notas ENEM por Município"),
        html.Div([
            dcc.Graph(figure=fig_maiores)
        ]),
        html.Div([
            dcc.Graph(figure=fig_menores)
        ])
    ])


def exibir_dados(app):
    df = acessar_banco_de_dados()
    top_10_maiores_notas, top_10_menores_notas = agrupar_e_ordenar_dados(df)
    gerar_dashboard(app, top_10_maiores_notas, top_10_menores_notas)
