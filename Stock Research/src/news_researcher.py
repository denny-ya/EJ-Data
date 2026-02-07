# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import yfinance as yf
from urllib.parse import quote

class NewsResearcher:
    def __init__(self, ticker):
        # Remove '.KS' or '.KQ' for Naver Finance
        self.code = ticker.split('.')[0]
        self.ticker = ticker

    def search_and_analyze(self):
        """
        Searches for news, company info, and market trends.
        Returns a dictionary with comprehensive research data.
        """
        print(f"Searching news for {self.ticker} (Code: {self.code})...")
        
        # 1. Company Vision (Business Summary)
        company_info = self._fetch_company_info()
        
        # 2. News & Risk Analysis
        news_items = self._fetch_naver_news(query=self.code) # Search by code
        risks = self._analyze_risks(news_items)
        
        # 3. Market Trend (Sector News)
        sector_trend = "N/A"
        global_trend = []
        policy_news = []
        brokerage_reports = []
        
        if company_info.get('sector'):
            sector = company_info['sector']
            sector_trend = self._fetch_sector_news(sector)
            global_trend = self._fetch_global_market_news(sector)
            policy_news = self._fetch_policy_news(sector)
        
        # 4. Brokerage Reports
        # Search query: "Name + 목표주가" (Target Price)
        # Note: self.ticker might be '005930.KS', we want the name if possible.
        # But for now we use the code which works decently on finance search.
        brokerage_reports = self._fetch_brokerage_reports()

        return {
            "company_info": company_info,
            "news": news_items,
            "risks": risks,
            "sector_trend": sector_trend,
            "global_trend": global_trend,
            "policy_news": policy_news,
            "brokerage_reports": brokerage_reports
        }

    def _fetch_company_info(self):
        try:
            stock = yf.Ticker(self.ticker)
            info = stock.info
            return {
                "summary": info.get('longBusinessSummary') or info.get('businessSummary') or "No summary available.",
                "sector": info.get('sector') or info.get('industry') or "Unknown"
            }
        except Exception as e:
            print(f"Error fetching company info: {e}")
            return {"summary": "Error fetching data", "sector": "Unknown"}

    def _fetch_sector_news(self, sector_keyword):
        # " 전망"
        return self._search_naver_news_by_keyword(f"{sector_keyword} \uc804\ub9dd", limit=3)

    def _fetch_global_market_news(self, sector_keyword):
        # "미국 " + keyword + " 이슈"
        return self._search_naver_news_by_keyword(f"\ubbf8\uad6d {sector_keyword} \uc774\uc288", limit=3)

    def _fetch_policy_news(self, sector_keyword):
        # " 정부 정책"
        return self._search_naver_news_by_keyword(f"{sector_keyword} \uc815\ubd80 \uc815\ucc45", limit=3)

    def _fetch_brokerage_reports(self):
        # " 목표주가 리포트"
        return self._search_naver_news_by_keyword(f"{self.code} \ubaa9\ud45c\uc8fc\uac00 \ub9ac\ud3ec\ud2b8", limit=3)

    def _search_naver_news_by_keyword(self, keyword, limit=3):
        
        # Use English to Korean mapping (using unicode escapes)
        sector_map = {
            "Technology": "\ubc18\ub3c4\uccb4 IT", # 반도체 IT
            "Financial Services": "\uae08\uc735", # 금융
            "Healthcare": "\ubc14\uc774\uc624 \ud5ec\uc2a4\ucf00\uc5b4", # 바이오 헬스케어
            "Consumer Cyclical": "\uc18c\ube44\uc7ac", # 소비재
            "Communication Services": "\ud1b5\uc2e0" # 통신
        }
        
        for eng, kor in sector_map.items():
            if eng in keyword:
                keyword = keyword.replace(eng, kor)

        # Naver Finance uses EUC-KR encoding for search queries
        encoded_keyword = quote(keyword.encode('euc-kr'))
        url = f"https://finance.naver.com/news/news_search.naver?q={encoded_keyword}"
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            # We construct URL manually, so no params dict needed for 'q'
            response = requests.get(url, headers=headers)
            response.encoding = 'euc-kr' 
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            news_list = []
            
            # Naver Finance Search Results Structure
            # <dl class="newsList"> ... <dt class="articleSubject"><a ...>
            subjects = soup.select('.articleSubject a')
            
            for subject in subjects[:limit]:
                title = subject.text.strip()
                link = subject['href']
                if not link.startswith('http'):
                    link = "https://finance.naver.com" + link
                    
                news_list.append({
                    "title": title,
                    "link": link
                })
            
            if not news_list:
                print(f"Warning: No results found for '{keyword}'.")
                
            return news_list
        except Exception as e:
            print(f"Error searching {keyword}: {e}")
            return []

    def _fetch_naver_news(self, query=None):
        # Naver Finance News URL (focused on specific stock code)
        url = f"https://finance.naver.com/item/news_news.naver?code={self.code}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            news_list = []
            # Typical structure for Naver Finance news list
            # Note: This selector might change, need to be robust
            articles = soup.select('.type5 tbody tr')
            
            for article in articles:
                title_tag = article.select_one('.title a')
                date_tag = article.select_one('.date')
                
                if title_tag and date_tag:
                    title = title_tag.text.strip()
                    link = "https://finance.naver.com" + title_tag['href']
                    date = date_tag.text.strip()
                    
                    news_list.append({
                        "title": title,
                        "link": link,
                        "date": date
                    })
                    
                    if len(news_list) >= 10: # Limit to 10 items
                        break
            
            return news_list
            
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def _analyze_risks(self, news_items):
        risk_keywords = ["하락", "급락", "악재", "손실", "적자", "둔화", "우려", "불황", "경고", "제재", "소송"]
        detected_risks = []

        for item in news_items:
            title = item['title']
            for keyword in risk_keywords:
                if keyword in title:
                    detected_risks.append({
                        "description": f"Risk detected in news: {title}",
                        "source": item['link'],
                        "keyword": keyword
                    })
                    break # One risk per article is enough
        
        return detected_risks
