# Contador de Microalgas

Um software para análise e contagem automática de microalgas em imagens microscópicas.

## Download e Instalação

### Opção 1: Download Direto (Recomendado)
1. Acesse a [página de releases](https://github.com/robertfabio/contador-microalgas/releases)
2. Baixe o arquivo `ContadorMicroalgas.exe` mais recente
3. Execute o programa clicando duas vezes no arquivo baixado

### Opção 2: Instalação via Python (Para desenvolvedores)
Se você deseja modificar o código ou contribuir com o projeto:

1. Clone este repositório:
```bash
git clone https://github.com/robertfabio/contador-microalgas.git
cd contador-microalgas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o programa:
```bash
python microalgas/main.py
```

## Como Usar

1. Abra o programa
2. Clique em "Carregar Imagem" e selecione uma foto de microscópio
3. Ajuste os parâmetros de detecção usando os controles deslizantes:
   - **Distância Mínima**: Distância entre microalgas (aumente se estiver detectando a mesma microalga várias vezes)
   - **Sensibilidade**: Sensibilidade na detecção (aumente se estiver perdendo microalgas, diminua se estiver detectando ruído)
   - **Acurácia**: Precisão na detecção (aumente para detecção mais precisa, diminua se estiver perdendo microalgas)
   - **Raio Mínimo/Máximo**: Ajuste conforme o tamanho das suas microalgas
4. Clique em "Contar Microalgas" para processar a imagem
5. Os resultados serão exibidos na tela e podem ser exportados

## Resultados

O programa fornece:
- Contagem total de microalgas
- Tamanho médio das microalgas
- Densidade de microalgas por área
- Imagem processada com marcações
- Relatório detalhado em CSV

Os resultados são salvos automaticamente na pasta `resultados_analise`.

## Exemplos

Incluímos algumas imagens de exemplo na pasta `imagens_teste` para você começar:
- `circulos_simples.png`: Imagem com círculos básicos para teste inicial
- `microorganismos.jpg`: Imagem de microscópio com células circulares
- `bolhas.jpg`: Imagem com bolhas de diferentes tamanhos

## Suporte

Se encontrar algum problema ou tiver sugestões:
1. Abra uma [issue](https://github.com/robertfabio/contador-microalgas/issues)
2. Ou envie um e-mail para: [seu-email@exemplo.com]

## Contribuição

Contribuições são bem-vindas! Por favor:
1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request 