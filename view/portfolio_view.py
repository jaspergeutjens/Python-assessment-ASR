import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from model.portfolio_model import PortfolioModel

class PortfolioView:
    def show_main_menu(self):
        print("\n=== Portfolio Tracker ===")
        print("1. Add Asset")
        print("2. View Current & Historical Prices")
        print("3. View Portfolio Overview")
        print("4. Display portfolio weights")
        print("5. Run Simulation")
        print("Q. Quit")

    def show_prices(self, assets):
        # print current price and plot price history of the asset
        seen = set()
        for asset in assets:
            ticker = asset['ticker']
            if ticker not in seen:
                seen.add(ticker)
                print(f"\n{ticker} - Current Price: €{asset['current_price']:.2f}")
                self.plot_price_history(ticker)

    def plot_price_history(self, ticker):
        # function that plots the price history
        data = yf.Ticker(ticker).history(period="1y")
        data['Close'].plot(title=f"{ticker} - 1 Year Price History")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid()
        plt.show()

    def display_portfolio(self, df: pd.DataFrame):
        # Displays the current portfolio
        print("\n=== Portfolio Overview ===")
        print(df)
        # Current portfolio value
        total_value = df['current_value'].sum()
        # Profit/loss of the trades that are made
        total_pnl = df['PnL'].sum()
        print(f"\nTotal Portfolio Value: €{total_value:,.2f}")
        print(f"\nTotal Portfolio PnL: €{total_pnl:,.2f}")

    def plot_simulation(self, simulation_results):
        # Function that plots the simulated portfolio values over the next 15 years
        plt.hist(simulation_results, bins=1000, alpha=0.7, color='skyblue', edgecolor='grey')
        plt.title(f"Simulated Portfolio Value Distribution")
        plt.xlabel("Portfolio Value (EUR)")
        plt.ylabel("Frequency")
        plt.grid()
        plt.show()
    
    def display_risk_measure(self, simulation_results, alpha, df: pd.DataFrame):
        # Current portfolio value
        current_value = df['current_value'].sum()
        # Risk measure, sort of similar to a VaR, which refers to a loss distribution
        adjusted_VaR = PortfolioModel.risk_measure(simulation_results, alpha)
        print(f"\nWith {100*alpha}% probability, your portfolio value in 15 years will not be smaller than {adjusted_VaR}.")
        print(f"Note that the current value of your portfolio is equal to €{current_value:,.2f}.")
        
    def display_weight_summary(self, summary_df, level):
        if level == 'pf':
            print(f"\n=== Portfolio Breakdown at portfolio level ===")
            print(summary_df.to_string(index=False))
        if level == 'ac':
            print(f"\n=== Portfolio Breakdown at asset class level ===")
            print(summary_df.to_string(index=False))
        if level == 'sec':
            print(f"\n=== Portfolio Breakdown at sector level ===")
            print(summary_df.to_string(index=False))