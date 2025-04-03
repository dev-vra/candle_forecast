from data_collector import DataCollector
from pattern_analyzer import PatternAnalyzer
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def plot_chart_with_patterns(df, patterns, repeated_patterns, title):
    """Plota o gráfico com os padrões identificados"""
    # Cria o estilo do gráfico
    mc = mpf.make_marketcolors(up='g', down='r')
    s = mpf.make_mpf_style(marketcolors=mc)
    
    # Prepara os marcadores para os padrões
    markers = []
    for pattern, idx in patterns:
        if idx < len(df):
            candle = df.iloc[idx]
            price = (candle['high'] + candle['low']) / 2
            
            # Cria um DataFrame temporário para o marcador com o mesmo índice do DataFrame original
            temp_df = pd.DataFrame(index=df.index)
            temp_df['price'] = np.nan
            temp_df.loc[df.index[idx], 'price'] = price
            
            if pattern == 'hammer':
                markers.append(mpf.make_addplot(temp_df['price'], type='scatter', marker='^', color='g', markersize=100))
            elif pattern == 'shooting_star':
                markers.append(mpf.make_addplot(temp_df['price'], type='scatter', marker='v', color='r', markersize=100))
            elif pattern == 'doji':
                markers.append(mpf.make_addplot(temp_df['price'], type='scatter', marker='o', color='b', markersize=100))
    
    # Adiciona marcadores para padrões repetidos
    for pattern, indices in repeated_patterns:
        for idx in indices:
            if idx < len(df):
                candle = df.iloc[idx]
                price = (candle['high'] + candle['low']) / 2
                
                temp_df = pd.DataFrame(index=df.index)
                temp_df['price'] = np.nan
                temp_df.loc[df.index[idx], 'price'] = price
                
                # Usa um marcador diferente para padrões repetidos
                markers.append(mpf.make_addplot(temp_df['price'], type='scatter', marker='*', color='y', markersize=150))
    
    # Plota o gráfico
    mpf.plot(df, type='candle', style=s, title=title, addplot=markers)

def print_pattern_info(patterns, repeated_patterns):
    """Imprime informações sobre os padrões encontrados"""
    if not patterns and not repeated_patterns:
        print("Nenhum padrão encontrado.")
        return
    
    if patterns:
        print("\nPadrões encontrados:")
        for pattern, idx in patterns:
            print(f"- {pattern.upper()} no candle {idx}")
    
    if repeated_patterns:
        print("\nPadrões repetidos:")
        for pattern, indices in repeated_patterns:
            print(f"- {pattern.upper()} repetido nos candles {indices}")

def main():
    # Inicializa os componentes
    collector = DataCollector()
    analyzer = PatternAnalyzer()
    
    # Coleta dados
    print("Coletando dados históricos...")
    m1_data, m5_data = collector.get_multiple_timeframes(limit=200)  # Aumentado para 200 candles
    
    if m1_data is None or m5_data is None:
        print("Erro ao coletar dados. Verifique sua conexão com a internet.")
        return
    
    # Analisa padrões
    print("Analisando padrões...")
    m5_patterns = analyzer.analyze_patterns(m5_data)
    
    # Imprime informações sobre os padrões
    print_pattern_info(m5_patterns, analyzer.repeated_patterns)
    
    # Faz previsão
    prediction = analyzer.predict_next_candle(m1_data, m5_data)
    print(f"\nPrevisão para próxima vela M5: {prediction.upper()}")
    
    # Plota os gráficos
    print("\nPlotando gráficos...")
    
    # Gráfico M5
    plot_chart_with_patterns(m5_data, m5_patterns, analyzer.repeated_patterns, "BTC/USDT - M5")
    
    # Gráfico M1 (últimos 25 candles)
    plot_chart_with_patterns(m1_data.tail(25), [], [], "BTC/USDT - M1 (últimos 25 candles)")
    
    plt.show()

if __name__ == "__main__":
    main() 