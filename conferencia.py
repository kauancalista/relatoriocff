from localizador import localizar_documento


def conferir_documentos(nomes, pasta):
    completos = []
    pendentes = []

    for nome in nomes:
        doc = localizar_documento(nome, pasta)

        # Trata o casamento para o CPF também na conferência
        if " E " in nome.upper():
            nome_limpo = nome.upper().split(" E ")[0].strip()
        else:
            nome_limpo = nome

        cpf = localizar_documento(f"{nome_limpo} CPF", pasta)

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