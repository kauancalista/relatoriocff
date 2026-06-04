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

    # 4. Remove espaços duplos (ex: "JOAO   SILVA" -> "JOAO SILVA")
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto


def tratar_casamentos(texto):
    # Se houver " E ", pega apenas o primeiro nome da lista
    if " E " in texto:
        return texto.split(" E ")[0].strip()
    return texto


def localizar_documento(nome_original, pasta):
    # Trata casamentos e normaliza a base
    nome_base = normalizar(tratar_casamentos(nome_original))

    melhor_match = None
    maior_similaridade = 0
    arquivo_encontrado = None

    for arquivo in os.listdir(pasta):
        nome_arquivo, extensao = os.path.splitext(arquivo)
        if extensao.lower() not in EXTENSOES_VALIDAS:
            continue

        nome_arquivo_norm = normalizar(nome_arquivo)

        # CAMADA 1: Busca Exata (Normalizada)
        if nome_arquivo_norm == nome_base:
            return {
                "caminho": os.path.join(pasta, arquivo),
                "tipo": "Exata / Normalizada",
                "similaridade": 100,
                "arquivo": arquivo
            }

        # CAMADA 2: Calcula Similaridade
        similaridade = fuzz.ratio(nome_base, nome_arquivo_norm)
        if similaridade > maior_similaridade:
            maior_similaridade = similaridade
            melhor_match = nome_arquivo_norm
            arquivo_encontrado = arquivo

    # CAMADA 3: Retorna se a similaridade for >= 90%
    if maior_similaridade >= 90:
        return {
            "caminho": os.path.join(pasta, arquivo_encontrado),
            "tipo": "Similaridade",
            "similaridade": round(maior_similaridade, 1),
            "arquivo": arquivo_encontrado
        }

    return None