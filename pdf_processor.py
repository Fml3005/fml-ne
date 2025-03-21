import fitz  # PyMuPDF
import re
import os
import tkinter as tk
from tkinter import filedialog
import logging

class PDFProcessor:
    def __init__(self):
        self.current_progress = 0
        self.total_pages = 0
        
        # Configuração do log
        logging.basicConfig(
            level=logging.DEBUG,  # Nível de log: DEBUG, INFO, WARNING, ERROR, CRITICAL
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.StreamHandler(), 
                logging.FileHandler("processamento_pdf.log", mode="w", encoding="utf-8")  # Define a codificação UTF-8
            ]
        )
        self.logger = logging.getLogger()

    def format_empenho_number(self, number):
        """Remove os zeros à esquerda do número do empenho e adiciona o prefixo NE"""
        return f"NE{int(number)}"
    
    def process_pdf(self, pdf_path, output_folder, progress_callback=None):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        self.logger.info(f"Iniciando o processamento do PDF: {pdf_path}")
            
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            self.logger.error(f"Erro ao abrir o arquivo PDF {pdf_path}: {e}")
            return
        
        self.total_pages = len(doc)
        current_pages = []
        last_empenho_number = None
        file_counter = {}
        numeros_repetidos = {}  # Dicionário para controlar as repetições de empenho
        
        self.logger.info(f"Total de páginas no PDF: {self.total_pages}")
        
        for page_num, page in enumerate(doc):
            text = page.get_text("text")
            self.logger.debug(f"Processando página {page_num + 1}/{self.total_pages}")
            
            if progress_callback:
                progress = (page_num + 1) / self.total_pages * 100
                progress_callback(progress)
            
            # Ignora páginas em branco
            if not text.strip():
                self.logger.debug(f"Página {page_num + 1} ignorada (em branco)")
                current_pages.append(page_num)
                continue
            
            # Ignora páginas de NOTA DE LIQUIDAÇÃO
            has_liquidacao = "NOTA DE LIQUIDAÇÃO" in text or "NOTA DE LIQ" in text
            if has_liquidacao:
                self.logger.debug(f"Página {page_num + 1} ignorada (Nota de Liquidação detectada)")
                current_pages.append(page_num)
                continue
            
            # Regex para capturar o número da nota de empenho
            match = re.search(r"NOTA DE EMPENHO\s*(Nº|N|N°|N0|Nu|N2|N9|Na|Ne|W|Ng)\s*(\d{3,10})", text)
            if match:
                empenho_number = match.group(2)
                self.logger.info(f"Nota de Empenho detectada na página {page_num + 1}: {empenho_number}")
                
                # Verifica se já houve uma repetição do número de empenho
                if empenho_number in numeros_repetidos:
                    numeros_repetidos[empenho_number] += 1
                else:
                    numeros_repetidos[empenho_number] = 1
                
                # Salva as páginas anteriores com o número de empenho anterior
                if current_pages and last_empenho_number:
                    self._save_pdf(doc, current_pages, last_empenho_number, file_counter, output_folder, numeros_repetidos)
                
                # Reinicia a lista de páginas
                current_pages = [page_num]
                last_empenho_number = empenho_number
            else:
                current_pages.append(page_num)
        
        # Salva as páginas restantes
        if current_pages and last_empenho_number:
            self._save_pdf(doc, current_pages, last_empenho_number, file_counter, output_folder, numeros_repetidos)
    
    def _save_pdf(self, doc, pages, empenho_number, file_counter, output_folder, numeros_repetidos):
        formatted_number = self.format_empenho_number(empenho_number)
        repetition_index = numeros_repetidos[empenho_number]
        
        # Nome do arquivo com o sufixo correto
        output_filename = os.path.join(output_folder, f"{formatted_number}.pdf")
        
        # Verifica se o arquivo já existe e incrementa o sufixo, se necessário
        while os.path.exists(output_filename):
            repetition_index += 1
            output_filename = os.path.join(output_folder, f"{formatted_number}_{repetition_index}.pdf")
        
        try:
            # Cria o novo PDF com as páginas corretas
            new_doc = fitz.open()
            for page_num in pages:
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
            
            new_doc.save(output_filename)
            new_doc.close()
            self.logger.info(f"Arquivo salvo com sucesso: {output_filename}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar o arquivo {output_filename}: {e}")

# Função para selecionar o arquivo PDF
def selecionar_arquivo_pdf():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    pdf_path = filedialog.askopenfilename(
        title="Selecione o arquivo PDF",
        filetypes=[("Arquivos PDF", "*.pdf")]
    )
    return pdf_path

# Função para selecionar a pasta de saída
def selecionar_pasta_saida():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    pasta_saida = filedialog.askdirectory(
        title="Selecione a pasta de saída"
    )
    return pasta_saida

# Função principal para executar o processo
def main():
    pdf_path = selecionar_arquivo_pdf()  # Seleciona o arquivo PDF
    if not pdf_path:
        print("Nenhum arquivo PDF selecionado. O programa será encerrado.")
        return

    pasta_saida = selecionar_pasta_saida()  # Seleciona a pasta de saída
    if not pasta_saida:
        print("Nenhuma pasta de saída selecionada. O programa será encerrado.")
        return

    # Cria o processador e inicia o processamento
    processor = PDFProcessor()
    processor.process_pdf(pdf_path, pasta_saida)

# Chama a função principal
if __name__ == "__main__":
    main()