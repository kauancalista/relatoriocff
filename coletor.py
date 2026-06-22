from localizador import construir_cache_pasta
from aguardador import aguardar_documentos


def coletar_documentos(nomes, pasta, log_callback, modo="CPF", progresso_callback=None):
    documentos_finais = []
    total = len(nomes)

    # Cache construído uma única vez para todos os nomes
    cache_pasta = construir_cache_pasta(pasta)

    for indice, nome in enumerate(nomes, start=1):
        # Atualiza progresso se o caller forneceu um callback
        if progresso_callback:
            progresso_callback(nome, indice, total)

        doc_principal, doc_secundario = aguardar_documentos(
            nome, pasta, log_callback, modo, cache_pasta
        )

        if doc_principal:
            if "similaridade" in doc_principal["tipo"]:
                log_callback(f"⚠ Similaridade {doc_principal['similaridade']}% — {nome} → {doc_principal['arquivo']}")
            else:
                log_callback(f"✓ {nome}")
            documentos_finais.append(doc_principal["caminho"])

        if doc_secundario:
            if "similaridade" in doc_secundario["tipo"]:
                log_callback(f"⚠ Similaridade {doc_secundario['similaridade']}% — Anexo de {nome} → {doc_secundario['arquivo']}")
            else:
                log_callback(f"✓ Anexo de {nome}")
            documentos_finais.append(doc_secundario["caminho"])

    return documentos_finais
