import os
import tempfile
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter


def imagem_para_pdf(imagem_path):
    # (Mantenha seu código intacto aqui)
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_pdf.name, pagesize=A4)
    largura_a4, altura_a4 = A4
    imagem = Image.open(imagem_path)
    largura_img, altura_img = imagem.size
    proporcao = min(largura_a4 / largura_img, altura_a4 / altura_img)
    nova_largura = largura_img * proporcao
    nova_altura = altura_img * proporcao
    x = (largura_a4 - nova_largura) / 2
    y = (altura_a4 - nova_altura) / 2
    c.drawImage(imagem_path, x, y, width=nova_largura, height=nova_altura)
    c.showPage()
    c.save()
    return temp_pdf.name


def gerar_relatorio(documentos, saida_pdf):
    writer = PdfWriter()
    temporarios = []

    try:
        for arquivo in documentos:
            # ---> ALTERAÇÃO AQUI: Ignora arquivos ausentes/None
            if not arquivo or not os.path.exists(arquivo):
                continue

            extensao = os.path.splitext(arquivo)[1].lower()
            pdf_utilizado = arquivo
            if extensao in [".jpg", ".jpeg", ".png"]:
                pdf_utilizado = imagem_para_pdf(arquivo)
                temporarios.append(pdf_utilizado)

            reader = PdfReader(pdf_utilizado)
            for pagina in reader.pages:
                writer.add_page(pagina)

        with open(saida_pdf, "wb") as arquivo_saida:
            writer.write(arquivo_saida)

    finally:
        for temp in temporarios:
            try:
                os.remove(temp)
            except:
                pass