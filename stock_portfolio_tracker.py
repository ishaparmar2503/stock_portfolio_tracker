import json
import requests
import os

# Constants
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'
API_URL = 'https://www.alphavantage.co/query'
PORTFOLIO_FILE = 'portfolio.json'

# Helper Functions
def load_portfolio():
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_portfolio(portfolio):
    with open(PORTFOLIO_FILE, 'w') as f:
        json.dump(portfolio, f, indent=4)

def fetch_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1min',
        'apikey': API_KEY
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    return data

# Core Functions
def add_stock(symbol, quantity, purchase_price, user_id):
    portfolio = load_portfolio()

    if user_id not in portfolio:
        portfolio[user_id] = []
    portfolio[user_id].append({
        'symbol': symbol,
        'quantity': quantity,
        'purchase_price': purchase_price
    })
    save_portfolio(portfolio)
    print(f"Added {quantity} shares of {symbol} at ${purchase_price} to {user_id}'s portfolio.")

def remove_stock(symbol, user_id):
    portfolio = load_portfolio()
    if user_id in portfolio:
        portfolio[user_id] = [stock for stock in portfolio[user_id] if stock['symbol'] != symbol]
        save_portfolio(portfolio)
        print(f"Removed {symbol} from {user_id}'s portfolio.")
    else:
        print(f"No portfolio found for user {user_id}.")

def view_portfolio(user_id):
    portfolio = load_portfolio()
    if user_id in portfolio:
        for stock in portfolio[user_id]:
            print(f"{stock['symbol']} - {stock['quantity']} shares @ ${stock['purchase_price']}")
    else:
        print(f"No portfolio found for user {user_id}.")

def get_real_time_data(symbol):
    data = fetch_stock_data(symbol)
    if 'Time Series (1min)' in data:
        latest_time = sorted(data['Time Series (1min)'].keys())[0]
        latest_data = data['Time Series (1min)'][latest_time]
        current_price = latest_data['4. close']
        print(f"Current price of {symbol} is ${current_price}")
    else:
        print(f"Failed to fetch data for {symbol}.")

# Command-Line Interface
def main():
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Get Real-Time Stock Data")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ")
            quantity = int(input("Enter quantity: "))
            purchase_price = float(input("Enter purchase price: "))
            user_id = input("Enter user ID: ")
            add_stock(symbol, quantity, purchase_price, user_id)
        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ")
            user_id = input("Enter user ID: ")
            remove_stock(symbol, user_id)
        elif choice == '3':
            user_id = input("Enter user ID: ")
            view_portfolio(user_id)
        elif choice == '4':
            symbol = input("Enter stock symbol: ")
            get_real_time_data(symbol)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

