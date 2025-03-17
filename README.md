# AlgaView

Um aplicativo Flutter para análise e contagem de microalgas em imagens microscópicas.

## Funcionalidades

- Seleção de imagens da galeria
- Processamento automático de imagens
- Detecção e contagem de microalgas
- Análise de características morfológicas
- Classificação por tipo de microalga
- Armazenamento local de análises
- Configurações ajustáveis de processamento

## Requisitos

- Flutter SDK >=3.0.0
- Dart SDK >=3.0.0

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/algaview.git
```

2. Instale as dependências:
```bash
cd algaview
flutter pub get
```

3. Execute o aplicativo:
```bash
flutter run
```

## Configurações de Processamento

O aplicativo permite ajustar os seguintes parâmetros:

- Tamanho do kernel de desfoque (3-11)
- Tamanho do bloco para threshold adaptativo (3-21)
- Constante C para threshold (0-10)
- Área mínima de detecção (50-500)
- Área máxima de detecção (500-10000)
- Circularidade mínima (0.0-1.0)

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
