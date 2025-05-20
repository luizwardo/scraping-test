# Image Scraper & AI Description Generator

## Descrição
Este projeto é uma aplicação desktop Python que permite extrair imagens de páginas web e gerar automaticamente descrições para elas usando a API de visão da OpenAI. A ferramenta oferece uma interface gráfica amigável para facilitar o processo de scraping de imagens e análise de conteúdo visual.

## Funcionalidades

- **Extração de imagens** de qualquer URL acessível publicamente
- **Suporte para diferentes formatos de imagem** (URLs absolutas, relativas, e formatos base64)
- **Processamento em paralelo** para não bloquear a interface
- **Geração automática de descrições** usando modelos de IA de visão computacional
- **Visualização em tempo real** do progresso e logs
- **Armazenamento local** das imagens baixadas e suas descrições
- **Exportação de resultados** em formato JSON para uso posterior


## Requisitos

- Python 3.7+
- Bibliotecas necessárias:
  - requests
  - beautifulsoup4
  - pillow (PIL)
  - tkinter (normalmente incluído com o Python)
- Uma API key da OpenAI com acesso aos modelos de visão

**Nota**: Este projeto foi desenvolvido para fins educacionais. Certifique-se de respeitar os termos de serviço dos sites de onde você extrai imagens e os termos de uso da API da OpenAI.
