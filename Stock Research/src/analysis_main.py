import argparse
import os
from chart_analyzer import ChartAnalyzer
from news_researcher import NewsResearcher
from report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description="Stock Analysis System")
    parser.add_argument("ticker", type=str, help="Stock ticker (e.g., 005930.KS)")
    args = parser.parse_args()

    ticker = args.ticker
    print(f"Starting analysis for {ticker}...")

    # 1. Chart Analysis
    chart_analyzer = ChartAnalyzer(ticker)
    chart_data = chart_analyzer.analyze()
    print("Chart analysis completed.")

    # 2. News & Risk Research
    news_researcher = NewsResearcher(ticker)
    news_data = news_researcher.search_and_analyze()
    print("News research completed.")

    # 3. Report Generation
    report_generator = ReportGenerator(ticker)
    report_path = report_generator.generate(chart_data, news_data)
    print(f"Report generated at: {report_path}")

if __name__ == "__main__":
    main()
