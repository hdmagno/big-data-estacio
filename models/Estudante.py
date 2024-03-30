from dataclasses import dataclass
from enum import Enum


class FaixaEtaria(Enum):
    MENOR_17_ANOS = 1
    TEM_17_ANOS = 2
    TEM_18_ANOS = 3
    TEM_19_ANOS = 4
    TEM_20_ANOS = 5
    TEM_21_ANOS = 6
    TEM_22_ANOS = 7
    TEM_23_ANOS = 8
    TEM_24_ANOS = 9
    TEM_25_ANOS = 10
    ENTRE_26_E_30_ANOS = 11
    ENTRE_31_E_35_ANOS = 12
    ENTRE_36_E_40_ANOS = 13
    ENTRE_41_E_45_ANOS = 14
    ENTRE_46_E_50_ANOS = 15
    ENTRE_51_E_55_ANOS = 16
    ENTRE_56_E_60_ANOS = 17
    ENTRE_61_E_65_ANOS = 18
    ENTRE_66_E_70_ANOS = 19
    MAIOR_70_ANOS = 20


class CorRaca(Enum):
    NAO_DECLARADO = 0
    BRANCA = 1
    PRETA = 2
    PARDA = 3
    AMARELA = 4
    INDIGENA = 5
    NAO_DISPOE_DA_INFORMACAO = 6


class Escola(Enum):
    NAO_RESPONDEU = 1
    PUBLICA = 2
    PRIVADA = 3


@dataclass
class CriarEstudanteDTO:
    inscricao: str
    faixa_etaria: FaixaEtaria
    sexo: str
    cor_raca: CorRaca
    escola: Escola
    municipio: str
    uf: str
    nota_ciencias_natureza: float
    nota_ciencias_humanas: float
    nota_linguagens_codigos: float
    nota_matematica: float
    nota_redacao: float
