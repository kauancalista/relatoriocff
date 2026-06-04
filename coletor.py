from aguardador import aguardar_documentos


def coletar_documentos(nomes, pasta, log_callback):
    documentos_finais = []

    for nome in nomes:
        # Pede para o aguardador buscar (e perguntar ao usuário se faltar)
        doc_principal, doc_cpf = aguardar_documentos(nome, pasta, log_callback)

        # --- LOG PARA O DOCUMENTO PRINCIPAL ---
        if doc_principal:
            if doc_principal["tipo"] == "Similaridade":
                log_callback(
                    f"\n⚠ Correspondência por similaridade\nPlanilha: {nome}\nArquivo: {doc_principal['arquivo']}\nSimilaridade: {doc_principal['similaridade']}%\n")
            else:
                log_callback(f"✓ Encontrado: {nome} ({doc_principal['tipo']})")

            documentos_finais.append(doc_principal["caminho"])

        # --- LOG PARA O CPF ---
        if doc_cpf:
            if doc_cpf["tipo"] == "Similaridade":
                log_callback(
                    f"\n⚠ Correspondência por similaridade\nPlanilha: {nome} CPF\nArquivo: {doc_cpf['arquivo']}\nSimilaridade: {doc_cpf['similaridade']}%\n")
            else:
                log_callback(f"✓ Encontrado: CPF de {nome} ({doc_cpf['tipo']})")

            documentos_finais.append(doc_cpf["caminho"])

    return documentos_finais