import yfinance as yf

nvidia_stock = yf.Ticker("NVDA")
nvidia_info = nvidia_stock.info

print("NVIDIA Stock Information:")
for key, value in nvidia_info.items():
    print(f"{key}: {value}")