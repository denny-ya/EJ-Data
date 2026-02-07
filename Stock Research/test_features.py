# -*- coding: utf-8 -*-
"""테스트 스크립트: RSI/MACD/Volume 기능 확인"""
import sys
import os

# SSL 인증서 문제 우회
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''
os.environ['SSL_CERT_FILE'] = ''

import ssl
import urllib3
try:
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib3.disable_warnings()
except:
    pass

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.chart_analyzer import ChartAnalyzer
from src.news_researcher import NewsResearcher

def test_chart_analyzer():
    print("="*50)
    print("Testing ChartAnalyzer with 005930.KS (Samsung)")
    print("="*50)
    
    try:
        ca = ChartAnalyzer('005930.KS')
        result = ca.analyze()
        
        indicators = result['indicators']
        
        print("\n=== RSI ===")
        print(f"RSI: {indicators.get('RSI')}")
        print(f"RSI Signal: {indicators.get('RSI_Signal')}")
        
        print("\n=== MACD ===")
        print(f"MACD: {indicators.get('MACD')}")
        print(f"MACD Signal Line: {indicators.get('MACD_Signal_Line')}")
        print(f"MACD Cross: {indicators.get('MACD_Cross')}")
        
        print("\n=== Volume ===")
        print(f"Volume Ratio: {indicators.get('Volume_Ratio')}")
        print(f"Volume Signal: {indicators.get('Volume_Signal')}")
        
        print("\n=== Patterns ===")
        for p in result['patterns']:
            print(f"  - {p}")
        
        print("\n[OK] ChartAnalyzer test passed!")
        return True
        
    except Exception as e:
        import traceback
        print(f"[ERROR] ChartAnalyzer test failed: {e}")
        traceback.print_exc()
        return False

def test_news_researcher():
    print("\n" + "="*50)
    print("Testing NewsResearcher with 005930.KS (Samsung)")
    print("="*50)
    
    try:
        nr = NewsResearcher('005930.KS')
        result = nr.search_and_analyze()
        
        print(f"\nCompany Sector: {result['company_info'].get('sector')}")
        print(f"News count: {len(result.get('news', []))}")
        print(f"Risks detected: {len(result.get('risks', []))}")
        
        if result.get('news'):
            print("\nRecent News:")
            for news in result['news'][:3]:
                print(f"  - {news['title'][:50]}...")
        
        print("\n[OK] NewsResearcher test passed!")
        return True
        
    except Exception as e:
        print(f"[ERROR] NewsResearcher test failed: {e}")
        return False

if __name__ == "__main__":
    print("Stock Research - Feature Test")
    print("="*50)
    
    chart_ok = test_chart_analyzer()
    news_ok = test_news_researcher()
    
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"ChartAnalyzer (RSI/MACD/Volume): {'PASS' if chart_ok else 'FAIL'}")
    print(f"NewsResearcher (Crawling): {'PASS' if news_ok else 'FAIL'}")
