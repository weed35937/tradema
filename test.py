import requests

# TradingView EMA request URL
url = "https://www.tradingview.com/conversation-status/"

# Query parameters extracted from your request
params = {
    "_rand": "0.020576634749572387",
    "offset": "0",
    "room_id": "general",
    "stat_symbol": "TSX:EMA",
    "is_private": ""
}

# Headers copied from the browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Referer": "https://www.tradingview.com/symbols/TSX-EMA/",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Requested-With": "XMLHttpRequest",
    "X-Language": "en",
    "Cookie": "cookiePrivacyPreferenceBannerProduction=notApplicable; _ga=GA1.1.219009804.1741203565; cookiesSettings={'analytics':true,'advertising':true}; _gcl_au=1.1.1266539189.1741206223; device_t=a180S0JnOjA.PJJCWWriAy_7E0rsdT3tDjGPA0BknygdCAnRjMVql4g; sessionid=b7vsk3hup53fv2eefipgibp9ilmbzuwi; sessionid_sign=v3:akiTfnlC/kBKRBQBz6NMn/iGUrDhdcEHJfQE8is5OFI=; png=e2a52ffb-1af7-4703-a0aa-8bd020da03ee; etg=e2a52ffb-1af7-4703-a0aa-8bd020da03ee; cachec=e2a52ffb-1af7-4703-a0aa-8bd020da03ee; tv_ecuid=e2a52ffb-1af7-4703-a0aa-8bd020da03ee"
}

# Send GET request
response = requests.get(url, headers=headers, params=params)

# Print response (check if successful)
if response.status_code == 200:
    print(response.json())  # Assuming JSON response
else:
    print(f"Failed to fetch data: {response.status_code}")
    print(response.text)
