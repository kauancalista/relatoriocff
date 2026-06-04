import os
import re
import unicodedata
from rapidfuzz import fuzz

EXTENSOES_VALIDAS = [".pdf", ".jpg", ".jpeg", ".png"]


def normalizar(texto):
    # 1. Tudo para maiúsculo e remove espaços nas pontas
    texto = str(texto).upper().strip()

    # 2. Remove acentos (Á vira A, Õ vira O)
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")

    # 3. Substitui pontuações por espaço (.-_())
    texto = re.sub(r'[.,\-_()]', ' ', texto)

    # 4. Remove espaços duplos
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto


def extrair_primeiro_conjuge(texto_normalizado):
    """Pega apenas o primeiro nome se houver ' E '"""
    # Como o texto já foi normalizado antes de chegar aqui,
    # o " e " minúsculo já virou " E " maiúsculo com certeza.
    if " E " in texto_normalizado:
        return texto_normalizado.split(" E ")[0].strip()
    return texto_normalizado


def localizar_documento(nome_original, pasta):
    # Primeiro transforma TUDO em maiúsculo e tira os acentos
    nome_norm_completo = normalizar(nome_original)

    # Depois, cria uma versão cortando o segundo nome (se for casamento)
    nome_primeiro_conjuge = extrair_primeiro_conjuge(nome_norm_completo)

    melhor_match = None
    maior_similaridade = 0
    arquivo_encontrado = None

    for arquivo in os.listdir(pasta):
        nome_arquivo, extensao = os.path.splitext(arquivo)
        if extensao.lower() not in EXTENSOES_VALIDAS:
            continue

        nome_arquivo_norm = normalizar(nome_arquivo)

        # CAMADA 1: Busca Exata pelo CASAL (Ex: O PDF tem o nome dos dois)
        if nome_arquivo_norm == nome_norm_completo:
            return {
                "caminho": os.path.join(pasta, arquivo),
                "tipo": "Exata (Casal Completo)",
                "similaridade": 100,
                "arquivo": arquivo
            }

        # CAMADA 2: Busca Exata APENAS pelo 1º Cônjuge (Ex: O PDF só tem o nome do noivo/noiva)
        if nome_arquivo_norm == nome_primeiro_conjuge:
            return {
                "caminho": os.path.join(pasta, arquivo),
                "tipo": "Exata (1º Cônjuge)",
                "similaridade": 100,
                "arquivo": arquivo
            }

        # CAMADA 3: Calcula a Similaridade.
        # (Usamos o nome do 1º cônjuge para não confundir o sistema)
        similaridade = fuzz.ratio(nome_primeiro_conjuge, nome_arquivo_norm)
        if similaridade > maior_similaridade:
            maior_similaridade = similaridade
            melhor_match = nome_arquivo_norm
            arquivo_encontrado = arquivo

    # CAMADA 4: Retorna se a similaridade for >= 90%
    if maior_similaridade >= 90:
        return {
            "caminho": os.path.join(pasta, arquivo_encontrado),
            "tipo": "Similaridade (1º Cônjuge)",
            "similaridade": round(maior_similaridade, 1),
            "arquivo": arquivo_encontrado
        }

    return None