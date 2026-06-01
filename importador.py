import os
import shutil


def importar_arquivos(pasta_origem, pasta_destino):
    copiados = []

    for arquivo in os.listdir(pasta_origem):
        caminho_origem = os.path.join(pasta_origem, arquivo)

        if not os.path.isfile(caminho_origem):
            continue

        # Já copia transformando o nome em maiúsculo para padronizar
        novo_nome = arquivo.upper().strip()
        caminho_destino = os.path.join(pasta_destino, novo_nome)

        shutil.copy2(caminho_origem, caminho_destino)
        copiados.append(novo_nome)

    return copiados
