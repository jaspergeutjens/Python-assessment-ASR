from controller.portfolio_controller import PortfolioController

def main():
    print("Portfolio tracker has opened.")
    controller = PortfolioController()
    controller.run()

if __name__ == "__main__":
    main()