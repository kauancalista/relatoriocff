import time
from tkinter import messagebox
from localizador import localizar_documento


def aguardar_documentos(nome, pasta, log_callback):
    """
    Tenta localizar. Se não achar, pergunta ao usuário se ele quer
    Aguardar, Ignorar ou Cancelar toda a operação.
    """
    while True:
        doc_principal = localizar_documento(nome, pasta)

        # Para o CPF, tratamos o casamento primeiro para garantir que a busca fique "NOME CPF"
        if " E " in nome.upper():
            nome_limpo = nome.upper().split(" E ")[0].strip()
        else:
            nome_limpo = nome

        doc_cpf = localizar_documento(f"{nome_limpo} CPF", pasta)

        if doc_principal and doc_cpf:
            return doc_principal, doc_cpf

        # Se chegou aqui, está faltando documento. Montamos a janela de erro.
        faltam = []
        status_principal = "✓ Documento Principal" if doc_principal else "✗ Documento Principal"
        status_cpf = "✓ CPF" if doc_cpf else "✗ CPF"

        msg = f"Pendência encontrada para:\n{nome}\n\n{status_principal}\n{status_cpf}\n\n"
        msg += "O que deseja fazer?\n"
        msg += "[Sim] = Tentar achar de novo (Coloque o arquivo na pasta)\n"
        msg += "[Não] = Ignorar o que falta e gerar mesmo assim\n"
        msg += "[Cancelar] = Parar a geração do relatório agora"

        # Pop-up nativo e elegante (Sim, Não, Cancelar)
        resposta = messagebox.askyesnocancel("Documento Faltando", msg)

        if resposta is True:
            # Sim -> Tenta de novo
            log_callback(f"Aguardando arquivos para: {nome}...")
            time.sleep(1)
            continue
        elif resposta is False:
            # Não -> Ignorar (Passa os arquivos como None)
            log_callback(f"⚠ Faltando documentos. Ignorando e avançando: {nome}.")
            return doc_principal, doc_cpf
        else:
            # Cancelar -> Para o script inteiro gerando um erro amigável
            raise Exception("O processo foi cancelado pelo usuário.")