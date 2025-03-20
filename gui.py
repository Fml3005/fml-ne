import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pdf_processor import PDFProcessor

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.pdf_processor = PDFProcessor()
        
        # Configuração dos estilos
        self.setup_styles()
        
        # Criar container principal que centralizará todo o conteúdo
        self.create_main_container()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurações de estilo para modo escuro
        self.style.configure('Custom.TFrame', background='#1e1e1e')
        self.style.configure('Custom.TLabel', 
                           font=('Segoe UI', 10),
                           background='#1e1e1e',
                           foreground='#ffffff')
        self.style.configure('Title.TLabel',
                           font=('Segoe UI', 20, 'bold'),
                           background='#1e1e1e',
                           foreground='#ffffff')
        self.style.configure('Custom.TButton', 
                           padding=(20, 10),
                           font=('Segoe UI', 10))
        self.style.configure('Custom.Horizontal.TProgressbar',
                           troughcolor='#2d2d2d',
                           background='#007acc',
                           bordercolor='#1e1e1e')
    
    def create_main_container(self):
        # Container principal que ocupará toda a janela
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        
        # Frame central com tamanho fixo
        center_frame = ttk.Frame(self.master, style='Custom.TFrame', padding="20")
        center_frame.grid(row=0, column=0, sticky='nsew')
        
        # Configurar linhas e colunas para centralização
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_rowconfigure(2, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        
        # Frame para conteúdo com largura fixa
        content_frame = ttk.Frame(center_frame, style='Custom.TFrame')
        content_frame.grid(row=1, column=0)
        
        # Título
        title_label = ttk.Label(content_frame, 
                               text="Separador de Notas de Empenho",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 40))
        
        # Botões
        ttk.Button(content_frame,
                  text="Selecionar PDF",
                  style='Custom.TButton',
                  command=self.select_pdf).pack(pady=10)
        
        self.pdf_path_var = tk.StringVar()
        ttk.Label(content_frame,
                 textvariable=self.pdf_path_var,
                 style='Custom.TLabel').pack(pady=(0, 20))
        
        ttk.Button(content_frame,
                  text="Selecionar Pasta de Saída",
                  style='Custom.TButton',
                  command=self.select_output_folder).pack(pady=10)
        
        self.output_folder_var = tk.StringVar()
        ttk.Label(content_frame,
                 textvariable=self.output_folder_var,
                 style='Custom.TLabel').pack(pady=(0, 30))
        
        # Barra de progresso
        progress_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        progress_frame.pack(pady=20, fill='x')
        
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(progress_frame,
                                      length=400,
                                      mode='determinate',
                                      style='Custom.Horizontal.TProgressbar',
                                      variable=self.progress_var)
        self.progress.pack(fill='x')
        
        self.progress_label = ttk.Label(progress_frame,
                                      text="0%",
                                      style='Custom.TLabel')
        self.progress_label.pack(pady=(5, 0))
        
        # Botão de processamento
        self.process_button = ttk.Button(content_frame,
                                       text="Processar PDF",
                                       style='Custom.TButton',
                                       command=self.process_pdf)
        self.process_button.pack(pady=30)

    def update_progress(self, value):
        self.progress_var.set(value)
        self.progress_label.config(text=f"{int(value)}%")
        self.master.update_idletasks()

    def select_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_path_var.set(file_path)
    
    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_var.set(folder_path)
    
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