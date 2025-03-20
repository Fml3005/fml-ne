# Separador de Notas de Empenho

## Descrição
Aplicação desktop desenvolvida para automatizar o processo de separação de documentos PDF contendo múltiplas Notas de Empenho. O programa identifica e separa automaticamente cada nota em arquivos individuais.

## Funcionalidades
- Interface gráfica moderna e intuitiva
- Processamento automático de PDFs
- Separação inteligente de documentos
- Numeração automática com formato padronizado (NE0000000123)
- Barra de progresso em tempo real
- Seleção simplificada de arquivos e pastas
- Abertura automática da pasta de destino após processamento

## Como Usar
1. Execute o aplicativo "Separador_NE.exe"
2. Clique em "Selecionar PDF" para escolher o arquivo PDF que contém as notas
3. Clique em "Selecionar Pasta de Saída" para definir onde os arquivos serão salvos
4. Clique em "Processar PDF" para iniciar a separação
5. Aguarde o processamento (acompanhe pela barra de progresso)
6. A pasta de destino abrirá automaticamente ao finalizar

## Formato dos Arquivos
- Os arquivos de saída seguem o padrão: NE0000000123.pdf
- Números são preenchidos com zeros à esquerda até completar 10 dígitos
- Em caso de múltiplas notas com mesmo número, um sufixo é adicionado (_1, _2, etc.)

## Requisitos do Sistema
- Sistema Operacional: Windows
- Não requer instalação de software adicional
- Não requer Python instalado

## Processamento
O programa:
1. Analisa cada página do PDF
2. Identifica números de empenho
3. Agrupa páginas relacionadas
4. Gera arquivos individuais
5. Mantém notas de liquidação junto com seus empenhos

## Observações
- A aplicação funciona melhor com PDFs legíveis e bem formatados
- O processo é totalmente automático após a seleção dos arquivos
- Interface em modo escuro para melhor experiência visual