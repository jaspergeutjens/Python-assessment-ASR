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
        self.model.update_prices()
        self.view.show_prices(self.model.assets)

    def view_portfolio(self):
        self.model.update_prices()
        self.view.display_portfolio(self.model.get_portfolio_summary())
    
    def view_portfolio_calculation(self):
        self.model.update_prices()  # Always make sure prices are fresh
        level = input("Choose level to view weights (choose, pf for portfolio, ac for asset class, sec for sector): ").strip().lower()
        try:
            summary_df = self.model.get_portfolio_weights(level)  # Pass input to model
            self.view.display_weight_summary(summary_df, level)
        except ValueError as e:
            print(f"Error: {e}")

    def simulate_portfolio(self):
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