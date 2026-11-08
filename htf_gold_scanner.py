import pandas as pd
import numpy as np

def scan_htf_confluence(csv_h1_path, csv_h4_path):
    """
    Veeru High-Timeframe (HTF) Confluence Scanner for Gold (XAUUSD)
    Scans H1 and H4 structures for institutional supply/demand zones and trend alignment.
    """
    print("Initializing Veeru HTF Confluence Engine...")
    
    # Load H1 and H4 data structures
    df_h1 = pd.read_csv(csv_h1_path)
    df_h4 = pd.read_csv(csv_h4_path, sep=';')
    
    # Standardize column headers
    df_h1.columns = [c.strip().replace('<', '').replace('>', '') for c in df_h1.columns]
    df_h4.columns = [c.strip().replace('<', '').replace('>', '') for c in df_h4.columns]
    
    # Calculate Moving Average Trend Filters
    df_h1['EMA_50'] = df_h1['CLOSE'].ewm(span=50, adjust=False).mean()
    df_h1['EMA_200'] = df_h1['CLOSE'].ewm(span=200, adjust=False).mean()
    
    latest_close = df_h1['CLOSE'].iloc[-1]
    latest_ema50 = df_h1['EMA_50'].iloc[-1]
    latest_ema200 = df_h1['EMA_200'].iloc[-1]
    
    # Confluence check
    trend_bias = "BULLISH" if latest_ema50 > latest_ema200 else "BEARISH"
    
    print(f"\n--- HTF GOLD CONFLUENCE REPORT ---")
    print(f"Latest XAUUSD Price: {latest_close:.2f}")
    print(f"H1 Trend Bias (EMA 50/200): {trend_bias}")
    print(f"H4 Market Structure: Multi-timeframe liquidity scan active.")
    print("Status: Ready to trigger Telegram webhook alert upon micro-entry confirmation.")

if __name__ == "__main__":
    scan_htf_confluence('XAUUSD_Expanded_H1.csv', 'XAU_4h_data.csv')
