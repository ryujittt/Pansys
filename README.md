# Pansys
Pansys is a desktop application that allows users to fetch cryptocurrency market data and visualize it using advanced plotting techniques. It fetches historical or real-time OHLCV data  exchange, performs some technical analysis, and visualizes the data in a candlestick chart with weighted price modifications.

# Functionality 
The goal of this app is to estimate a price based on a given period, using the close and volume from the historical data frame. An approximation to the actual price is computed using polynomial regression, which accounts for the actual price and whether the traded volume at a given level is reasonable.

Regions where the price deviates too far from the calculated curve indicate that the price is either too high or too low for a long or short position. When the short-period estimated price (red curve) crosses above or below the long-period estimated price (green curve), it signals that the trend is entering a strong momentum phase.

# Key Features:
Fetch Market Data: Fetch historical or real-time market data (OHLCV) .

User Inputs: Allows the user to input parameters like trading symbol (e.g., ETH/USDT), timeframe (e.g., 5m), short and long window for calculations, and sample size.

Real-Time Processing: The application processes the fetched data in real-time and computes the weighted price based on volume and price differences.

Candlestick Chart with Indicators: The application uses mplfinance to plot the candlestick chart along with weighted price indicators (short and long).

EMA Option: Option to include Exponential Moving Averages (EMA) in the plot for further technical analysis.

Session Plotting: The application can plot vertical lines on the chart for specific session times (e.g., 7 AM, 1 PM, etc.).

# Main Features & Workflow:
User Input:

Symbol: The trading pair (e.g., ETH/USDT).

Timeframe: The time period for each candlestick (e.g., 5m for 5 minutes).

Short and Long: User-defined parameters for short and long windows used in calculating weighted prices.

Sample Size: How many data points to use for analysis.

Historic or Real-Time Data: Option to fetch either historic or real-time data.

# Data Fetching:

The program fetches OHLCV data from Binance using the ccxt library, based on user inputs for the symbol, timeframe, and sample size.

Weighted Price Calculation:

A weighted price is calculated using a custom formula that considers both the volume and price differences.

# Data Plotting:

Candlestick Chart: The program plots a candlestick chart of the OHLCV data using mplfinance.

Weighted Prices: The weighted price values are plotted as additional plots on top of the candlestick chart.

Session Indicators: Vertical lines are drawn on the chart for specific session times (7 AM, 1 PM, etc.).

# Save the Plot:

The final chart is saved as a PNG file (weighted_price_graph.png).

# Dependencies:
PyQt5: For the GUI.

ccxt: For fetching cryptocurrency market data from exchanges like Binance.

mplfinance: For plotting financial charts (OHLCV).

numpy and pandas: For data manipulation and calculations.

matplotlib: For plotting graphs.


# Example Workflow:
Input Symbol: ETH/USDT

Input Timeframe: 5m

Input Short: 75

Input Long: 100

Input Sample: 75

Check "EMA" and "HISTORIC" if needed.

Click Start to see the weighted price graph plotted and saved as a PNG file.

# Disclaimer:

This app is intended for research purposes only. The developers do not take any responsibility for any financial losses or damages resulting from the use of this app. Users are advised to make their own independent decisions and conduct thorough research before taking any actions based on the information provided by this app.

Pansys Project. All rights reserved.

Open-source code, developed by [CHAKRAR ABDELMALIK].
