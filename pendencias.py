def exportar_pendencias(pendentes, caminho_saida):
    with open(caminho_saida, "w", encoding="utf-8") as arquivo:
        arquivo.write("RELATÓRIO DE PENDÊNCIAS\n\n")

        for item in pendentes:
            arquivo.write(f"{item['nome']}\n")

            if not item["documento"]:
                arquivo.write("- Documento Principal\n")

            if not item["cpf"]:
                arquivo.write("- CPF\n")

            arquivo.write("\n")