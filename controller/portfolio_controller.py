from model.portfolio_model import PortfolioModel
from view.portfolio_view import PortfolioView
import yfinance as yf

class PortfolioController:
    def __init__(self):
        self.model = PortfolioModel()
        self.view = PortfolioView()

    def run(self):
        while True:
            # Show the control window
            self.view.show_main_menu()
            choice = input("Please choose one of the options above by entering the corresponding number (or Q): ").strip()
            if choice == "1":
                self.add_asset()
            elif choice == "2":
                self.view_prices()
            elif choice == "3":
                self.view_portfolio()
            elif choice == "4":
                self.view_portfolio_calculation()
            elif choice == "5":
                self.simulate_portfolio()
            elif choice.lower() in {"q", "quit"}:
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please enter a correct value.")

    def add_asset(self):
        # asset_data = self.view.get_asset_input()
        while True:
            ticker = input("Please enter the ticker of the asset: ").upper()
            data = yf.Ticker(ticker).history(period="max")
            # Ensures that the user cannot enter an invalid ticker
            if data.empty:
                print("Invalid or non-existent ticker. Please enter a valid ticker.\n")
                continue  
            # If the ticker is valid, let the user enter asset and transaction information
            try:
                sector = input("Please enter the corresponding sector: ")
                asset_class = input("Please enter the corresponding asset class: ")
                quantity = float(input("Please enter the quantity: "))
                purchase_price = float(input("Please enter the purchase price: "))
                asset_data = {
                    'ticker': ticker,
                    'sector': sector,
                    'asset_class': asset_class,
                    'quantity': quantity,
                    'purchase_price': purchase_price
                }
                break
            except ValueError:
                print("Invalid numeric input. Please try again.\n")
                continue
        self.model.add_asset(asset_data)

    def view_prices(self):
        # Update asset prices
        self.model.update_prices()
        unique_tickers = list({asset['ticker'] for asset in self.model.assets})
        if not unique_tickers:
            print("No assets in the portfolio. Please add assets first.")
            return
        # Let the user choose which tickers to include in the price inspection
        while True:
            print("\nDo you want to inspect prices for:")
            print("1. One specific ticker")
            print("2. Multiple tickers")
            print("3. All tickers in the portfolio")
            choice = input("Enter 1, 2 or 3: ").strip()
            if choice in {"1", "2", "3"}:
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        # Display current price(s) and plot the historic price graph(s)
        if choice == "1":
            ticker = self.view.get_single_ticker_choice(unique_tickers)
            asset = next(asset for asset in self.model.assets if asset['ticker'] == ticker)
            self.view.display_current_price(ticker, asset['current_price'])
            self.view.plot_price_history(ticker)
        elif choice == "2":
            tickers = self.view.get_multiple_ticker_choices(unique_tickers)
            for ticker in tickers:
                asset = next(asset for asset in self.model.assets if asset['ticker'] == ticker)
                self.view.display_current_price(ticker, asset['current_price'])
            self.view.plot_multiple_price_histories(tickers)
        elif choice == "3":
            for ticker in unique_tickers:
                asset = next(asset for asset in self.model.assets if asset['ticker'] == ticker)
                self.view.display_current_price(ticker, asset['current_price'])
            self.view.plot_multiple_price_histories(unique_tickers)

    def view_portfolio(self):
        # View transactions in the portfolio
        self.model.update_prices()
        self.view.display_portfolio(self.model.get_portfolio_summary())
    
    def view_portfolio_calculation(self):
        # View portfolio with weigths
        self.model.update_prices()  # Always make sure prices are fresh
        level = input("Choose level to view weights (choose, pf for portfolio, ac for asset class, sec for sector): ").strip().lower()
        try:
            summary_df = self.model.get_portfolio_weights(level)  # Pass input to model
            self.view.display_weight_summary(summary_df, level)
        except ValueError as e:
            print(f"Error: {e}")

    def simulate_portfolio(self):
        # Perform a simulation of future portfolio value 
        self.model.update_prices()
        simulation_results = self.model.simulate()
        while True:
            try:
                alpha = float(input("Please enter the alpha/confidence level for the risk measure (e.g., 0.99 for 99% confidence): ").strip())
                if 0 < alpha < 1:
                    break
                else:
                    print("Alpha must be between 0 and 1. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number for alpha.")
        self.view.display_risk_measure(simulation_results, alpha, self.model.get_portfolio_summary())
        self.view.plot_simulation(simulation_results)