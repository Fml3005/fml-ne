import tkinter as tk
from tkinter import ttk, filedialog
import os
from pdf_processor import PDFProcessor
from gui import MainWindow

def main():
    root = tk.Tk()
    root.title("Separador de Notas de Empenho")
    
    # Maximiza a janela
    root.state('zoomed')
    root.configure(bg='#1e1e1e')
    
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()