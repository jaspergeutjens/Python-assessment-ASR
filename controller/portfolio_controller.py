from model.portfolio_model import PortfolioModel
from view.portfolio_view import PortfolioView

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
        # Allows the user to specify the confidence level for the risk measure
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