import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import numpy as np

class PortfolioView:
    def show_main_menu(self):
        print("\n=== Portfolio Tracker ===")
        print("1. Add Asset")
        print("2. View Current & Historical Prices")
        print("3. View Portfolio Overview")
        print("4. Run Simulation")
        print("Q. Quit")

    def get_asset_input(self):
        while True:
            ticker = input("Please enter the ticker of the asset: ").upper()
            data = yf.Ticker(ticker).history(period="max")
            if data.empty:
                print("Invalid or non-existent ticker. Please enter a valid ticker.\n")
                continue  
            try:
                sector = input("Please enter the corresponding sector: ")
                asset_class = input("Please enter the corresponding asset Class: ")
                quantity = float(input("PLease enter the quantity: "))
                purchase_price = float(input("Please enter the purchase Price: "))
                return {
                    'ticker': ticker,
                    'sector': sector,
                    'asset_class': asset_class,
                    'quantity': quantity,
                    'purchase_price': purchase_price
                }
            except ValueError:
                print("Invalid numeric input. Please try again.\n")
                continue

    def show_prices(self, assets):
        seen = set()
        for asset in assets:
            ticker = asset['ticker']
            if ticker not in seen:
                seen.add(ticker)
                print(f"\n{ticker} - Current Price: €{asset['current_price']:.2f}")
                self.plot_price_history(ticker)

    def plot_price_history(self, ticker):
        data = yf.Ticker(ticker).history(period="1y")
        data['Close'].plot(title=f"{ticker} - 1 Year Price History")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.grid()
        plt.show()

    def display_portfolio(self, df: pd.DataFrame):
        print("\n=== Portfolio Overview ===")
        print(df)
        total_value = df['current_value'].sum()
        total_pnl = df['PnL'].sum()
        print(f"\nTotal Portfolio Value: €{total_value:,.2f}")
        print(f"\nTotal Portfolio PnL: €{total_pnl:,.2f}")

    def plot_simulation(self, simulation_results, plot_choice, alpha):
        VaR = np.percentile(simulation_results, (1 - alpha) * 100)
        ES = simulation_results[simulation_results <= VaR].mean()
        plt.hist(simulation_results, bins=100, alpha=0.7, color='skyblue', edgecolor='grey')

        if plot_choice == 'var':
            plt.axvline(VaR, color='red', linestyle='dashed', linewidth=1.3, label=f'VaR {int(alpha * 100)}%: €{VaR:,.2f}')
        elif plot_choice == 'es':
            plt.axvline(ES, color='green', linestyle='dashed', linewidth=1.3, label=f'ES {int(alpha * 100)}%: €{ES:,.2f}')
        
        plt.legend(loc='upper right', frameon=True, fontsize=10)
        plt.title(f"Simulated Portfolio Value Distribution ({int(alpha * 100)}% Confidence)")
        plt.xlabel("Portfolio Value (EUR)")
        plt.ylabel("Frequency")
        plt.grid(True)
        plt.tight_layout()
        plt.show()