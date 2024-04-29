# import the libraries that we going to use for the analysis
import pandas as pd
import numpy as np
from tradingview_ta import TA_Handler, Interval, Exchange
import yfinance as yf
import mplfinance as mpf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

tickers = [ 'ADANIENT',
'ADANIPORTS',
'APOLLOHOSP',
'ASIANPAINT',
'AXISBANK',
'BAJAJ_AUTO',
'BAJFINANCE',
'BAJAJFINSV',
'BPCL',
'BHARTIARTL',
'BRITANNIA',
'CIPLA',
'COALINDIA',
'DIVISLAB',
'DRREDDY',
'EICHERMOT',
'GRASIM',
'HCLTECH',
'HDFCBANK',
'HDFCLIFE',
'HEROMOTOCO',
'HINDALCO',
'HINDUNILVR',
'ICICIBANK',
'ITC',
'INDUSINDBK',
'INFY',
'JSWSTEEL',
'KOTAKBANK',
'LTIM',
'LT',
'M_M',
'MARUTI',
'NTPC',
'NESTLEIND',
'ONGC',
'POWERGRID',
'RELIANCE',
'SBILIFE',
'SHRIRAMFIN',
'SBIN',
'SUNPHARMA',
'TCS',
'TATACONSUM',
'TATAMOTORS',
'TATASTEEL',
'TECHM',
'TITAN',
'ULTRACEMCO',
'WIPRO']


def get_data(tf):

    tickers_data = []

    # Iterate through each ticker
    for ticker in tickers:
        try:
            # Retrieve data for the ticker from NYSE
            data = TA_Handler(
                symbol=ticker,
                screener="india",
                exchange="NSE",
                interval=tf
            )
            data = data.get_analysis().summary
            tickers_data.append(data)
            
        except Exception as e:
            # If no data is found for the ticker in NYSE, search in NASDAQ
            print(f"No data found for ticker {ticker} in NSE. Searching ..")
            '''data = TA_Handler(
                symbol=ticker,
                screener="america",
                exchange="NASDAQ",
                interval="1d"
            )
            data = data.get_analysis().summary
            tickers_data.append(data)'''

    print("Data successfully imported.")
    recommendations = []
    buys = []
    sells = []
    neutrals = []

    # Iterate through each data in tickers_data
    for data in tickers_data:
        recommendation = data.get('RECOMMENDATION')
        buy = data.get('BUY')
        sell = data.get('SELL')
        neutral = data.get('NEUTRAL')
        
        recommendations.append(recommendation)
        buys.append(buy)
        sells.append(sell)
        neutrals.append(neutral)

    data = {
        'Ticker': tickers,
        'Recommendations': recommendations,
        'Buys': buys,
        'Sells': sells,
        'Neutrals': neutrals
    }

    df = pd.DataFrame(data)
    # Define the order of categories
    order_categories = {
        'STRONG_BUY': 5,
        'BUY': 4,
        'NEUTRAL': 3,
        'SELL': 2,
        'STRONG_SELL': 1
    }

    # Assign a numerical value to each category in a new column "Order"
    df['Order'] = df['Recommendations'].map(order_categories)
    df = df.sort_values('Order', ascending=True).reset_index(drop=True)

    # Drop the "Order" column if not needed in the final output
    df = df.drop('Order', axis=1)

    # Display the sorted dataframe
    print(df)
        # Create the figure and axes
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.set_facecolor('#111111')
    ax.set_facecolor('#111111')

    # Add the horizontal bars for buys, neutrals, and sells
    ax.barh(df.index, df["Buys"], height=0.25, color='#00BFFF', label='B')
    ax.barh(df.index, df["Neutrals"], height=0.25, color='#808080', label='N', left=df["Buys"])
    ax.barh(df.index, df["Sells"], height=0.25, color='#FFA500', label='S', left=df["Buys"] + df["Neutrals"])

    # Set the axes labels
    ax.set_yticks(df.index)
    ax.set_yticklabels(df["Ticker"], fontsize=8, color='white')
    ax.set_xlabel(tf+' View', fontsize=10, color='white')

    # Add title with larger font size and additional spacing
    ax.set_title('NIFTY 50 Stocks Trend', fontsize=14, color='white', pad=20)

    # Add the annotations
    for i, recommendation in enumerate(df["Recommendations"]):
        ax.annotate(recommendation, xy=(25, i), xytext=(26.5, i),
                    color='white', fontsize=8, va='center', ha='left')

    # Remove the horizontal grid lines
    ax.yaxis.grid(False)

    # Configure the tick and axis styles
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Adjust the spacing
    plt.tight_layout()

    # Set the text color of the legend to white
    legend = ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.175), ncol=3, fontsize=8)
    for text in legend.get_texts():
        text.set_color('#111111')
    fig.savefig('nifty'+tf+datetime.now().strftime('%H%M')+'.png')
    # Display the plot
    #plt.show()



if __name__=="__main__":
    get_data("1h")
    get_data("15m")