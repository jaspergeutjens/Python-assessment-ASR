from model.portfolio_model import PortfolioModel
from view.portfolio_view import PortfolioView

class PortfolioController:
    def __init__(self):
        self.model = PortfolioModel()
        self.view = PortfolioView()

    def run(self):
        while True:
            self.view.show_main_menu()
            choice = input("Please choose one of the options above by entering the corresponding number (or Q): ").strip()
            if choice == "1":
                self.add_asset()
            elif choice == "2":
                self.view_prices()
            elif choice == "3":
                self.view_portfolio()
            elif choice == "4":
                self.simulate_portfolio()
            elif choice.lower() in {"q", "quit"}:
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please enter a correct value.")

    def add_asset(self):
        asset_data = self.view.get_asset_input()
        self.model.add_asset(asset_data)

    def view_prices(self):
        self.model.update_prices()
        self.view.show_prices(self.model.assets)

    def view_portfolio(self):
        self.model.update_prices()
        self.view.display_portfolio(self.model.get_portfolio_summary())

    def simulate_portfolio(self):
        self.model.update_prices()
        simulation_results = self.model.simulate()

        while True:
            plot_choice = input("Which risk measure do you want to use, Value at Risk or Expected Shortfall? (Enter 'VaR' or 'ES'): ").strip().lower()
            if plot_choice in {'var', 'es'}:
                break
            else:
                print("Invalid choice. Please enter 'VaR' or 'ES'.")
        while True:
            try:
                alpha = float(input("Please enter the alpha for VaR/ES (e.g., 0.99 for 99% confidence): ").strip())
                if 0 < alpha < 1:
                    break
                else:
                    print("Alpha must be between 0 and 1. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number for alpha.")

        self.view.plot_simulation(simulation_results, plot_choice, alpha)