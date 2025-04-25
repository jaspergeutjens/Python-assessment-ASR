import yfinance as yf
import pandas as pd
import numpy as np

class PortfolioModel:
    def __init__(self):
        self.assets = []

    def add_asset(self, asset_data):
        self.assets.append(asset_data)

    def update_prices(self):
        for asset in self.assets:
            ticker = yf.Ticker(asset['ticker'])
            current_price = ticker.history(period='1d')['Close'].iloc[-1]
            asset['current_price'] = current_price
            asset['current_value'] = current_price * asset['quantity']

    def get_portfolio_summary(self):
        df = pd.DataFrame(self.assets)
        df['transaction_value'] = df['quantity'] * df['purchase_price']
        df['current_value'] = df['quantity'] * df['current_price']
        df['PnL'] = df['current_value'] - df['transaction_value']
        return df

    def simulate(self, years=15, simulations=10000):
        results = []
        for asset in self.assets:
            mu = 0.07  
            sigma = 0.15  
            S0 = asset['current_price']
            steps = years
            dt = 1
            paths = np.exp(np.cumsum((mu - 0.5 * sigma**2) * dt + sigma * np.random.randn(simulations, steps) * np.sqrt(dt), axis=1))
            final_values = S0 * paths[:, -1] * asset['quantity']
            results.append(final_values)
        total = np.sum(results, axis=0)
        return total
