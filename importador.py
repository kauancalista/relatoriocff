import os
import shutil


def importar_arquivos(pasta_origem, pasta_destino, mover=True):
    processados = []
    ignorados = []

    for arquivo in os.listdir(pasta_origem):
        caminho_origem = os.path.join(pasta_origem, arquivo)

        if not os.path.isfile(caminho_origem):
            continue

        # strip antes de upper para remover espaços originais do nome
        novo_nome = arquivo.strip().upper()
        caminho_destino = os.path.join(pasta_destino, novo_nome)

        # Pula se o arquivo já existe no destino (evita duplicatas)
        if os.path.exists(caminho_destino):
            ignorados.append(novo_nome)
            continue

        if mover:
            shutil.move(caminho_origem, caminho_destino)
        else:
            shutil.copy2(caminho_origem, caminho_destino)

        processados.append(novo_nome)

    return processados, ignorados
