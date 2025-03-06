import time
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import itertools

# Initialize TradingView API
tv = TvDatafeed()

# Predefined symbols and their corresponding exchanges
symbol_exchange_map = {
    "BTCUSD": "BINANCE",
    "ETHUSD": "BINANCE",
    "AAPL": "NASDAQ",
    "TSLA": "NASDAQ",
    "EURUSD": "FX",
    "GBPUSD": "FX",
    "SPX": "SPX",
    "EMA": "TSX"  # Example stock on TSX
}

# Store last price for comparison
last_price = None
fetching = False  # Control fetching thread
loading_animation = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

# Available EMA periods
ema_periods = [3, 5, 13, 50]

def update_exchange(event):
    selected_symbol = symbol_var.get()
    exchange_var.set(symbol_exchange_map[selected_symbol])  # Auto-set exchange

# Function to calculate EMA manually
def calculate_ema(data, period):
    return data['close'].ewm(span=period, adjust=False).mean()

# Function to fetch real-time data
def fetch_real_time_data():
    global last_price, fetching
    symbol = symbol_var.get()
    exchange = exchange_var.get()
    period = int(ema_period_var.get())
    
    if not symbol or not exchange:
        messagebox.showerror("Error", "Please select both Symbol and Exchange.")
        return

    fetch_button.config(state=DISABLED)
    stop_button.config(state=NORMAL)
    fetching = True

    def fetch_loop():
        global last_price
        while fetching:
            try:
                data = tv.get_hist(symbol=symbol, exchange=exchange, interval=Interval.in_1_minute, n_bars=50)

                if data is not None and not data.empty:
                    latest_price = data['close'].iloc[-1]

                    data[f'ema_{period}'] = calculate_ema(data, period=period)
                    
                    latest_ema = data[f'ema_{period}'].iloc[-1]
                    
                    result_label.config(text=f"Latest Price: {latest_price} {next(loading_animation)}\nEMA ({period}): {latest_ema}")
                    
                    plot_graph(data, period)
                    
                    if last_price is not None:
                        if latest_price > last_price:
                            result_label.config(bootstyle="success")
                        elif latest_price < last_price:
                            result_label.config(bootstyle="danger")
                        else:
                            result_label.config(bootstyle="info")
                    last_price = latest_price
                else:
                    result_label.config(text="No data received. Check your inputs.", bootstyle="warning")
            except Exception as e:
                result_label.config(text=f"Error: {str(e)}", bootstyle="danger")
            time.sleep(1)

    threading.Thread(target=fetch_loop, daemon=True).start()

def stop_fetching():
    global fetching
    fetching = False
    fetch_button.config(state=NORMAL)
    stop_button.config(state=DISABLED)
    result_label.config(text="Fetching stopped.", bootstyle="secondary")

def plot_graph(data, period):
    ax.clear()
    ax.plot(data.index, data['close'], label='Close Price', color='white', linewidth=2)
    ax.plot(data.index, data[f'ema_{period}'], label=f'EMA {period}', color='yellow', linestyle='dashed')
    ax.set_title("Market Price & EMA Trends", fontsize=12, color='white')
    ax.legend()
    ax.grid(True, linestyle='dotted')
    ax.figure.canvas.draw()

def toggle_theme():
    current_theme = root.style.theme_use()
    new_theme = "darkly" if current_theme == "superhero" else "superhero"
    root.style.theme_use(new_theme)

root = ttk.Window(themename="superhero")
root.title("💎 Real-Time TradingView Fetcher")
root.geometry("700x600")

title_label = ttk.Label(root, text="📈 Real-Time Market Data", font=("Arial", 18, "bold"), bootstyle="primary")
title_label.pack(pady=10)

symbol_var = ttk.StringVar()
symbol_dropdown = ttk.Combobox(root, textvariable=symbol_var, values=list(symbol_exchange_map.keys()), state="readonly")
symbol_dropdown.pack(pady=5)
symbol_dropdown.bind("<<ComboboxSelected>>", update_exchange)

exchange_var = ttk.StringVar()
exchange_dropdown = ttk.Combobox(root, textvariable=exchange_var, state="readonly")
exchange_dropdown.pack(pady=5)

ema_period_var = ttk.StringVar(value=str(ema_periods[0]))
ema_period_dropdown = ttk.Combobox(root, textvariable=ema_period_var, values=[str(p) for p in ema_periods], state="readonly")
ema_period_dropdown.pack(pady=5)

fetch_button = ttk.Button(root, text="🚀 Fetch Data", bootstyle="primary", command=fetch_real_time_data)
fetch_button.pack(pady=5)
stop_button = ttk.Button(root, text="🛑 Stop Fetching", bootstyle="danger", command=stop_fetching, state=DISABLED)
stop_button.pack(pady=5)

result_label = ttk.Label(root, text="📊 Select a symbol and click Fetch", font=("Arial", 14, "bold"), bootstyle="info")
result_label.pack(pady=10)

fig, ax = plt.subplots(figsize=(6, 3), facecolor='#2c3e50')
fig.patch.set_alpha(0)
ax.set_facecolor('#2c3e50')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

toggle_button = ttk.Button(root, text="🌙 Toggle Dark Mode", bootstyle="secondary", command=toggle_theme)
toggle_button.pack(pady=5)

symbol_var.set(list(symbol_exchange_map.keys())[0])
update_exchange(None)

root.mainloop()
