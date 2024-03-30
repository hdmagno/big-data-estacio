from pandas import DataFrame
from config import (
    criar_banco_de_dados,
    ler_csv, 
    gerar_lista_estudantes,
    salvar_no_banco_de_dados
)
from models.Estudante import CriarEstudanteDTO


def main() -> None:
    criar_banco_de_dados()
    dados: DataFrame = ler_csv()
    estudantes: list[CriarEstudanteDTO] = gerar_lista_estudantes(dados)
    salvar_no_banco_de_dados(estudantes)


if __name__ == '__main__':
    main()
