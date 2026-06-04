from aguardador import aguardar_documentos


def coletar_documentos(nomes, pasta, log_callback, modo="CPF"):
    documentos_finais = []

    for nome in nomes:
        doc_principal, doc_secundario = aguardar_documentos(nome, pasta, log_callback, modo)

        # --- LOG PARA O DOCUMENTO PRINCIPAL ---
        if doc_principal:
            if doc_principal["tipo"].startswith("Similaridade"):
                log_callback(
                    f"\n⚠ Correspondência por similaridade\nPlanilha: {nome}\nArquivo: {doc_principal['arquivo']}\nSimilaridade: {doc_principal['similaridade']}%\n")
            else:
                log_callback(f"✓ Encontrado: {nome} ({doc_principal['tipo']})")
            documentos_finais.append(doc_principal["caminho"])

        # --- LOG PARA O SECUNDÁRIO ---
        if doc_secundario:
            if doc_secundario["tipo"].startswith("Similaridade"):
                log_callback(
                    f"\n⚠ Correspondência por similaridade\nPlanilha: {nome} (Anexo)\nArquivo: {doc_secundario['arquivo']}\nSimilaridade: {doc_secundario['similaridade']}%\n")
            else:
                log_callback(f"✓ Encontrado: Anexo de {nome} ({doc_secundario['tipo']})")
            documentos_finais.append(doc_secundario["caminho"])

    return documentos_finais