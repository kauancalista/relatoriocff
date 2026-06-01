from localizador import localizar_documento

def conferir_documentos(nomes, pasta):
    completos = []
    pendentes = []

    for nome in nomes:
        doc = localizar_documento(nome, pasta)
        cpf = localizar_documento(f"{nome} CPF", pasta)

        if doc and cpf:
            completos.append(nome)
        else:
            pendente = {
                "nome": nome,
                "documento": bool(doc),
                "cpf": bool(cpf)
            }
            pendentes.append(pendente)

    return completos, pendentes