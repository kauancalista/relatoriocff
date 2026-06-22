def exportar_pendencias(pendentes, caminho_saida):
    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write("RELATÓRIO DE PENDÊNCIAS\n\n")

        for item in pendentes:
            arquivo.write(f"{item['nome']}\n")

            if not item["documento"]:
                arquivo.write("  - Documento Principal\n")

            # CORRIGIDO: era item["cpf"], que não existe no dicionário.
            # A chave correta montada em conferencia.py é "anexo".
            if not item["anexo"]:
                # Exibe o rótulo certo dependendo do modo salvo no item
                modo = item.get("modo", "CPF")
                if modo == "CERTIDAO":
                    arquivo.write("  - Anexo (FERC / CRAS / REGISTRE-SE)\n")
                else:
                    arquivo.write("  - CPF\n")

            arquivo.write("\n")
