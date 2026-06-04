import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

from leitor_planilha import ler_nomes
from coletor import coletar_documentos
from pdf_builder import gerar_relatorio
from conferencia import conferir_documentos
from pendencias import exportar_pendencias
from importador import importar_arquivos

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class Aplicacao:
    def __init__(self, root):
        self.root = root
        # NOME ATUALIZADO NA BARRA DA JANELA
        self.root.title("Gerador de Relatórios - Versão 2.0 (PRO)")
        self.root.geometry("1050x750")
        self.root.minsize(950, 700)

        # Ícone ativado
        self.root.iconbitmap("icone.ico")

        self.planilha = ""
        self.pasta = ""
        self.saida = "Relatorio_Final.pdf"
        self.import_origem = ""
        self.import_destino = ""

        self.criar_interface()

    def criar_interface(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_rowconfigure(7, weight=1)  # Aumentado para 7 devido à nova linha

        # NOME ATUALIZADO NO TÍTULO AZUL PRINCIPAL
        titulo = ctk.CTkLabel(frame, text="Gerador de Relatórios", font=("Segoe UI", 26, "bold"),
                              text_color="#3498db")
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 30))

        ctk.CTkLabel(frame, text="Planilha Base:", font=("Segoe UI", 15)).grid(row=1, column=0, sticky="w")
        self.lbl_planilha = ctk.CTkLabel(frame, text="Nenhuma selecionada", text_color="gray")
        self.lbl_planilha.grid(row=1, column=1, sticky="ew", padx=15)
        ctk.CTkButton(frame, text="Selecionar", font=("Segoe UI", 13, "bold"), command=self.selecionar_planilha,
                      width=130).grid(row=1, column=2, pady=8)

        ctk.CTkLabel(frame, text="Pasta Documentos:", font=("Segoe UI", 15)).grid(row=2, column=0, sticky="w")
        self.lbl_pasta = ctk.CTkLabel(frame, text="Nenhuma selecionada", text_color="gray")
        self.lbl_pasta.grid(row=2, column=1, sticky="ew", padx=15)
        ctk.CTkButton(frame, text="Selecionar", font=("Segoe UI", 13, "bold"), command=self.selecionar_pasta,
                      width=130).grid(row=2, column=2, pady=8)

        ctk.CTkLabel(frame, text="Arquivo de Saída:", font=("Segoe UI", 15)).grid(row=3, column=0, sticky="w")
        self.lbl_saida = ctk.CTkLabel(frame, text=self.saida, text_color="gray")
        self.lbl_saida.grid(row=3, column=1, sticky="ew", padx=15)
        ctk.CTkButton(frame, text="Salvar Como", font=("Segoe UI", 13, "bold"), command=self.selecionar_saida,
                      width=130).grid(row=3, column=2, pady=8)

        # ---- NOVO: SELETOR DE MODO ----
        ctk.CTkLabel(frame, text="Tipo de Relatório:", font=("Segoe UI", 15, "bold")).grid(row=4, column=0, sticky="w",
                                                                                           pady=10)
        self.combo_modo = ctk.CTkComboBox(frame, values=["CPF", "CERTIDAO"], state="readonly", font=("Segoe UI", 14))
        self.combo_modo.grid(row=4, column=1, sticky="w", padx=15, pady=10)
        self.combo_modo.set("CPF")  # Padrão

        ctk.CTkLabel(frame, text="Processando Atual:", font=("Segoe UI", 15)).grid(row=5, column=0, sticky="w",
                                                                                   pady=(15, 0))
        self.lbl_atual = ctk.CTkLabel(frame, text="Aguardando...", font=("Segoe UI", 16, "bold"), text_color="#f39c12")
        self.lbl_atual.grid(row=5, column=1, sticky="w", pady=(15, 0))

        self.progresso = ctk.CTkProgressBar(frame, progress_color="#2ecc71", height=12)
        self.progresso.grid(row=6, column=0, columnspan=3, sticky="ew", pady=20)
        self.progresso.set(0)

        self.log = ctk.CTkTextbox(frame, font=("Consolas", 13), fg_color="#1E1E1E", text_color="#A9CCE3")
        self.log.grid(row=7, column=0, columnspan=3, sticky="nsew", pady=(0, 20))

        frame_botoes = ctk.CTkFrame(frame, fg_color="transparent")
        frame_botoes.grid(row=8, column=0, columnspan=3, pady=(10, 0))

        ctk.CTkButton(frame_botoes, text="📥 1. Coletar", command=self.abrir_tela_importacao,
                      font=("Segoe UI", 14, "bold")).grid(row=0, column=0, padx=10)
        ctk.CTkButton(frame_botoes, text="🔍 2. Conferir", command=self.thread_conferir,
                      font=("Segoe UI", 14, "bold")).grid(row=0, column=1, padx=10)
        ctk.CTkButton(frame_botoes, text="📋 3. Pendências", command=self.salvar_pendencias,
                      font=("Segoe UI", 14, "bold"), fg_color="#d35400", hover_color="#e67e22").grid(row=0, column=2,
                                                                                                     padx=10)
        ctk.CTkButton(frame_botoes, text="📄 4. Gerar PDF", command=self.iniciar_thread, font=("Segoe UI", 14, "bold"),
                      fg_color="#27ae60", hover_color="#2ecc71").grid(row=0, column=3, padx=10)

    # --- SELETORES ---
    def selecionar_planilha(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Planilhas Excel", "*.xlsx")])
        if arquivo:
            self.planilha = arquivo
            self.lbl_planilha.configure(text=arquivo, text_color="white")

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.pasta = pasta
            self.lbl_pasta.configure(text=pasta, text_color="white")

    def selecionar_saida(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if arquivo:
            self.saida = arquivo
            self.lbl_saida.configure(text=arquivo, text_color="white")

    def escrever_log(self, texto):
        self.log.insert(tk.END, texto + "\n")
        self.log.see(tk.END)

    # --- LÓGICA ATUALIZADA COM O 'MODO' ---
    def thread_conferir(self):
        threading.Thread(target=self.executar_conferencia, daemon=True).start()

    def executar_conferencia(self):
        try:
            if not self.planilha or not self.pasta:
                messagebox.showerror("Erro", "Selecione a planilha e a pasta principal.")
                return

            modo_selecionado = self.combo_modo.get()
            self.escrever_log(f"\n--- INICIANDO CONFERÊNCIA ({modo_selecionado}) ---")

            nomes = ler_nomes(self.planilha)
            completos, pendentes = conferir_documentos(nomes, self.pasta, modo_selecionado)

            self.pendentes_atuais = pendentes

            self.escrever_log("Conferência concluída!")
            self.escrever_log(f" ✓ Completos: {len(completos)}")
            self.escrever_log(f" ✗ Pendentes: {len(pendentes)}")

            messagebox.showinfo("Resultado",
                                f"Total: {len(nomes)}\nCompletos: {len(completos)}\nPendentes: {len(pendentes)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na conferência:\n{str(e)}")

    def salvar_pendencias(self):
        if not hasattr(self, 'pendentes_atuais'):
            messagebox.showwarning("Aviso", "Você precisa clicar em '2. Conferir' antes.")
            return

        if len(self.pendentes_atuais) == 0:
            messagebox.showinfo("Sucesso", "Nenhuma pendência!")
            return

        arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de Texto", "*.txt")],
                                               initialfile="Pendencias.txt")
        if arquivo:
            try:
                exportar_pendencias(self.pendentes_atuais, arquivo)
                self.escrever_log(f"\nPendências salvas em: {arquivo}")
                messagebox.showinfo("Sucesso", "Arquivo exportado!")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def iniciar_thread(self):
        threading.Thread(target=self.executar, daemon=True).start()

    def executar(self):
        try:
            if not self.planilha or not self.pasta:
                messagebox.showerror("Erro", "Selecione planilha e pasta principal.")
                return

            modo_selecionado = self.combo_modo.get()
            self.escrever_log(f"\n--- GERANDO RELATÓRIO ({modo_selecionado}) ---")

            nomes = ler_nomes(self.planilha)
            total_nomes = len(nomes)

            documentos = []
            for indice, nome in enumerate(nomes, start=1):
                self.lbl_atual.configure(text=nome, text_color="#f39c12")
                self.progresso.set(indice / total_nomes)
                self.root.update_idletasks()

                # Passa o modo (CPF ou CERTIDAO) para o coletor
                docs_coletados = coletar_documentos([nome], self.pasta, self.escrever_log, modo_selecionado)
                documentos.extend(docs_coletados)

            self.escrever_log("\nGerando PDF...")
            gerar_relatorio(documentos, self.saida)
            self.escrever_log("Concluído.")
            self.lbl_atual.configure(text="✔ PDF Gerado com Sucesso!", text_color="#2ecc71")

            messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!")

        except Exception as e:
            self.escrever_log(f"\n❌ Parado: {str(e)}")
            self.lbl_atual.configure(text="Processo Cancelado", text_color="#e74c3c")
            messagebox.showwarning("Aviso", str(e))

    # --- TELA SECUNDÁRIA (IMPORTAÇÃO MANTIDA IGUAL) ---
    def abrir_tela_importacao(self):
        janela = ctk.CTkToplevel(self.root)
        janela.title("Ferramenta - Coletar Arquivos")
        janela.geometry("700x250")
        janela.transient(self.root)
        janela.grab_set()

        frame = ctk.CTkFrame(janela)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame, text="Origem (Scanner):", font=("Segoe UI", 14)).grid(row=0, column=0, sticky="w",
                                                                                  pady=(15, 10))
        lbl_origem = ctk.CTkLabel(frame, text=self.import_origem if self.import_origem else "Nenhuma selecionada",
                                  text_color="gray")
        lbl_origem.grid(row=0, column=1, sticky="ew", padx=10, pady=(15, 10))
        ctk.CTkButton(frame, text="Selecionar", command=lambda: self.selec_imp_origem(lbl_origem), width=100).grid(
            row=0, column=2, pady=(15, 10))

        ctk.CTkLabel(frame, text="Destino:", font=("Segoe UI", 14)).grid(row=1, column=0, sticky="w", pady=(10, 20))
        lbl_destino = ctk.CTkLabel(frame, text=self.import_destino if self.import_destino else "Nenhuma selecionada",
                                   text_color="gray")
        lbl_destino.grid(row=1, column=1, sticky="ew", padx=10, pady=(10, 20))
        ctk.CTkButton(frame, text="Selecionar", command=lambda: self.selec_imp_destino(lbl_destino), width=100).grid(
            row=1, column=2, pady=(10, 20))

        ctk.CTkButton(frame, text="🚀 INICIAR CÓPIA", command=self.thread_importacao, font=("Segoe UI", 14, "bold"),
                      fg_color="#8e44ad", hover_color="#9b59b6").grid(row=2, column=0, columnspan=3, pady=10)

    def selec_imp_origem(self, lbl):
        pasta = filedialog.askdirectory()
        if pasta:
            self.import_origem = pasta
            lbl.configure(text=pasta, text_color="white")

    def selec_imp_destino(self, lbl):
        pasta = filedialog.askdirectory()
        if pasta:
            self.import_destino = pasta
            lbl.configure(text=pasta, text_color="white")

    def thread_importacao(self):
        threading.Thread(target=self.executar_importacao, daemon=True).start()

    def executar_importacao(self):
        if not self.import_origem or not self.import_destino:
            messagebox.showerror("Erro", "Selecione as pastas de Origem e Destino.")
            return

        try:
            self.escrever_log("\n--- COLETANDO ARQUIVOS ---")
            copiados, _ = importar_arquivos(self.import_origem, self.import_destino)

            if not copiados:
                self.escrever_log("Nenhum arquivo encontrado na origem.")
                messagebox.showinfo("Aviso", "A pasta do scanner está vazia.")
                return

            for arq in copiados:
                self.escrever_log(f" ✓ Copiado: {arq}")

            self.escrever_log(f"Total importado: {len(copiados)} arquivo(s).")
            messagebox.showinfo("Coleta Concluída", f"{len(copiados)} arquivos copiados!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao coletar:\n{str(e)}")