import time
from localizador import localizar_documento


def aguardar_documentos(nome, pasta):
    """
    Aguarda até encontrar:
    - NOME
    - NOME CPF
    """

    while True:

        doc_principal = localizar_documento(nome, pasta)

        doc_cpf = localizar_documento(
            f"{nome} CPF",
            pasta
        )

        if doc_principal and doc_cpf:
            return doc_principal, doc_cpf

        print("\n-----------------------------")
        print(f"Pessoa: {nome}")

        if doc_principal:
            print("✓ Documento principal")
        else:
            print("✗ Documento principal")

        if doc_cpf:
            print("✓ Documento CPF")
        else:
            print("✗ Documento CPF")

        print("\nAguardando arquivos...")
        time.sleep(3)