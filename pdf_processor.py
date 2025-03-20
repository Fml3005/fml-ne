import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
import re
import os

class PDFProcessor:
    def __init__(self):
        self.current_progress = 0
        self.total_pages = 0
    
    def format_empenho_number(self, number):
        """Formata o número do empenho para ter 10 dígitos"""
        return f"NE{number.zfill(10)}"
    
    def process_pdf(self, pdf_path, output_folder, progress_callback=None):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        with pdfplumber.open(pdf_path) as pdf:
            pdf_reader = PdfReader(pdf_path)
            self.total_pages = len(pdf.pages)
            current_pages = []
            last_empenho_number = None
            file_counter = {}
            
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                
                if progress_callback:
                    progress = (page_num + 1) / self.total_pages * 100
                    progress_callback(progress)
                
                if not text:
                    current_pages.append(page_num)
                    continue
                
                has_liquidacao = "NOTA DE LIQUIDAÇÃO" in text or "NOTA DE LIQ" in text
                if has_liquidacao:
                    current_pages.append(page_num)
                    continue
                
                match = re.search(r"NOTA DE EMPENHO\s*(Nº|N|N°|N0|Nu|N2|N9|Na|Ne|W|Ng)\s*(\d+)", text)
                if match:
                    empenho_number = match.group(2)
                    
                    if current_pages and last_empenho_number:
                        self._save_pdf(pdf_reader, current_pages, last_empenho_number, 
                                     file_counter, output_folder)
                    
                    current_pages = [page_num]
                    last_empenho_number = empenho_number
                else:
                    current_pages.append(page_num)
            
            if current_pages and last_empenho_number:
                self._save_pdf(pdf_reader, current_pages, last_empenho_number, 
                             file_counter, output_folder)
    
    def _save_pdf(self, pdf_reader, pages, empenho_number, file_counter, output_folder):
        file_counter[empenho_number] = file_counter.get(empenho_number, 0) + 1
        counter_suffix = f"_{file_counter[empenho_number]}" if file_counter[empenho_number] > 1 else ""
        
        formatted_number = self.format_empenho_number(empenho_number)
        output_file = f"{output_folder}/{formatted_number}{counter_suffix}.pdf"
        
        pdf_writer = PdfWriter()
        for p in pages:
            pdf_writer.add_page(pdf_reader.pages[p])
            
        with open(output_file, "wb") as out:
            pdf_writer.write(out)