import requests
import time

# Define the symbol, interval, and limit for the API request
symbol = "BTC-USDT"  # Example trading pair
interval = "1h"  # Timeframe: 1-hour candles
limit = 100  # Number of candles to fetch per request

# Correct API URL (Ensure the endpoint is correct from BingX documentation)
url = f"https://openapi.bingx.com/swap/v3/quote/klines?symbol={symbol}&interval={interval}&limit={limit}"

# Function to fetch the data from the API
def fetch_data(url):
    try:
        print(f"Sending request to URL: {url}")
        # Sending GET request to the API with a timeout
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()  # Will raise HTTPError for bad responses

        # Check if the response contains 'data'
        data = response.json()
        if 'data' in data:
            return data['data']
        else:
            print("Error: 'data' key not found in the response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except requests.exceptions.SSLError as ssl_err:
        print(f"SSL Error: {ssl_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None

# Main function to continuously fetch data and print real-time results
def fetch_and_display_real_time_data(url, interval=20):
    while True:
        # Fetch data from the API
        data = fetch_data(url)
        
        if data:
            print(f"Data fetched successfully: {data[:1]}")  # Display first data point
        else:
            print("No data received.")
        
        # Wait for the next cycle (delay can be adjusted)
        print("\nWaiting for next update...\n")
        time.sleep(interval)  # Sleep for the interval (e.g., 20 seconds)

# Start fetching and displaying data in real-time
fetch_and_display_real_time_data(url, interval=20)  # Update every 20 seconds