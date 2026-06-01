from aguardador import aguardar_documentos


def coletar_documentos(nomes, pasta):
    """
    Retorna todos os documentos
    na ordem correta para o PDF final.
    """

    documentos = []

    total = len(nomes)

    for indice, nome in enumerate(nomes, start=1):

        print("\n========================")
        print(f"{indice}/{total}")
        print(nome)

        doc_principal, doc_cpf = aguardar_documentos(
            nome,
            pasta
        )

        documentos.append(doc_principal)
        documentos.append(doc_cpf)

        print("✓ Adicionado à fila")

    return documentos