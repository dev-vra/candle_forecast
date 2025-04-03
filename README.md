# Análise de Padrões de Candlesticks BTC/USD

Este sistema utiliza inteligência artificial para analisar padrões de candlesticks no mercado de BTC/USD, combinando dados dos timeframes M1 e M5 para fazer previsões da direção da próxima vela.

## Funcionalidades

- Coleta de dados históricos em tempo real da Binance
- Identificação de padrões de candlesticks (Hammer, Shooting Star, Doji, Engulfing)
- Análise combinada dos timeframes M1 e M5
- Visualização gráfica dos padrões identificados
- Previsão da direção da próxima vela

## Requisitos

- Python 3.8 ou superior
- Conexão com a internet
- Bibliotecas listadas no requirements.txt

## Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

Execute o script principal:
```bash
python main.py
```

O sistema irá:
1. Coletar dados históricos
2. Analisar padrões
3. Fazer previsão
4. Exibir gráficos com os padrões identificados

## Padrões Identificados

- **Hammer**: Sinal de reversão de baixa
- **Shooting Star**: Sinal de reversão de alta
- **Doji**: Indecisão do mercado
- **Engulfing Bullish**: Reversão de baixa
- **Engulfing Bearish**: Reversão de alta

## Observações

- O sistema utiliza dados em tempo real da Binance
- A previsão é baseada em análise técnica e padrões históricos
- Use o sistema como ferramenta auxiliar, não como única fonte de decisão 