import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

from leitor_planilha import ler_nomes
from coletor import coletar_documentos
from pdf_builder import gerar_relatorio
from conferencia import conferir_documentos
from pendencias import exportar_pendencias


class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Relatório CPF")
        self.root.geometry("1000x700")
        self.root.minsize(850, 600)

        self.planilha = ""
        self.pasta = ""
        self.saida = "Relatorio_Final.pdf"

        self.configurar_estilo()
        self.criar_interface()

    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Titulo.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground="#0D47A1"
        )

        style.configure(
            "Info.TLabel",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Custom.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

        style.configure(
            "green.Horizontal.TProgressbar",
            troughcolor="#E0E0E0",
            background="#2E7D32",
            bordercolor="#E0E0E0",
            lightcolor="#2E7D32",
            darkcolor="#2E7D32"
        )

    def criar_interface(self):
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        frame = ttk.Frame(self.root, padding=20)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_columnconfigure(1, weight=1)

        titulo = ttk.Label(
            frame,
            text="Gerador de Relatório CPF",
            style="Titulo.TLabel"
        )
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        ttk.Label(frame, text="Planilha:", style="Info.TLabel").grid(row=1, column=0, sticky="w")
        self.lbl_planilha = ttk.Label(frame, text="Nenhuma planilha selecionada")
        self.lbl_planilha.grid(row=1, column=1, sticky="ew", padx=10)
        ttk.Button(frame, text="Selecionar", style="Custom.TButton", command=self.selecionar_planilha).grid(row=1,
                                                                                                            column=2)

        ttk.Label(frame, text="Pasta dos Documentos:", style="Info.TLabel").grid(row=2, column=0, sticky="w",
                                                                                 pady=(10, 0))
        self.lbl_pasta = ttk.Label(frame, text="Nenhuma pasta selecionada")
        self.lbl_pasta.grid(row=2, column=1, sticky="ew", padx=10)
        ttk.Button(frame, text="Selecionar", style="Custom.TButton", command=self.selecionar_pasta).grid(row=2,
                                                                                                         column=2)

        ttk.Label(frame, text="Arquivo de Saída:", style="Info.TLabel").grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.lbl_saida = ttk.Label(frame, text=self.saida)
        self.lbl_saida.grid(row=3, column=1, sticky="ew", padx=10)
        ttk.Button(frame, text="Salvar Como", style="Custom.TButton", command=self.selecionar_saida).grid(row=3,
                                                                                                          column=2)

        ttk.Label(frame, text="Pessoa Atual:").grid(row=4, column=0, sticky="w", pady=(20, 0))
        self.lbl_atual = ttk.Label(frame, text="Aguardando...")
        self.lbl_atual.grid(row=4, column=1, sticky="w")

        self.progresso = ttk.Progressbar(
            frame,
            style="green.Horizontal.TProgressbar",
            mode="determinate"
        )
        self.progresso.grid(row=5, column=0, columnspan=3, sticky="ew", pady=15)

        self.log = tk.Text(
            frame,
            font=("Consolas", 10),
            bg="white",
            fg="#1A1A1A"
        )
        self.log.grid(row=6, column=0, columnspan=3, sticky="nsew")
        frame.grid_rowconfigure(6, weight=1)

        # Novo quadro para os botões da Versão 1.0
        frame_botoes = ttk.Frame(frame)
        frame_botoes.grid(row=7, column=0, columnspan=3, pady=15)

        ttk.Button(
            frame_botoes,
            text="1. Conferir Arquivos",
            style="Custom.TButton",
            command=self.thread_conferir
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            frame_botoes,
            text="2. Exportar Pendências",
            style="Custom.TButton",
            command=self.salvar_pendencias
        ).grid(row=0, column=1, padx=10)

        ttk.Button(
            frame_botoes,
            text="3. Gerar PDF Final",
            style="Custom.TButton",
            command=self.iniciar_thread
        ).grid(row=0, column=2, padx=10)

    def selecionar_planilha(self):
        arquivo = filedialog.askopenfilename(
            filetypes=[("Planilhas Excel", "*.xlsx")]
        )
        if arquivo:
            self.planilha = arquivo
            self.lbl_planilha.config(text=arquivo)

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.pasta = pasta
            self.lbl_pasta.config(text=pasta)

    def selecionar_saida(self):
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")]
        )
        if arquivo:
            self.saida = arquivo
            self.lbl_saida.config(text=arquivo)

    def escrever_log(self, texto):
        self.log.insert(tk.END, texto + "\n")
        self.log.see(tk.END)

    # ================= NOVAS FUNÇÕES DA VERSÃO 1.0 ================= #

    def thread_conferir(self):
        threading.Thread(target=self.executar_conferencia, daemon=True).start()

    def executar_conferencia(self):
        try:
            if not self.planilha:
                messagebox.showerror("Erro", "Selecione uma planilha.")
                return
            if not self.pasta:
                messagebox.showerror("Erro", "Selecione a pasta dos documentos.")
                return

            self.escrever_log("\nIniciando conferência...")
            nomes = ler_nomes(self.planilha)

            completos, pendentes = conferir_documentos(nomes, self.pasta)

            self.pendentes_atuais = pendentes

            self.escrever_log("Conferência concluída!")
            self.escrever_log(f"  ✓ Completos: {len(completos)}")
            self.escrever_log(f"  ✗ Pendentes: {len(pendentes)}")

            messagebox.showinfo(
                "Resultado da Conferência",
                f"Total de Pessoas: {len(nomes)}\n\nCompletos: {len(completos)}\nPendentes: {len(pendentes)}"
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro na conferência:\n{str(e)}")

    def salvar_pendencias(self):
        if not hasattr(self, 'pendentes_atuais'):
            messagebox.showwarning("Aviso", "Você precisa 'Conferir Arquivos' antes de exportar as pendências.")
            return

        if len(self.pendentes_atuais) == 0:
            messagebox.showinfo("Sucesso", "Não há nenhuma pendência! Todos os documentos estão corretos.")
            return

        arquivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de Texto", "*.txt")],
            initialfile="Pendencias.txt"
        )

        if arquivo:
            try:
                exportar_pendencias(self.pendentes_atuais, arquivo)
                self.escrever_log(f"\nRelatório de pendências salvo em:\n{arquivo}")
                messagebox.showinfo("Sucesso", "Relatório de pendências exportado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{str(e)}")

    # ================= FUNÇÕES ORIGINAIS DE GERAR PDF ================= #

    def iniciar_thread(self):
        threading.Thread(target=self.executar, daemon=True).start()

    def executar(self):
        try:
            if not self.planilha:
                messagebox.showerror("Erro", "Selecione uma planilha.")
                return
            if not self.pasta:
                messagebox.showerror("Erro", "Selecione uma pasta.")
                return

            self.escrever_log("Lendo planilha...")
            nomes = ler_nomes(self.planilha)
            self.progresso["maximum"] = len(nomes)
            self.escrever_log(f"{len(nomes)} nomes encontrados.")

            documentos = []
            for indice, nome in enumerate(nomes, start=1):
                self.lbl_atual.config(text=nome)
                self.progresso["value"] = indice
                self.root.update_idletasks()

                # Usa a sua função que aguarda/coleta da pasta
                docs_coletados = coletar_documentos([nome], self.pasta)
                documentos.extend(docs_coletados)

            self.escrever_log("Gerando PDF...")
            gerar_relatorio(documentos, self.saida)
            self.escrever_log("Relatório concluído.")
            self.lbl_atual.config(text="Concluído")

            messagebox.showinfo("Sucesso", "Relatório criado com sucesso.")

        except Exception as e:
            messagebox.showerror("Erro", str(e))