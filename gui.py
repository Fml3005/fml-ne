import tkinter as tk
from tkinter import ttk, filedialog
import os
from pdf_processor import PDFProcessor

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.pdf_processor = PDFProcessor()
        
        # Configuração da janela principal
        self.master.geometry("600x400")
        self.master.resizable(True, True)
        
        # Criar widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botões de seleção de arquivo e pasta
        ttk.Button(main_frame, text="Selecionar PDF", command=self.select_pdf).grid(row=0, column=0, pady=5)
        ttk.Button(main_frame, text="Selecionar Pasta de Saída", command=self.select_output_folder).grid(row=1, column=0, pady=5)
        
        # Labels para mostrar caminhos selecionados
        self.pdf_path_var = tk.StringVar()
        self.output_folder_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.pdf_path_var).grid(row=0, column=1, pady=5)
        ttk.Label(main_frame, textvariable=self.output_folder_var).grid(row=1, column=1, pady=5)
        
        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate', 
                                      variable=self.progress_var)
        self.progress.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Botão de processamento
        self.process_button = ttk.Button(main_frame, text="Processar PDF", 
                                       command=self.process_pdf)
        self.process_button.grid(row=3, column=0, columnspan=2, pady=10)
        
    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_path_var.set(file_path)
    
    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_var.set(folder_path)
    
    def update_progress(self, value):
        self.progress_var.set(value)
        self.master.update_idletasks()
    
    def process_pdf(self):
        pdf_path = self.pdf_path_var.get()
        output_folder = self.output_folder_var.get()
        
        if not pdf_path or not output_folder:
            tk.messagebox.showerror("Erro", "Selecione o PDF e a pasta de saída!")
            return
        
        self.process_button.config(state='disabled')
        self.pdf_processor.process_pdf(pdf_path, output_folder, self.update_progress)
        self.process_button.config(state='normal')
        
        # Abrir pasta de saída ao finalizar
        os.startfile(output_folder)
        
        tk.messagebox.showinfo("Sucesso", "Processamento concluído!")