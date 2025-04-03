import ccxt
import pandas as pd
from datetime import datetime, timedelta

class DataCollector:
    def __init__(self):
        self.exchange = ccxt.binance()
        
    def get_historical_data(self, timeframe='5m', limit=1000):
        """
        Coleta dados históricos do BTC/USD
        timeframe: '1m' ou '5m'
        limit: número de candles a serem coletados
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv('BTC/USDT', timeframe=timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Erro ao coletar dados: {e}")
            return None

    def get_multiple_timeframes(self, limit=1000):
        """
        Coleta dados dos timeframes M1 e M5
        """
        m1_data = self.get_historical_data('1m', limit)
        m5_data = self.get_historical_data('5m', limit)
        return m1_data, m5_data 