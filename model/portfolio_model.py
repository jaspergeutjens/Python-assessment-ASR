import yfinance as yf
import pandas as pd
import numpy as np
# Note that the datetime package does not need to be included in requirements.txt
# This package is part of Python's standard library
from datetime import datetime, timedelta

class PortfolioModel:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset_data):
        # add asset data 
        self.assets.append(asset_data)

    def update_prices(self):
        # Determine current asset price and current value of trade, also store information
        for asset in self.assets:
            ticker = yf.Ticker(asset['ticker'])
            current_price = ticker.history(period='1d')['Close'].iloc[-1]
            asset['current_price'] = current_price
            asset['current_value'] = current_price * asset['quantity']

    def get_portfolio_summary(self):
        # Return portfolio information
        df = pd.DataFrame(self.assets)
        df['transaction_value'] = df['quantity'] * df['purchase_price']
        df['current_value'] = df['quantity'] * df['current_price']
        df['PnL'] = df['current_value'] - df['transaction_value']
        return df

    def simulate(self, years=15, simulations=100000):
        # Set a seed, this implies that it is assumed that the shocks to asset prices here are driven by the same Brownian Motion
        np.random.seed(42)
        unique_assets = {}
        for asset in self.assets:
            unique_assets.setdefault(asset["ticker"], {'quantity': 0, 'current_price': asset['current_price']})
            unique_assets[asset["ticker"]]['quantity'] += asset['quantity']
        # Simulate asset values
        results = np.zeros((simulations, len(unique_assets)))
        for idx, (ticker, data) in enumerate(unique_assets.items()):
            mu, sigma = PortfolioModel.estimate_mu_sigma(ticker)
            # Closed form solution of a Geometric Brownian motion at time T
            final_values = data['current_price'] * np.exp((mu - 0.5 * sigma**2) * years + sigma * np.sqrt(years) * np.random.randn(simulations))
            results[:, idx] = final_values * data['quantity']
        # Return the summed portfolio values
        return np.sum(results, axis=1).flatten()
        
    def estimate_mu_sigma(ticker):
        # Estimate mu and sigma of a specific asset based on historic averages
        end_date = datetime.today()
        # 5 years ago from today, approximately
        start_date = end_date - timedelta(days=5*365)  
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
        # Download price data
        df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True) 
        if df.empty:
            raise ValueError("No data downloaded. Check the ticker or dates.")
        prices = df['Close']
        arithmetic_returns = (prices / prices.shift(1)) - 1
        arithmetic_returns = arithmetic_returns.dropna()
        # Estimate daily drift and volatility
        mu_daily = arithmetic_returns.mean()
        sigma_daily = arithmetic_returns.std()
        # Annualize the drift and volatility (assuming 252 trading days)
        trading_days = 252
        mu_annual = float(mu_daily * trading_days)
        sigma_annual = float(sigma_daily * np.sqrt(trading_days))
        return mu_annual, sigma_annual
    
    def risk_measure(simulation_results, alpha):
        # Calculates a risk measure, sort of similar to a VaR, which refers to a loss distribution
        adjusted_VaR = np.percentile(simulation_results, (1 - alpha) * 100)
        return adjusted_VaR

    def get_portfolio_weights(self, level):
        df = pd.DataFrame(self.assets)
        total_value = df['current_value'].sum()
        # Grouping rows based on ticker, asset class or sector
        if level == "pf":
            grouped = df.groupby('ticker')['current_value'].sum().reset_index()
            grouped['weight'] = grouped['current_value'] / total_value
            return grouped[['ticker', 'current_value', 'weight']]
        elif level == "ac":
            grouped = df.groupby('asset_class')['current_value'].sum().reset_index()
            grouped['weight'] = grouped['current_value'] / total_value
            return grouped
        elif level == "sec":
            grouped = df.groupby('sector')['current_value'].sum().reset_index()
            grouped['weight'] = grouped['current_value'] / total_value
            return grouped
        else:
            raise ValueError("Invalid level. Choose 'pf', 'ac', or 'sec'.")