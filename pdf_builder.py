import os
import tempfile
from PIL import Image, ImageOps
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter


def imagem_para_pdf(imagem_path):
    # Cria apenas o ficheiro temporário para o PDF (não precisamos mais de temp de imagem)
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    # 1. Abre a imagem original
    with Image.open(imagem_path) as img:
        # Corrige imagens deitadas ou de pernas para o ar (scanners ou telemóveis)
        img = ImageOps.exif_transpose(img)

        # 2. A CONVERSÃO DEFINITIVA (Fim das imagens pretas)
        # Se tiver transparência (RGBA, LA) ou paleta com máscara, cria fundo branco
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            fundo_branco = Image.new('RGB', img.size, (255, 255, 255))
            fundo_branco.paste(img, mask=img.convert('RGBA').split()[3])
            img = fundo_branco
        # Qualquer outro formato bizarro (CMYK, Grayscale, etc), força para RGB puro
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # 3. O TRUQUE DE MESTRE: Coloca a imagem tratada na Memória RAM
        # O ReportLab vai ler daqui, sem o Windows bloquear o ficheiro!
        img_reader = ImageReader(img)

        # 4. Matemática e Desenho do PDF
        c = canvas.Canvas(temp_pdf.name, pagesize=A4)
        largura_a4, altura_a4 = A4
        largura_img, altura_img = img.size

        proporcao = min(largura_a4 / largura_img, altura_a4 / altura_img)
        nova_largura = largura_img * proporcao
        nova_altura = altura_img * proporcao

        x = (largura_a4 - nova_largura) / 2
        y = (altura_a4 - nova_altura) / 2

        c.drawImage(img_reader, x, y, width=nova_largura, height=nova_altura)
        c.showPage()
        c.save()

    return temp_pdf.name


def gerar_relatorio(documentos, saida_pdf):
    writer = PdfWriter()
    temporarios = []

    try:
        for arquivo in documentos:
            if not arquivo or not os.path.exists(arquivo):
                continue

            extensao = os.path.splitext(arquivo)[1].lower()
            pdf_utilizado = arquivo

            # Se for imagem, faz a conversão pela memória RAM
            if extensao in [".jpg", ".jpeg", ".png"]:
                pdf_utilizado = imagem_para_pdf(arquivo)
                temporarios.append(pdf_utilizado)

            # Lê o PDF (original ou convertido) e junta ao relatório final
            reader = PdfReader(pdf_utilizado)
            for pagina in reader.pages:
                writer.add_page(pagina)

        if len(writer.pages) > 0:
            with open(saida_pdf, "wb") as arquivo_saida:
                writer.write(arquivo_saida)
        else:
            raise Exception("Nenhum documento processado. Relatório vazio.")

    finally:
        # Garante que os ficheiros temporários do PDF são apagados do PC
        for temp in temporarios:
            if temp and os.path.exists(temp):
                try:
                    os.remove(temp)
                except:
                    pass