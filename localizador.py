import os
import unicodedata


EXTENSOES_VALIDAS = [
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png"
]


def normalizar(texto):
    texto = str(texto).upper().strip()

    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    return texto


def localizar_documento(nome_base, pasta):
    """
    Procura um documento pelo nome,
    ignorando acentos e maiúsculas/minúsculas.
    """

    nome_base = normalizar(nome_base)

    for arquivo in os.listdir(pasta):

        nome_arquivo, extensao = os.path.splitext(arquivo)

        if extensao.lower() not in EXTENSOES_VALIDAS:
            continue

        if normalizar(nome_arquivo) == nome_base:
            return os.path.join(pasta, arquivo)

    return None