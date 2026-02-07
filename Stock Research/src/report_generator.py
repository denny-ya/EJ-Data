import os
import datetime

class ReportGenerator:
    def __init__(self, ticker):
        self.ticker = ticker
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
        os.makedirs(self.output_dir, exist_ok=True)

    def generate(self, chart_data, news_data):
        """
        Generates a markdown report.
        """
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{self.ticker}_Report_{date_str}.md"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# 📈 {self.ticker} 분석 리포트 (Analysis Report)\n")
            f.write(f"**날짜 (Date)**: {date_str}\n\n")

            # 1. Executive Summary
            trend = chart_data.get('trend_summary', 'N/A')
            price = chart_data.get('current_price', 0)
            f.write("## 1. 요약 (Executive Summary)\n")
            f.write(f"- **현재가 (Price)**: {price:,.0f} KRW\n")
            f.write(f"- **추세 (Trend)**: {trend}\n")
            
            patterns = chart_data.get('patterns', [])
            if patterns:
                f.write(f"- **감지된 패턴 (Signals)**: {', '.join(patterns)}\n")
            else:
                f.write("- **감지된 패턴**: 없음 (최근 3일 기준)\n")
            f.write("\n")

            # 2. Technical Analysis
            f.write("## 2. 기술적 분석 (Technical Analysis)\n")
            f.write("### 차트 (Chart)\n")
            chart_img = chart_data.get('chart_image')
            if chart_img:
                # Relative path for markdown
                rel_path = os.path.relpath(chart_img, self.output_dir)
                f.write(f"![Chart]({rel_path})\n\n")
            
            f.write("### 📊 상세 기술적 분석 (Detailed Analysis Results)\n")
            
            # Trend Check
            indicators = chart_data.get('indicators', {})
            ma20 = indicators.get('MA20', 0)
            ma60 = indicators.get('MA60', 0)
            ma120 = indicators.get('MA120', 0)
            
            f.write("**1. 이동평균선 배열 및 추세 (Moving Average Alignment)**\n")
            if price > ma20 and ma20 > ma60:
                f.write("- **정배열 (Bullish Alignment)**: 주가 > 20일선 > 60일선 (강한 상승 추세)\n")
            elif price < ma20 and ma20 < ma60:
                f.write("- **역배열 (Bearish Alignment)**: 주가 < 20일선 < 60일선 (하락 추세 지속)\n")
            else:
                f.write("- **혼조세 (Mixed)**: 이평선이 엇갈려 있어 추세 전환 또는 횡보 구간임.\n")
            f.write(f"- (20일: {ma20:,.0f}, 60일: {ma60:,.0f}, 120일: {ma120:,.0f})\n\n")

            # Support/Resistance Check
            f.write("**2. 지지 및 저항 분석 (Support & Resistance)**\n")
            nearest_ma = min([ma20, ma60, ma120], key=lambda x: abs(x - price))
            diff_pct = ((price - nearest_ma) / nearest_ma) * 100
            
            if abs(diff_pct) < 1.0: # Within 1%
                f.write(f"- **중요 위치**: 현재 주가가 주요 이동평균선({nearest_ma:,.0f}) 부근에 위치함.\n")
                if diff_pct > 0:
                    f.write("  - **지지 테스트 (Support Test)**: 이평선 지지 여부 확인 필요.\n")
                else:
                    f.write("  - **저항 테스트 (Resistance Test)**: 이평선 돌파 여부 확인 필요.\n")
            elif price > nearest_ma:
                 f.write(f"- **지지선 확인**: 주요 지지선(이평선) 위에 위치함 (이격도: {diff_pct:+.1f}%).\n")
            else:
                 f.write(f"- **저항선 확인**: 주요 저항선(이평선) 아래에 위치함 (이격도: {diff_pct:+.1f}%).\n")
            f.write("\n")

            # Pattern Check
            f.write("**3. 패턴 분석 (Pattern Analysis)**\n")
            if patterns:
                 f.write(f"- ✅ **감지된 신호**: {', '.join(patterns)}\n")
            else:
                 f.write("- ⏳ **특이 패턴 없음**: 컵앤핸들, W패턴 등은 차트 이미지를 통해 육안 확인 권장.\n")
            f.write("\n")
            
            # NEW: RSI/MACD/Volume Indicators
            f.write("**4. 보조지표 분석 (Technical Indicators)**\n")
            
            # RSI
            rsi_val = indicators.get('RSI')
            rsi_signal = indicators.get('RSI_Signal', 'N/A')
            if rsi_val is not None:
                f.write(f"- **RSI (14일)**: {rsi_val:.1f} - {rsi_signal}\n")
                if rsi_val >= 70:
                    f.write("  - ⚠️ 과매수 구간: 조정 가능성에 유의\n")
                elif rsi_val <= 30:
                    f.write("  - 💡 과매도 구간: 반등 가능성 존재\n")
            else:
                f.write("- **RSI**: 데이터 부족\n")
            
            # MACD
            macd_val = indicators.get('MACD')
            macd_signal = indicators.get('MACD_Signal_Line')
            macd_cross = indicators.get('MACD_Cross', '없음')
            if macd_val is not None and macd_signal is not None:
                f.write(f"- **MACD**: {macd_val:,.0f} / Signal: {macd_signal:,.0f}\n")
                if '골든' in macd_cross:
                    f.write(f"  - ✅ {macd_cross}\n")
                elif '데드' in macd_cross:
                    f.write(f"  - ⚠️ {macd_cross}\n")
                elif macd_cross != '없음 (None)':
                    f.write(f"  - {macd_cross}\n")
            else:
                f.write("- **MACD**: 데이터 부족\n")
            
            # Volume
            vol_ratio = indicators.get('Volume_Ratio')
            vol_signal = indicators.get('Volume_Signal', 'N/A')
            if vol_ratio is not None:
                f.write(f"- **거래량**: 20일 평균 대비 {vol_ratio}배 - {vol_signal}\n")
            else:
                f.write("- **거래량**: 데이터 부족\n")
            f.write("\n")

            # 3. Fundamental & Market Analysis (New)
            f.write("## 3. 기본적 & 시장 분석 (Fundamental & Market)\n")
            
            # 3.1 Corporate Vision
            company_info = news_data.get('company_info', {})
            f.write("### 🏢 기업 비전 및 개요 (Corporate Vision)\n")
            f.write(f"- **섹터 (Sector)**: {company_info.get('sector', 'N/A')}\n")
            summary = company_info.get('summary', 'N/A')
            # Truncate summary if too long for report readability
            if len(summary) > 300:
                summary = summary[:300] + "..."
            f.write(f"- **사업 요약**: {summary}\n\n")

            # 3.2 Market Trend
            f.write("### 🌊 시장/섹터 동향 (Market Trend)\n")
            f.write("**국내 산업 동향 (Domestic)**\n")
            sector_news = news_data.get('sector_trend', [])
            self._write_news_list(f, sector_news)

            f.write("\n**글로벌 시장 영향 (Global Impact - US/Global)**\n")
            global_news = news_data.get('global_trend', [])
            self._write_news_list(f, global_news)

            f.write("\n**정부 정책 및 규제 (Policy & Regulations)**\n")
            policy_news = news_data.get('policy_news', [])
            self._write_news_list(f, policy_news)

            # 3.3 Brokerage Consensus
            f.write("\n### 📑 증권사 리포트 요약 (Brokerage Reports)\n")
            brokerage_reports = news_data.get('brokerage_reports', [])
            self._write_news_list(f, brokerage_reports)
            f.write("\n")

            # 4. News & Risks
            f.write("## 4. 뉴스 및 리스크 (News & Risks)\n")
            
            # Risks Highlights
            risks = news_data.get('risks', [])
            if risks:
                f.write("### ⚠️ 주요 리스크 요인 (Risk Factors)\n")
                for risk in risks:
                    f.write(f"- **{risk['keyword']}**: {risk['description']} ([Source]({risk['source']}))\n")
            else:
                f.write("### ✅ 리스크 점검\n")
                f.write("- 최근 주요 뉴스에서 감지된 중대 리스크 키워드 없음.\n")
            
            # Recent News
            f.write("\n### 최근 뉴스 (Recent News)\n")
            self._write_news_list(f, news_data.get('news', []))

            # 5. Conclusion (New Section)
            f.write("\n## 5. 종합 분석 결과 (Conclusion)\n")
            
            # Simple scoring logic
            score = 0
            reasons = []
            
            # 1. Trend Score
            if "상승세" in trend:
                score += 2
                reasons.append("주가가 상승 추세에 있으며 이동평균선이 정배열 상태입니다.")
            elif "하락세" in trend:
                score -= 2
                reasons.append("주가가 하락 추세에 있으며 이동평균선이 역배열 상태입니다.")
            else:
                reasons.append("주가가 뚜렷한 방향성 없이 횡보하고 있습니다.")

            # 2. Pattern Score
            bullish_patterns = [p for p in patterns if "상승" in p or "Bullish" in p or "W패턴" in p or "컵앤핸들" in p]
            bearish_patterns = [p for p in patterns if "하락" in p or "Bearish" in p or "M패턴" in p or "흑삼병" in p]
            
            if bullish_patterns:
                score += 1
                reasons.append(f"긍정적 패턴이 감지되었습니다: {', '.join(bullish_patterns)}")
            if bearish_patterns:
                score -= 1
                reasons.append(f"부정적 패턴이 감지되었습니다: {', '.join(bearish_patterns)}")

            # 3. Support/Resistance Score
            indicators = chart_data.get('indicators', {})
            ma20 = indicators.get('MA20', 0)
            if price > ma20:
                score += 1
            else:
                score -= 1
            
            # 4. NEW: RSI Score
            rsi_val = indicators.get('RSI')
            if rsi_val is not None:
                if rsi_val >= 70:
                    score -= 1
                    reasons.append(f"RSI {rsi_val:.1f}로 과매수 구간 - 조정 가능성에 유의")
                elif rsi_val <= 30:
                    score += 1
                    reasons.append(f"RSI {rsi_val:.1f}로 과매도 구간 - 반등 기대")
            
            # 5. NEW: MACD Cross Score
            macd_cross = indicators.get('MACD_Cross', '')
            if '골든크로스' in macd_cross:
                score += 1
                reasons.append(f"MACD {macd_cross}")
            elif '데드크로스' in macd_cross:
                score -= 1
                reasons.append(f"MACD {macd_cross}")
            
            # 6. NEW: Volume Score
            vol_ratio = indicators.get('Volume_Ratio')
            vol_signal = indicators.get('Volume_Signal', '')
            if vol_ratio and vol_ratio >= 2.0:
                if '양봉' in vol_signal or 'Buying' in vol_signal:
                    score += 1
                    reasons.append(f"거래량 {vol_ratio}배 급증과 함께 강한 매수세")
                elif '음봉' in vol_signal or 'Selling' in vol_signal:
                    score -= 1
                    reasons.append(f"거래량 {vol_ratio}배 급증과 함께 강한 매도세")

            # Determine Verdict
            verdict = "관망 (Hold)"
            color = "🟡"
            if score >= 4:
                verdict = "강력 매수 (Strong Buy)"
                color = "🟢"
            elif score >= 2:
                verdict = "매수 (Buy)"
                color = "🟢"
            elif score <= -4:
                verdict = "강력 매도 (Strong Sell)"
                color = "🔴"
            elif score <= -2:
                verdict = "매도 (Sell)"
                color = "🔴"

            f.write(f"### 📋 종합 의견: {color} **{verdict}**\n")
            f.write(f"#### 💡 판단 근거 (점수: {score}점)\n")
            for reason in reasons:
                f.write(f"- {reason}\n")
            
            f.write("\n> **참고**: 본 분석은 기술적 지표와 뉴스 데이터를 기반으로 한 참고용 자료이며, 실제 투자의 책임은 투자자 본인에게 있습니다.\n")

        return filepath

    def _write_news_list(self, f, news_list):
        if news_list and isinstance(news_list, list):
            for item in news_list:
                f.write(f"- **{item['title']}** ([Link]({item['link']}))\n")
        else:
            f.write("- 관련 데이터 없음 (No Data Found).\n")
