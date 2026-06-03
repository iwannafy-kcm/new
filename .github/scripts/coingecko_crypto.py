import requests
import json
from datetime import datetime, timezone
import time

COINS = {
    'btc': 'BTCUSDT',
    'eth': 'ETHUSDT',
    'bnb': 'BNBUSDT',
    'sol': 'SOLUSDT',
    'xrp': 'XRPUSDT',
    'ada': 'ADAUSDT',
    'avax': 'AVAXUSDT',
    'dot': 'DOTUSDT',
    'link': 'LINKUSDT',
    'matic': 'MATICUSDT'
}

COIN_META = {
    'bitcoin': {'name': 'Bitcoin', 'symbol': 'btc'},
    'ethereum': {'name': 'Ethereum', 'symbol': 'eth'},
    'binancecoin': {'name': 'BNB', 'symbol': 'bnb'},
    'solana': {'name': 'Solana', 'symbol': 'sol'},
    'ripple': {'name': 'XRP', 'symbol': 'xrp'},
    'cardano': {'name': 'Cardano', 'symbol': 'ada'},
    'avalanche-2': {'name': 'Avalanche', 'symbol': 'avax'},
    'polkadot': {'name': 'Polkadot', 'symbol': 'dot'},
    'chainlink': {'name': 'Chainlink', 'symbol': 'link'},
    'matic-network': {'name': 'Polygon', 'symbol': 'matic'}
}

def fetch_binance_kline(symbol, interval='1d', limit=365):
    url = 'https://api.binance.com/api/v3/klines'
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    prices = []
    volumes = []
    for k in data:
        t = int(k[0])
        prices.append([t, float(k[4])])
        volumes.append([t, float(k[5])])
    return prices, volumes

def fetch_binance_meta(symbol):
    url = 'https://api.binance.com/api/v3/ticker/24hr'
    params = {'symbol': symbol}
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    d = r.json()
    return {
        'price': float(d.get('lastPrice', 0)),
        'change_24h': float(d.get('priceChangePercent', 0)),
        'volume': float(d.get('volume', 0)),
        'high': float(d.get('highPrice', 0)),
        'low': float(d.get('lowPrice', 0))
    }

def build():
    out = {'updated_at': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC'), 'coins': {}}

    for sym, binance_symbol in COINS.items():
        print(f'Fetching {sym} ({binance_symbol})...')
        try:
            prices, volumes = fetch_binance_kline(binance_symbol, limit=365)
            meta = fetch_binance_meta(binance_symbol)
            coin_meta = next((v for v in COIN_META.values() if v['symbol'] == sym), {'name': sym, 'symbol': sym})
            out['coins'][sym] = {
                'id': sym,
                'name': coin_meta['name'],
                'symbol': coin_meta['symbol'],
                'prices': prices,
                'volumes': volumes,
                'current_price': meta['price'],
                'change_24h': meta['change_24h'],
                'change_7d': None,
                'market_cap': None,
                'circulating_supply': None,
                'total_supply': None,
                'max_supply': None
            }
            print(f'  -> {len(prices)} points')
        except Exception as e:
            print(f'  -> error: {e}')
        time.sleep(0.15)

    with open('crypto_data.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False)
    print(f'Saved crypto_data.json with {len(out["coins"])} coins')

if __name__ == '__main__':
    build()
