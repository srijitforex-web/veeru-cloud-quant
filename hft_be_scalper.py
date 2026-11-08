import pandas as pd
import numpy as np

def run_be_scalp_simulation(csv_path, initial_capital_inr=50000, lot_target=1.0):
    """
    Simulates the 1-Lot Daily Break-Even Scalping Loop on M1 Gold Data.
    Capital: 50,000 INR
    Target: 1.0 Lot cumulative per day via 0.01 micro-lots
    Rule: 1-3 pip SL, immediate BE lock after 1.5 pips in favor.
    """
    print(f"Loading historical M1 data from {csv_path}...")
    df = pd.read_csv(csv_path, sep='\t')
    
    # Standardize column names
    df.columns = [c.replace('<', '').replace('>', '') for c in df.columns]
    
    # Initialize tracking variables
    current_lots_today = 0.0
    account_balance = initial_capital_inr
    trades_executed = 0
    be_locked_trades = 0
    winning_trades = 0
    
    # Simulate micro-scalping logic across M1 bars
    for i in range(1, len(df)):
        open_price = df['OPEN'].iloc[i]
        high_price = df['HIGH'].iloc[i]
        low_price = df['LOW'].iloc[i]
        close_price = df['CLOSE'].iloc[i]
        
        # Micro-breakout condition (scalping momentum)
        price_delta = close_price - open_price
        
        if abs(price_delta) > 0.5: # Threshold for micro-scalp trigger
            trade_lots = 0.01
            entry = open_price
            
            # Simulate trade outcome based on M1 high/low reach
            if price_delta > 0: # Long scalp
                sl = entry - 2.0  # 2 pip SL
                be_trigger = entry + 1.5
                target = entry + 3.0
                
                if high_price >= be_trigger:
                    be_locked_trades += 1
                    if high_price >= target:
                        winning_trades += 1
                        account_balance += (target - entry) * 10 * trade_lots
                    else:
                        # Exited at Breakeven
                        pass
            else: # Short scalp
                sl = entry + 2.0
                be_trigger = entry - 1.5
                target = entry - 3.0
                
                if low_price <= be_trigger:
                    be_locked_trades += 1
                    if low_price <= target:
                        winning_trades += 1
                        account_balance += (entry - target) * 10 * trade_lots
                        
            current_lots_today += trade_lots
            trades_executed += 1

    print("\n--- HFT BE SCALPER BACKTEST RESULTS ---")
    print(f"Starting Capital: {initial_capital_inr} INR")
    print(f"Total Trades Simulated: {trades_executed}")
    print(f"Trades Secured to Break-Even: {be_locked_trades}")
    print(f"Total Cumulative Lots Traded: {current_lots_today:.2f}")
    print(f"Simulated Final Balance: {account_balance:.2f} INR")

if __name__ == "__main__":
    # Run test on sample dataset
    run_be_scalp_simulation('XAUUSD_M1_202609210100_202610220239.csv')
