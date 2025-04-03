import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from data_collector import DataCollector
from pattern_analyzer import PatternAnalyzer

# Configuração da página
st.set_page_config(
    page_title="Análise de Padrões BTC/USDT",
    page_icon="📈",
    layout="wide"
)

# Título e descrição
st.title("📈 Análise de Padrões BTC/USDT em Tempo Real")
st.markdown("""
Este dashboard mostra a análise de padrões de candlesticks do BTC/USDT em tempo real.
- Gráfico M5 com padrões identificados
- Previsão da próxima vela
""")

# Inicializa os componentes
collector = DataCollector()
analyzer = PatternAnalyzer()

# Sidebar para configurações
st.sidebar.header("Configurações")
update_interval = st.sidebar.slider("Intervalo de atualização (segundos)", 5, 60, 30)
candles_limit = st.sidebar.slider("Número de candles", 50, 500, 200)

# Função para criar o gráfico
def create_candlestick_chart(df, patterns, repeated_patterns):
    fig = go.Figure()
    
    # Adiciona o gráfico de candlesticks
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='BTC/USDT'
    ))
    
    # Adiciona marcadores para padrões
    for pattern, idx in patterns:
        if idx < len(df):
            candle = df.iloc[idx]
            price = (candle['high'] + candle['low']) / 2
            
            if pattern == 'hammer':
                fig.add_trace(go.Scatter(
                    x=[df.index[idx]],
                    y=[price],
                    mode='markers',
                    marker=dict(symbol='triangle-up', size=15, color='green'),
                    name='Hammer'
                ))
            elif pattern == 'shooting_star':
                fig.add_trace(go.Scatter(
                    x=[df.index[idx]],
                    y=[price],
                    mode='markers',
                    marker=dict(symbol='triangle-down', size=15, color='red'),
                    name='Shooting Star'
                ))
            elif pattern == 'doji':
                fig.add_trace(go.Scatter(
                    x=[df.index[idx]],
                    y=[price],
                    mode='markers',
                    marker=dict(symbol='circle', size=15, color='blue'),
                    name='Doji'
                ))
    
    # Adiciona marcadores para padrões repetidos
    for pattern, indices in repeated_patterns:
        for idx in indices:
            if idx < len(df):
                candle = df.iloc[idx]
                price = (candle['high'] + candle['low']) / 2
                
                fig.add_trace(go.Scatter(
                    x=[df.index[idx]],
                    y=[price],
                    mode='markers',
                    marker=dict(symbol='star', size=20, color='yellow'),
                    name=f'Repetido: {pattern}'
                ))
    
    # Atualiza o layout
    fig.update_layout(
        title='BTC/USDT - M5',
        yaxis_title='Preço',
        xaxis_title='Data/Hora',
        height=600,
        showlegend=True
    )
    
    return fig

# Container para o gráfico
chart_container = st.empty()

# Container para previsão
prediction_container = st.empty()

# Loop principal
while True:
    try:
        # Coleta dados
        m1_data, m5_data = collector.get_multiple_timeframes(limit=candles_limit)
        
        if m1_data is not None and m5_data is not None:
            # Analisa padrões
            m5_patterns = analyzer.analyze_patterns(m5_data)
            
            # Atualiza o gráfico
            fig = create_candlestick_chart(m5_data, m5_patterns, analyzer.repeated_patterns)
            chart_container.plotly_chart(fig, use_container_width=True)
            
            # Atualiza previsão
            prediction = analyzer.predict_next_candle(m1_data, m5_data)
            with prediction_container.container():
                st.subheader("Previsão")
                if prediction == 'bullish':
                    st.success(f"Próxima vela M5: {prediction.upper()} 📈")
                else:
                    st.error(f"Próxima vela M5: {prediction.upper()} 📉")
        
        # Aguarda o próximo ciclo
        time.sleep(update_interval)
        
    except Exception as e:
        st.error(f"Erro ao atualizar dados: {str(e)}")
        time.sleep(update_interval) 