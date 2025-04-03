# Análise de Padrões de Candlesticks BTC/USDT

Este projeto implementa um sistema de análise de padrões de candlesticks para o par BTC/USDT, utilizando dados em tempo real da Binance. O sistema identifica padrões como Hammer, Shooting Star e Doji, além de analisar padrões repetidos e fazer previsões para a próxima vela.

## 🚀 Funcionalidades

- Coleta de dados em tempo real da Binance
- Análise de padrões de candlesticks (M5)
- Identificação de padrões repetidos
- Previsão da próxima vela
- Dashboard interativo em tempo real
- Visualização de gráficos com padrões identificados

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta na Binance (para acesso à API)

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/dev-vra/candle_forecast.git
cd candle_forecast
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🎮 Como Usar

### Dashboard Interativo

Para iniciar o dashboard interativo:

```bash
streamlit run dashboard.py
```

O dashboard oferece:
- Gráfico M5 em tempo real com padrões identificados
- Configurações de atualização e número de candles
- Lista de padrões encontrados
- Previsão da próxima vela
- Indicadores visuais para diferentes tipos de padrões

### Script Principal

Para executar a análise via linha de comando:

```bash
python main.py
```

O script irá:
1. Coletar dados históricos
2. Analisar padrões
3. Fazer previsões
4. Exibir gráficos com os padrões identificados

## 📊 Padrões Analisados

- **Hammer**: Sinal de reversão de baixa
- **Shooting Star**: Sinal de reversão de alta
- **Doji**: Indecisão do mercado
- **Padrões Repetidos**: Identificação de sequências de padrões

## 🔍 Estrutura do Projeto

- `data_collector.py`: Coleta dados da Binance
- `pattern_analyzer.py`: Análise de padrões e previsões
- `main.py`: Script principal para análise
- `dashboard.py`: Dashboard interativo em tempo real
- `requirements.txt`: Dependências do projeto

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Contato

Para dúvidas ou sugestões, abra uma issue no repositório. 