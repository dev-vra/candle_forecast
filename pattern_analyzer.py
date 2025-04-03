import numpy as np
import pandas as pd
from typing import List, Tuple, Dict

class PatternAnalyzer:
    def __init__(self):
        self.patterns = {
            'hammer': self._is_hammer,
            'shooting_star': self._is_shooting_star,
            'doji': self._is_doji,
            'engulfing_bullish': self._is_engulfing_bullish,
            'engulfing_bearish': self._is_engulfing_bearish
        }
        self.pattern_history = []
        self.repeated_patterns = []
    
    def _is_hammer(self, candle: pd.Series) -> bool:
        """Identifica padrão Hammer"""
        body = abs(candle['close'] - candle['open'])
        upper_wick = candle['high'] - max(candle['open'], candle['close'])
        lower_wick = min(candle['open'], candle['close']) - candle['low']
        
        return (lower_wick > 2 * body and 
                upper_wick < body and 
                candle['close'] > candle['open'])

    def _is_shooting_star(self, candle: pd.Series) -> bool:
        """Identifica padrão Shooting Star"""
        body = abs(candle['close'] - candle['open'])
        upper_wick = candle['high'] - max(candle['open'], candle['close'])
        lower_wick = min(candle['open'], candle['close']) - candle['low']
        
        return (upper_wick > 2 * body and 
                lower_wick < body and 
                candle['close'] < candle['open'])

    def _is_doji(self, candle: pd.Series) -> bool:
        """Identifica padrão Doji"""
        body = abs(candle['close'] - candle['open'])
        total_range = candle['high'] - candle['low']
        return body <= 0.1 * total_range

    def _is_engulfing_bullish(self, prev_candle: pd.Series, curr_candle: pd.Series) -> bool:
        """Identifica padrão Engulfing Bullish"""
        return (prev_candle['close'] < prev_candle['open'] and
                curr_candle['open'] < prev_candle['close'] and
                curr_candle['close'] > prev_candle['open'])

    def _is_engulfing_bearish(self, prev_candle: pd.Series, curr_candle: pd.Series) -> bool:
        """Identifica padrão Engulfing Bearish"""
        return (prev_candle['close'] > prev_candle['open'] and
                curr_candle['open'] > prev_candle['close'] and
                curr_candle['close'] < prev_candle['open'])

    def analyze_patterns(self, df: pd.DataFrame) -> List[Tuple[str, int]]:
        """Analisa padrões em um DataFrame de candles"""
        patterns_found = []
        self.pattern_history = []
        self.repeated_patterns = []
        
        for i in range(1, len(df)):
            prev_candle = df.iloc[i-1]
            curr_candle = df.iloc[i]
            
            for pattern_name, pattern_func in self.patterns.items():
                if pattern_name in ['engulfing_bullish', 'engulfing_bearish']:
                    if pattern_func(prev_candle, curr_candle):
                        patterns_found.append((pattern_name, i))
                        self.pattern_history.append((pattern_name, i))
                else:
                    if pattern_func(curr_candle):
                        patterns_found.append((pattern_name, i))
                        self.pattern_history.append((pattern_name, i))
        
        # Analisa padrões repetidos
        self._analyze_repeated_patterns()
        
        return patterns_found

    def _analyze_repeated_patterns(self):
        """Analisa padrões repetidos no histórico"""
        if len(self.pattern_history) < 2:
            return
        
        # Agrupa padrões por tipo
        pattern_groups = {}
        for pattern, idx in self.pattern_history:
            if pattern not in pattern_groups:
                pattern_groups[pattern] = []
            pattern_groups[pattern].append(idx)
        
        # Identifica padrões repetidos
        for pattern, indices in pattern_groups.items():
            if len(indices) >= 2:
                # Verifica se os padrões estão próximos (últimos 10 candles)
                recent_indices = [idx for idx in indices if idx >= max(indices) - 10]
                if len(recent_indices) >= 2:
                    self.repeated_patterns.append((pattern, recent_indices))

    def predict_next_candle(self, m1_data: pd.DataFrame, m5_data: pd.DataFrame) -> str:
        """
        Prevê a direção da próxima vela M5 baseado nos padrões atuais
        e no comportamento do M1
        """
        # Análise do M5
        m5_patterns = self.analyze_patterns(m5_data)
        
        # Análise do M1 (últimos 5 candles)
        recent_m1 = m1_data.tail(5)
        m1_trend = 'bullish' if recent_m1['close'].iloc[-1] > recent_m1['open'].iloc[-1] else 'bearish'
        
        # Verifica padrões repetidos
        if self.repeated_patterns:
            last_repeated = self.repeated_patterns[-1]
            pattern_name = last_repeated[0]
            
            if pattern_name in ['hammer', 'engulfing_bullish']:
                return 'bullish'
            elif pattern_name in ['shooting_star', 'engulfing_bearish']:
                return 'bearish'
        
        # Se não houver padrões repetidos, usa a lógica normal
        if m5_patterns:
            last_pattern = m5_patterns[-1]
            pattern_name = last_pattern[0]
            
            if pattern_name in ['hammer', 'engulfing_bullish']:
                return 'bullish'
            elif pattern_name in ['shooting_star', 'engulfing_bearish']:
                return 'bearish'
        
        # Se não houver padrões claros, segue a tendência do M1
        return m1_trend 