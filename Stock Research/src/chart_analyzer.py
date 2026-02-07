import yfinance as yf
import mplfinance as mpf
import pandas as pd
import numpy as np
import os
import datetime
import ssl
import urllib3

# SSL 인증서 문제 우회 (한글 경로 문제 해결)
try:
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    pass

class ChartAnalyzer:
    def __init__(self, ticker):
        self.ticker = ticker
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "charts")
        os.makedirs(self.output_dir, exist_ok=True)

    def _detect_patterns(self, df_subset):
        patterns = []
        if len(df_subset) < 3: return patterns

        # Data preparation
        rows = [row for _, row in df_subset.iterrows()]
        dates = [idx.strftime('%Y-%m-%d') for idx in df_subset.index]
        
        # 1. 캔들 색상 및 형태 (Last day)
        last_row = rows[-1]
        last_date = dates[-1]
        
        if last_row['Close'] > last_row['Open']:
            change_pct = (last_row['Close'] - last_row['Open']) / last_row['Open'] * 100
            if change_pct > 5.0:
                patterns.append(f"장대양봉 (Long Bullish Candle): {last_date} (+{change_pct:.1f}%)")
            else:
                patterns.append(f"양봉 (Bullish Candle): {last_date}")
        elif last_row['Close'] < last_row['Open']:
             patterns.append(f"음봉 (Bearish Candle): {last_date}")

        # 2. 캔들 패턴 (Engulfing, Three Black Crows)
        # 흑삼병 (Three Black Crows): 3 consecutive bearish candles
        if all(r['Close'] < r['Open'] for r in rows[-3:]):
            patterns.append(f"흑삼병 (Three Black Crows): {dates[-3]}~{last_date} (하락 예고)")

        # 장악형 (Engulfing) - Last 2 days
        prev_row = rows[-2]
        curr_row = rows[-1]
        prev_body = abs(prev_row['Close'] - prev_row['Open'])
        curr_body = abs(curr_row['Close'] - curr_row['Open'])
        
        # Bullish Engulfing (Previous: Bearish, Current: Bullish & Engulfs)
        if (prev_row['Close'] < prev_row['Open'] and 
            curr_row['Close'] > curr_row['Open'] and 
            curr_row['Open'] < prev_row['Close'] and 
            curr_row['Close'] > prev_row['Open']):
            patterns.append(f"상승장악형 (Bullish Engulfing): {last_date} (반전 신호)")
            
        # Bearish Engulfing (Previous: Bullish, Current: Bearish & Engulfs)
        if (prev_row['Close'] > prev_row['Open'] and 
            curr_row['Close'] < curr_row['Open'] and 
            curr_row['Open'] > prev_row['Close'] and 
            curr_row['Close'] < prev_row['Open']):
            patterns.append(f"하락장악형 (Bearish Engulfing): {last_date} (반전 신호)")

        # 3. Pinbar Detection
        for i, row in enumerate(rows):
            body_size = abs(row['Close'] - row['Open'])
            upper_shadow = row['High'] - max(row['Close'], row['Open'])
            lower_shadow = min(row['Close'], row['Open']) - row['Low']
            
            if body_size == 0: continue
            
            # Pinbar: Long tail (shadow) > 2 * body
            if lower_shadow > (2 * body_size) and upper_shadow < body_size:
                patterns.append(f"상승 핀바 (Bullish Pinbar): {dates[i]}")
            elif upper_shadow > (2 * body_size) and lower_shadow < body_size:
                patterns.append(f"하락 핀바 (Bearish Pinbar): {dates[i]}")
        
        return patterns

    def analyze(self):
        # Fetch data (1 year)
        stock = yf.Ticker(self.ticker)
        df = stock.history(period="1y")

        if df.empty:
            raise ValueError(f"No data found for {self.ticker}")

        # 1. Moving Averages
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['MA60'] = df['Close'].rolling(window=60).mean()
        df['MA120'] = df['Close'].rolling(window=120).mean()

        # 2. RSI 계산 (14일)
        rsi_data = self._calculate_rsi(df)
        df['RSI'] = rsi_data['rsi']
        
        # 3. MACD 계산 (12, 26, 9)
        macd_data = self._calculate_macd(df)
        df['MACD'] = macd_data['macd']
        df['MACD_Signal'] = macd_data['signal']
        df['MACD_Hist'] = macd_data['histogram']
        
        # 4. 거래량 분석
        volume_data = self._analyze_volume(df)

        # 5. Trend Determination
        current_price = df['Close'].iloc[-1]
        ma20 = df['MA20'].iloc[-1]
        ma60 = df['MA60'].iloc[-1]
        
        trend = "횡보세 (Sideways)"
        if current_price > ma20 and ma20 > ma60:
            trend = "상승세 (Uptrend/Bullish)"
        elif current_price < ma20 and ma20 < ma60:
            trend = "하락세 (Downtrend/Bearish)"

        # 6. Pattern Detection
        recent_patterns = self._detect_patterns(df.tail(3))
        
        # Advanced Pattern Detection
        advanced_patterns = self._detect_advanced_patterns(df.tail(60))
        recent_patterns.extend(advanced_patterns)
        
        # RSI/MACD/Volume 시그널 추가
        indicator_signals = self._detect_indicator_signals(df, rsi_data, macd_data, volume_data)
        recent_patterns.extend(indicator_signals)

        # Generate Chart Image
        chart_path = self._plot_chart(df)

        return {
            "current_price": current_price,
            "chart_image": chart_path,
            "trend_summary": trend,
            "patterns": recent_patterns,
            "indicators": {
                "MA20": ma20,
                "MA60": ma60,
                "MA120": df['MA120'].iloc[-1],
                "RSI": rsi_data['rsi'].iloc[-1] if not pd.isna(rsi_data['rsi'].iloc[-1]) else None,
                "RSI_Signal": rsi_data['signal'],
                "MACD": macd_data['macd'].iloc[-1] if not pd.isna(macd_data['macd'].iloc[-1]) else None,
                "MACD_Signal_Line": macd_data['signal'].iloc[-1] if not pd.isna(macd_data['signal'].iloc[-1]) else None,
                "MACD_Cross": macd_data['cross_signal'],
                "Volume_Ratio": volume_data['volume_ratio'],
                "Volume_Signal": volume_data['signal']
            }
        }
    
    def _calculate_rsi(self, df, period=14):
        """
        RSI(상대강도지수) 계산
        - 70 이상: 과매수 → 조정 가능성
        - 30 이하: 과매도 → 반등 가능성
        """
        delta = df['Close'].diff()
        
        gain = delta.where(delta > 0, 0)
        loss = (-delta).where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # RSI 신호 판별
        current_rsi = rsi.iloc[-1]
        signal = "중립 (Neutral)"
        if not pd.isna(current_rsi):
            if current_rsi >= 70:
                signal = "과매수 (Overbought)"
            elif current_rsi <= 30:
                signal = "과매도 (Oversold)"
            elif current_rsi >= 60:
                signal = "매수세 우위 (Bullish Momentum)"
            elif current_rsi <= 40:
                signal = "매도세 우위 (Bearish Momentum)"
        
        return {
            'rsi': rsi,
            'signal': signal
        }
    
    def _calculate_macd(self, df, fast=12, slow=26, signal_period=9):
        """
        MACD 계산
        - MACD = EMA(12) - EMA(26)
        - Signal = EMA(MACD, 9)
        - 골든크로스: MACD가 Signal 상향 돌파 → 매수
        - 데드크로스: MACD가 Signal 하향 돌파 → 매도
        """
        ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
        
        macd = ema_fast - ema_slow
        signal = macd.ewm(span=signal_period, adjust=False).mean()
        histogram = macd - signal
        
        # 크로스 시그널 판별 (최근 5일 내)
        cross_signal = "없음 (None)"
        if len(macd) >= 5:
            for i in range(-1, -5, -1):
                if i == -1:
                    continue
                # 골든크로스: 이전 MACD < Signal, 현재 MACD > Signal
                if macd.iloc[i] < signal.iloc[i] and macd.iloc[i+1] > signal.iloc[i+1]:
                    cross_signal = f"골든크로스 (Golden Cross) - {df.index[i+1].strftime('%Y-%m-%d')}"
                    break
                # 데드크로스: 이전 MACD > Signal, 현재 MACD < Signal
                elif macd.iloc[i] > signal.iloc[i] and macd.iloc[i+1] < signal.iloc[i+1]:
                    cross_signal = f"데드크로스 (Dead Cross) - {df.index[i+1].strftime('%Y-%m-%d')}"
                    break
        
        return {
            'macd': macd,
            'signal': signal,
            'histogram': histogram,
            'cross_signal': cross_signal
        }
    
    def _analyze_volume(self, df, period=20):
        """
        거래량 분석
        - 평균 대비 비율 계산
        - 거래량 급증 + 양봉 = 강한 매수세
        - 거래량 급증 + 음봉 = 강한 매도세
        """
        avg_volume = df['Volume'].rolling(window=period).mean()
        current_volume = df['Volume'].iloc[-1]
        avg_vol = avg_volume.iloc[-1]
        
        if pd.isna(avg_vol) or avg_vol == 0:
            return {'volume_ratio': None, 'signal': '데이터 부족'}
        
        volume_ratio = current_volume / avg_vol
        
        # 오늘 캔들 색상 확인
        is_bullish = df['Close'].iloc[-1] > df['Open'].iloc[-1]
        
        signal = "보통 (Normal)"
        if volume_ratio >= 2.0:
            if is_bullish:
                signal = "거래량 급증 + 양봉 (Strong Buying)"
            else:
                signal = "거래량 급증 + 음봉 (Strong Selling)"
        elif volume_ratio >= 1.5:
            if is_bullish:
                signal = "거래량 증가 + 양봉 (Buying Pressure)"
            else:
                signal = "거래량 증가 + 음봉 (Selling Pressure)"
        elif volume_ratio <= 0.5:
            signal = "거래량 감소 (Low Volume)"
        
        return {
            'volume_ratio': round(volume_ratio, 2),
            'signal': signal
        }
    
    def _detect_indicator_signals(self, df, rsi_data, macd_data, volume_data):
        """
        RSI/MACD/Volume 기반 시그널 생성
        """
        signals = []
        
        # RSI 시그널
        rsi_val = rsi_data['rsi'].iloc[-1]
        if not pd.isna(rsi_val):
            if rsi_val >= 70:
                signals.append(f"RSI 과매수 ({rsi_val:.1f}) - 조정 주의")
            elif rsi_val <= 30:
                signals.append(f"RSI 과매도 ({rsi_val:.1f}) - 반등 기대")
        
        # MACD 크로스 시그널
        if "골든크로스" in macd_data['cross_signal']:
            signals.append(f"MACD {macd_data['cross_signal']}")
        elif "데드크로스" in macd_data['cross_signal']:
            signals.append(f"MACD {macd_data['cross_signal']}")
        
        # 거래량 시그널
        if volume_data['volume_ratio'] and volume_data['volume_ratio'] >= 2.0:
            signals.append(f"거래량 급증 ({volume_data['volume_ratio']}배) - {volume_data['signal']}")
        
        return signals

    def _detect_advanced_patterns(self, df):
        patterns = []
        if len(df) < 60: return patterns
        
        prices = df['Close'].values
        # Normalize for easier comparison
        
        # 1. W-Pattern (Double Bottom)
        # Simplified: Check min of first half vs min of second half
        mid = len(prices) // 2
        min1 = min(prices[:mid])
        min2 = min(prices[mid:])
        
        if abs(min1 - min2) / min1 < 0.03: # Lows match within 3%
            peak = max(prices[mid-5:mid+5]) 
            if peak > min1 * 1.05: # Peak exists
                 patterns.append("W패턴/이중바닥 가능성 (Double Bottom Potential)")

        # 2. M-Pattern (Double Top)
        # Simplified: Check max of first half vs max of second half
        max1 = max(prices[:mid])
        max2 = max(prices[mid:])
        
        if abs(max1 - max2) / max1 < 0.03: # Highs match within 3%
            trough = min(prices[mid-5:mid+5])
            if trough < max1 * 0.95: # Trough exists
                patterns.append("M패턴/이중천장 가능성 (Double Top Potential)")

        # 3. Head & Shoulders (H&S) - Heuristic
        # Find 3 Peaks: Left(L), Head(H), Right(R)
        # H > L, H > R, L ~= R
        # We divide into 3 segments
        seg_len = len(prices) // 3
        p1 = max(prices[:seg_len]) # Left
        p2 = max(prices[seg_len:seg_len*2]) # Head
        p3 = max(prices[seg_len*2:]) # Right
        
        if p2 > p1 * 1.02 and p2 > p3 * 1.02: # Head is clearly higher
            if abs(p1 - p3) / p1 < 0.05: # Shoulders similar height (5%)
                patterns.append("헤드 앤 숄더 가능성 (Head & Shoulders Potential)")

        # 4. Cup & Handle (Simplified)
        recent_high = max(prices[-20:-5])
        current = prices[-1]
        if current < recent_high * 0.98 and current > recent_high * 0.90:
             period_low = min(prices)
             period_start = prices[0]
             if period_low < period_start * 0.9 and period_low < recent_high * 0.9:
                 patterns.append("컵앤핸들 형성 가능성 (Cup & Handle Potential)")

        # 5. Triangle / Flag (Volatility Contraction)
        # Check if highs are lowering and lows are rising over last 30 days
        sub_prices = prices[-30:]
        half = len(sub_prices) // 2
        
        high1 = max(sub_prices[:half])
        high2 = max(sub_prices[half:])
        low1 = min(sub_prices[:half])
        low2 = min(sub_prices[half:])
        
        if high1 > high2 and low1 < low2:
            patterns.append("삼각수렴/깃발형 가능성 (Triangle/Flag Potential)")

        return patterns

    def _plot_chart(self, df):
        filename = f"{self.ticker}_chart.png"
        filepath = os.path.join(self.output_dir, filename)
        
        # Custom Style
        mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
        s = mpf.make_mpf_style(marketcolors=mc)

        # Plot with MAs and Volume
        mpf.plot(df, type='candle', style=s, volume=True, 
                 mav=(20, 60, 120), 
                 title=f"{self.ticker} Daily Chart",
                 savefig=filepath)
        
        return filepath
