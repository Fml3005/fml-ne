import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["tkinter", "pdfplumber", "PyPDF2"],
    "includes": ["re", "os"],
    "include_files": []
}

setup(
    name="Separador de Notas de Empenho",
    version="1.0",
    description="Separador de Notas de Empenho PDF",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base="Win32GUI",
            icon="icon.ico",  # Se você tiver um ícone
            target_name="Separador_NE.exe"
        )
    ]
)