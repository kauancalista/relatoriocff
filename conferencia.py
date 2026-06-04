from localizador import localizar_documento


def conferir_documentos(nomes, pasta, modo="CPF"):
    completos = []
    pendentes = []

    for nome in nomes:
        doc = localizar_documento(nome, pasta)

        nome_upper = nome.upper()
        if " E " in nome_upper:
            nome_limpo = nome_upper.split(" E ")[0].strip()
        else:
            nome_limpo = nome_upper

        doc_secundario = None

        if modo == "CPF":
            doc_secundario = localizar_documento(f"{nome_limpo} CPF", pasta)
        elif modo == "CERTIDAO":
            sufixos = [" + FERC", " + CRAS", " + REGISTRE-SE", " FERC", " CRAS", " REGISTRE-SE"]
            for sufixo in sufixos:
                doc_secundario = localizar_documento(f"{nome_limpo}{sufixo}", pasta)
                if doc_secundario:
                    break

        if doc and doc_secundario:
            completos.append(nome)
        else:
            pendente = {
                "nome": nome,
                "documento": bool(doc),
                "anexo": bool(doc_secundario)
            }
            pendentes.append(pendente)

    return completos, pendentes