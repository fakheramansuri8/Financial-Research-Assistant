from crewai.tools import BaseTool
import yfinance as yf


class FinancialDataTool(BaseTool):
    name: str = "Financial Data"
    description: str = "Get key financial metrics for a company ticker symbol"

    def _run(self, ticker: str) -> str:
        """
        Retrieve financial data for a given ticker symbol.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'TLS.AX')
            
        Returns:
            String containing formatted financial metrics
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract key metrics with safe defaults
            market_cap = info.get('marketCap', 'N/A')
            if market_cap and isinstance(market_cap, (int, float)):
                market_cap = f"${market_cap:,.2f}"
            
            pe_ratio = info.get('trailingPE', 'N/A')
            if pe_ratio and isinstance(pe_ratio, (int, float)):
                pe_ratio = f"{pe_ratio:.2f}"
            
            revenue = info.get('totalRevenue', 'N/A')
            if revenue and isinstance(revenue, (int, float)):
                revenue = f"${revenue:,.2f}"
            
            profit_margin = info.get('profitMargins', 'N/A')
            if profit_margin and isinstance(profit_margin, (int, float)):
                profit_margin = f"{profit_margin * 100:.2f}%"
            
            week_high = info.get('fiftyTwoWeekHigh', 'N/A')
            if week_high and isinstance(week_high, (int, float)):
                week_high = f"${week_high:.2f}"
            
            week_low = info.get('fiftyTwoWeekLow', 'N/A')
            if week_low and isinstance(week_low, (int, float)):
                week_low = f"${week_low:.2f}"
            
            current_price = info.get('currentPrice', 'N/A')
            if current_price and isinstance(current_price, (int, float)):
                current_price = f"${current_price:.2f}"
            
            return f"""
Company: {info.get('longName', ticker)}
Ticker: {ticker}
Sector: {info.get('sector', 'N/A')}
Industry: {info.get('industry', 'N/A')}

Key Financial Metrics:
- Current Price: {current_price}
- Market Cap: {market_cap}
- P/E Ratio: {pe_ratio}
- Revenue (TTM): {revenue}
- Profit Margin: {profit_margin}
- 52-Week High: {week_high}
- 52-Week Low: {week_low}
- Beta: {info.get('beta', 'N/A')}
- Dividend Yield: {info.get('dividendYield', 'N/A')}
            """.strip()
            
        except Exception as e:
            return f"Error fetching financial data for {ticker}: {str(e)}"
