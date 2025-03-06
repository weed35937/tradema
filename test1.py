import time
from tvDatafeed import TvDatafeed, Interval

# Initialize TradingView data feed (Anonymous or use credentials)
tv = TvDatafeed()

# Define symbol and exchange (Modify as needed)
symbol = "EMA"        # Replace with your desired stock/crypto pair
exchange = "TSX"      # Replace with the correct exchange (TSX, NASDAQ, FX, etc.)
interval = Interval.in_1_minute  # Real-time updates with 1-minute interval

def fetch_real_time_data():
    while True:
        try:
            # Fetch latest market data
            data = tv.get_hist(symbol=symbol, exchange=exchange, interval=interval, n_bars=1)

            # Print the latest price and EMA if available
            latest_price = data['close'].iloc[-1]
            print(f"Latest Price: {latest_price}")

            # If EMA needs to be calculated manually, use:
            if "ema" in data.columns:
                latest_ema = data["ema"].iloc[-1]
                print(f"Latest EMA: {latest_ema}")
            else:
                print("EMA not found in response. You might need to calculate it manually.")

        except Exception as e:
            print(f"Error fetching data: {e}")

        time.sleep(10)  # Adjust the refresh rate (10 seconds)

# Run the real-time fetch function
fetch_real_time_data()
