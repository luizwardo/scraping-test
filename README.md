# Nota sobre o desenvolvimento da solução técnica

Este código foi desenvolvido como solução para o desafio técnico da AIAx, implementando um pipeline completo de processamento de dados com as seguintes etapas:

1. **Scraping web** - Extração da imagem da página alvo, com suporte para imagens convencionais e formatos base64 embutidos
2. **Validação** - Verificação da integridade da imagem baixada antes do processamento
3. **Processamento via IA** - Envio da imagem para o modelo Florence 2 para análise e geração de legendas detalhadas
4. **Submissão** - Entrega dos resultados para validação

A implementação inclui tratamento de erros robusto e logs detalhados em cada etapa do processo para facilitar a depuração, garantindo que o pipeline funcione corretamente mesmo com diferentes formatos de entrada.
