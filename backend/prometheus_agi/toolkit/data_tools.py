import yfinance as yf
from .base_tool import BaseTool

class StockPriceFetcher(BaseTool):
    name = "stock_price_fetcher"
    description = "Fetches the latest stock price and key metrics for a given stock ticker."
    def run(self, ticker: str) -> dict:
        print(f"  > Fetching stock data for {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return {
                "ticker": ticker,
                "price": info.get("currentPrice"),
                "day_high": info.get("dayHigh"),
                "day_low": info.get("dayLow"),
                "volume": info.get("volume"),
            }
        except Exception as e:
            return {"error": f"Could not fetch data for ticker {ticker}: {e}"}