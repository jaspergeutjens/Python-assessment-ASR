# Portfolio Tracker

## Overview

The **Portfolio Tracker** is a Python-based application that helps users manage and simulate their financial portfolio. It allows users to:

- Add assets to their portfolio
- View current and historical asset prices
- Simulate portfolio performance over 15 years
- View portfolio summaries, including risk measures

The program uses real-time financial data from Yahoo Finance and simulates asset price behavior using Geometric Brownian Motion (GBM).

---

## Files

- `main.py`: The entry point of the application. It initializes and runs the `PortfolioController`.
- `portfolio_controller.py`: The controller that handles user inputs and coordinates between the model and view.
- `portfolio_model.py`: Contains the logic for managing portfolio data, running simulations, and calculating risk measures.
- `portfolio_view.py`: Manages user interface and displays information about the portfolio, asset prices, and simulation results.

---

## Installation

1. Clone or download this repository.

2. Install required dependencies. Run the following command:

   pip install -r requirements.txt

3. To run the application, simply execute main.py, the CLI will automatically start.

4. To quit the application, simply choose the Quit option.

---

### Notes:

1. **Data Source**: The application uses **Yahoo Finance** (via the `yfinance` package) to fetch current and historical prices of assets. Make sure you have a working internet connection for the app to function properly.
2. **Simulations**: The simulation uses **Geometric Brownian Motion (GBM)** to model the future price behavior of assets. The portfolio simulation is based on a Monte Carlo method, running 100,000 simulations by default.
