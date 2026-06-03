import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import time

def fetch_naver_stock(ticker, days=365):
    """Fetch daily OHLCV from Naver Finance"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    url = f"https://finance.naver.com/item/sise_day.nhn"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    data = []
    page = 1
    max_pages = (days // 10) + 5
    
    while page <= max_pages:
        params = {
            'code': ticker,
            'page': page
        }
        
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            rows = soup.select('table.type2 tr')
            if not rows:
                break
            
            found_date = False
            for row in rows:
                cols = row.find_all('td')
                if len(cols) < 7:
                    continue
                
                date_str = cols[0].get_text(strip=True)
                if not date_str or date_str == '날짜':
                    continue
                
                try:
                    date_obj = datetime.strptime(date_str, '%Y.%m.%d')
                except ValueError:
                    continue
                
                if date_obj < start_date:
                    found_date = True
                    continue
                
                if date_obj > end_date:
                    continue
                
                try:
                    data.append({
                        'date': date_obj.strftime('%Y-%m-%d'),
                        'close': float(cols[1].get_text(strip=True).replace(',', '')),
                        'open': float(cols[3].get_text(strip=True).replace(',', '')),
                        'high': float(cols[4].get_text(strip=True).replace(',', '')),
                        'low': float(cols[5].get_text(strip=True).replace(',', '')),
                        'volume': int(cols[6].get_text(strip=True).replace(',', ''))
                    })
                except (ValueError, IndexError):
                    continue
            
            if found_date:
                break
                
            page += 1
            time.sleep(0.3)
            
        except Exception as e:
            print(f"Error fetching {ticker} page {page}: {e}")
            break
    
    # Sort by date and deduplicate
    seen = set()
    unique = []
    for row in sorted(data, key=lambda x: x['date']):
        if row['date'] not in seen:
            seen.add(row['date'])
            unique.append(row)
    
    return unique

def fetch_all_tickers():
    tickers = ['005930', '000660', '005380', '035420', '035720', '012330', '051910', '068270', '206640']
    all_data = {}
    
    for ticker in tickers:
        print(f"Fetching {ticker}...")
        stock_data = fetch_naver_stock(ticker, days=365)
        all_data[ticker] = stock_data
        print(f"  -> {len(stock_data)} days")
        time.sleep(0.5)
    
    # Save to stock_data.json
    output = {
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'tickers': all_data
    }
    
    with open('stock_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False)
    
    print(f"Saved stock_data.json with {len(tickers)} tickers")

if __name__ == '__main__':
    fetch_all_tickers()
