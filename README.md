# Contador de Microalgas

Um software para análise e contagem automática de microalgas em imagens microscópicas.

## Funcionalidades

- Interface gráfica moderna e intuitiva
- Detecção automática de microalgas usando processamento de imagem
- Ajuste de parâmetros de detecção em tempo real
- Visualização lado a lado da imagem original e processada
- Contagem automática com numeração das microalgas
- Cálculo de estatísticas (total, tamanho médio, densidade)
- Exportação de resultados em múltiplos formatos
- Salvamento de configurações de detecção

## Requisitos

- Python 3.8 ou superior
- OpenCV
- NumPy
- Pillow
- ttkthemes

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/contador-microalgas.git
cd contador-microalgas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

1. Execute o programa:
```bash
python main.py
```

2. Use a interface para:
   - Carregar imagens de microalgas
   - Ajustar parâmetros de detecção
   - Processar imagens e contar microalgas
   - Exportar resultados

## Parâmetros de Detecção

- **Distância Mínima**: Distância mínima em pixels entre microalgas detectadas
- **Sensibilidade**: Sensibilidade na detecção de bordas (maior = mais sensível)
- **Acurácia**: Precisão na detecção de círculos (maior = mais preciso)
- **Raio Mínimo**: Tamanho mínimo das microalgas em pixels
- **Raio Máximo**: Tamanho máximo das microalgas em pixels

## Resultados

Os resultados são salvos no diretório `resultados_analise` e incluem:
- Imagem processada com marcações
- Arquivo CSV com coordenadas e dimensões
- Relatório em texto com estatísticas

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar pull requests. 