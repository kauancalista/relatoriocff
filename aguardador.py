import time
from tkinter import messagebox
from localizador import localizar_documento


def tratar_nome(nome):
    """Garante o corte correto se for casamento antes de buscar o anexo"""
    nome_upper = nome.upper()
    if " E " in nome_upper:
        return nome_upper.split(" E ")[0].strip()
    return nome_upper


def aguardar_documentos(nome, pasta, log_callback, modo="CPF"):
    while True:
        doc_principal = localizar_documento(nome, pasta)
        nome_limpo = tratar_nome(nome)

        doc_secundario = None
        nome_secundario_exibicao = ""

        # LÓGICA DO SEGUNDO DOCUMENTO BASEADA NO MODO
        if modo == "CPF":
            doc_secundario = localizar_documento(f"{nome_limpo} CPF", pasta)
            nome_secundario_exibicao = "CPF"

        elif modo == "CERTIDAO":
            # Tenta encontrar qualquer uma das variações
            sufixos = [" + FERC", " + CRAS", " + REGISTRE-SE", " FERC", " CRAS", " REGISTRE-SE"]
            for sufixo in sufixos:
                doc_secundario = localizar_documento(f"{nome_limpo}{sufixo}", pasta)
                if doc_secundario:
                    break
            nome_secundario_exibicao = "Anexo (FERC/CRAS/REGISTRE-SE)"

        # VERIFICAÇÃO FINAL
        if doc_principal and doc_secundario:
            return doc_principal, doc_secundario

        # SE FALTAR ALGO, MONTA A TELA DE AVISO
        status_principal = "✓ Documento Principal" if doc_principal else "✗ Documento Principal"
        status_sec = f"✓ {nome_secundario_exibicao}" if doc_secundario else f"✗ {nome_secundario_exibicao}"

        msg = f"Pendência encontrada para:\n{nome}\n\n{status_principal}\n{status_sec}\n\n"
        msg += "O que deseja fazer?\n"
        msg += "[Sim] = Tentar achar de novo (Coloque o arquivo na pasta)\n"
        msg += "[Não] = Ignorar o que falta e gerar mesmo assim\n"
        msg += "[Cancelar] = Parar a geração do relatório agora"

        resposta = messagebox.askyesnocancel("Documento Faltando", msg)

        if resposta is True:
            log_callback(f"Aguardando arquivos para: {nome}...")
            time.sleep(1)
            continue
        elif resposta is False:
            log_callback(f"⚠ Faltando documentos. Ignorando e avançando: {nome}.")
            return doc_principal, doc_secundario
        else:
            raise Exception("O processo foi cancelado pelo usuário.")