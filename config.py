import pandas as pd
import sqlite3

from models.Estudante import CorRaca, Escola, FaixaEtaria, CriarEstudanteDTO


def criar_banco_de_dados() -> None:
    conexao = sqlite3.connect("./data/enem.db")
    cursor = conexao.cursor()

    criar_tabela = """
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

    cursor.execute(criar_tabela)
    conexao.commit()
    conexao.close()


def ler_csv() -> pd.DataFrame:
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


def gerar_lista_estudantes(dados_csv: pd.DataFrame) -> list[CriarEstudanteDTO]:
    estudantes: list[CriarEstudanteDTO] = []

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


def salvar_no_banco_de_dados(estudantes: list[CriarEstudanteDTO]) -> None:
    conexao = sqlite3.connect("./data/enem.db")
    cursor = conexao.cursor()

    inserir_registros = """
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

    cursor.executemany(inserir_registros, valores)
    conexao.commit()
    conexao.close()

    print("Fim...")
