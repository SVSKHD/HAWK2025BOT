 import json
from config import trading_config
# -------------------- CONFIGURATION -------------------- #
# Define trading configuration


# -------------------- TRADE CALCULATOR CLASS -------------------- #
class TradeCalculator:
    def __init__(self, instrument, start_price, current_price):
        if instrument not in trading_config:
            raise ValueError(f"Instrument {instrument} not found in config.")

        self.instrument = instrument
        self.start_price = start_price
        self.current_price = current_price
        self.pip_size = trading_config[instrument]["pip_size"]
        self.threshold = trading_config[instrument]["threshold"]
        self.direction = "NEUTRAL"  # Default direction

        self.trades_placed = {
            "status": "idle",
            "trade_placed_short": False,
            "trade_placed_long": False,
            "close_short_trades": False,
            "close_long_trades": False,
            "direction": self.direction,
            "thresholds_passed": 0,
            "pips_moved": 0
        }

    def calculate_trade_signal(self):
        # Reset all statuses
        self.trades_placed = {
            "status": "idle",
            "trade_placed_short": False,
            "trade_placed_long": False,
            "close_short_trades": False,
            "close_long_trades": False,
            "direction": self.direction,
            "thresholds_passed": 0,
            "pips_moved": 0
        }

        # Calculate price difference
        difference = self.current_price - self.start_price  

        # Determine direction
        if difference > 0:
            self.direction = "UP"
        elif difference < 0:
            self.direction = "DOWN"
        else:
            self.direction = "NEUTRAL"

        self.trades_placed["direction"] = self.direction

        # Compute pips moved
        pips_moved = round(abs(difference) / self.pip_size)
        self.trades_placed["pips_moved"] = pips_moved

        # Compute thresholds passed
        thresholds_passed = pips_moved // self.threshold  # Count how many thresholds reached
        self.trades_placed["thresholds_passed"] = thresholds_passed

        # Apply trade logic based on thresholds
        if thresholds_passed % 2 == 1:  # Odd thresholds: Place trade
            if self.direction == "UP":  # Uptrend → Place Long Trade
                self.trades_placed["status"] = "Place Long Trade"
                self.trades_placed["trade_placed_long"] = True
            elif self.direction == "DOWN":  # Downtrend → Place Short Trade
                self.trades_placed["status"] = "Place Short Trade"
                self.trades_placed["trade_placed_short"] = True
        elif thresholds_passed % 2 == 0 and thresholds_passed > 0:  # Even thresholds: Close trade
            if self.direction == "UP":  # Uptrend → Close Long Trade
                self.trades_placed["status"] = "Close Long Trades"
                self.trades_placed["close_long_trades"] = True
            elif self.direction == "DOWN":  # Downtrend → Close Short Trade
                self.trades_placed["status"] = "Close Short Trades"
                self.trades_placed["close_short_trades"] = True
        else:
            self.trades_placed["status"] = "Idle"

        return self.trades_placed

# -------------------- MAIN FUNCTION -------------------- #
if __name__ == "__main__":
    # Define trading parameters
    instrument = "EURUSD"
    start_price = 1.0000

    # Example 1: Prices moving UP
    current_prices_up = [1.0015, 1.0030, 1.0045]
    
    print("\n--- Trade Actions (UPTREND) ---")
    for price in current_prices_up:
        trade_calculator = TradeCalculator(instrument, start_price, price)
        result = trade_calculator.calculate_trade_signal()
        print(f"Start: {start_price}, Current: {price}, Trade: {json.dumps(result, indent=2)}")

    # Example 2: Prices moving DOWN
    current_prices_down = [0.9985, 0.9970, 0.9955]

    print("\n--- Trade Actions (DOWNTREND) ---")
    for price in current_prices_down:
        trade_calculator = TradeCalculator(instrument, start_price, price)
        result = trade_calculator.calculate_trade_signal()
        print(f"Start: {start_price}, Current: {price}, Trade: {json.dumps(result, indent=2)}")