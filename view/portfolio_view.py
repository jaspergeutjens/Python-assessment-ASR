import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from model.portfolio_model import PortfolioModel

class PortfolioView:
    def show_main_menu(self):
        print("\n=== Portfolio Tracker ===")
        print("1. Add Asset")
        print("2. View Current & Historical Prices")
        print("3. View Transactions Overview")
        print("4. View Portfolio Overview (weigths)")
        print("5. Run Simulation")
        print("Q. Quit")

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
        print("\n=== Transactions Overview ===")
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
        print(f"\nWith {100*alpha}% probability, your portfolio value in 15 years will not be smaller than €{adjusted_VaR}.")
        print(f"Note that the current value of your portfolio is equal to €{current_value:,.2f}.")
        
    def display_weight_summary(self, summary_df, level):
        # Display portfolio including weigths
        if level == 'pf':
            print(f"\n=== Portfolio Breakdown at portfolio level ===")
            print(summary_df.to_string(index=False))
        if level == 'ac':
            print(f"\n=== Portfolio Breakdown at asset class level ===")
            print(summary_df.to_string(index=False))
        if level == 'sec':
            print(f"\n=== Portfolio Breakdown at sector level ===")
            print(summary_df.to_string(index=False))

    def get_single_ticker_choice(self, valid_tickers):
        # Get the single ticker for price inspection
        while True:
            ticker = input("Enter the ticker you'd like to inspect: ").upper().strip()
            if ticker in valid_tickers:
                return ticker
            print(f"'{ticker}' is not in your portfolio. Available tickers: {', '.join(valid_tickers)}")

    def get_multiple_ticker_choices(self, valid_tickers):
        # Get multiple tickers for price inspection
        while True:
            tickers_input = input("Enter tickers separated by commas (e.g. AAPL,MSFT,GOOGL): ").upper()
            tickers = [ticker.strip() for ticker in tickers_input.split(",") if ticker.strip()]
            if not tickers:
                print("No tickers entered. Please try again.")
            elif any(t not in valid_tickers for t in tickers):
                invalid = [t for t in tickers if t not in valid_tickers]
                print(f"Invalid tickers: {', '.join(invalid)}. Available: {', '.join(valid_tickers)}")
            elif len(tickers) > len(valid_tickers):
                print(f"You entered more tickers than are available in the portfolio. Max allowed: {len(valid_tickers)}")
            else:
                return tickers

    def display_current_price(self, ticker, price):
        print(f"\n{ticker} - Current Price: €{price:.2f}")

    def plot_multiple_price_histories(self, tickers):
        # Plot prices of multiple tickers jointly
        plt.figure(figsize=(10, 6))
        for ticker in tickers:
            data = yf.Ticker(ticker).history(period="1y")
            plt.plot(data.index, data['Close'], label=ticker)
        plt.title("Historical Prices - Last 1 Year")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plt.grid(True)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Tickers")
        plt.tight_layout(rect=[0, 0, 0.85, 1]) 
        plt.show()