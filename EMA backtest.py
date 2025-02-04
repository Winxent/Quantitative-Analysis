import pandas as pd
import numpy as np
import plotly.graph_objects as go
import math
from scipy.optimize import differential_evolution
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
df = pd.read_csv('Bitcoin Historical Data.csv')#<< change to your CSV file name with ".csv"

def sharpe_opti(ma, n):
    # Copy and prepare the dataframe
    df_1 = df[['Date', 'Price']].copy()

    df_1 = df_1.iloc[::-1].reset_index(drop=True)

    df_1['Date'] = pd.to_datetime(df_1['Date'])

    df_1['Price'] = df_1['Price'].str.replace(',' , '', regex=True)

    df_1['Price'] = pd.to_numeric(df_1['Price'])

    df_1['ema'] = df_1['Price'].ewm(span=int(ma), adjust=False).mean()

    df_1['diff'] = df_1['Price'] / df_1['ema'] - 1

    df_1['position'] = np.where(df_1['diff'] > n, 1, 0)

    df_1['pricediff'] = df_1['Price'].pct_change() * 100

    df_1['pnl'] = df_1['position'].shift(1) * df_1['pricediff']

    df_1['total_pnl'] = df_1['pnl']

    df_1['Cumulative_PnL'] = df_1['total_pnl'].cumsum()

    pnl_std = df_1['total_pnl'].std()
    if pnl_std == 0:
        return float('inf')

    avg_return_per_year = df_1['total_pnl'].mean() * 365
    sharpe_ratio = avg_return_per_year / (pnl_std * math.sqrt(365))

    return -sharpe_ratio

def objective_function(variables):
    ma, n = variables
    return sharpe_opti(ma, n)

def sharpe_optimizer(a, b, c, d):  # a, b = bounds for ma, c, d = bounds for n
    bounds = [(a, b), (c, d)]
    result = differential_evolution(objective_function, bounds)

    if result.success:
        ma, n = result.x
        max_sharpe = -result.fun  # Convert back from negative to positive sharpe
        print(f"The optimal rolling window for MA is: {ma}\nThe optimal threshold gap is: {n}\nThe maximum Sharpe Ratio is: {max_sharpe}")
        return ma, n
    else:
        print("Optimization failed.")
        return None, None

# Run the optimizer and get the optimal ma and n
optimal_ma, optimal_n = sharpe_optimizer(2, 100, 0, 1)

# Use the optimized values in the plotting section
if optimal_ma is not None and optimal_n is not None:
    df_1 = df[['Date', 'Price']].copy()

    df_1 = df_1.iloc[::-1].reset_index(drop=True)

    df_1['Date'] = pd.to_datetime(df_1['Date'])

    df_1['Price'] = df_1['Price'].str.replace(',' , '', regex=True)

    df_1['Price'] = pd.to_numeric(df_1['Price'])

    df_1['ema'] = df_1['Price'].ewm(span=int(optimal_ma), adjust=False).mean()

    df_1['diff'] = df_1['Price'] / df_1['ema'] - 1

    df_1['position'] = np.where(df_1['diff'] > optimal_n, 1, 0)

    df_1['pricediff'] = df_1['Price'].pct_change() * 100

    df_1['pnl'] = df_1['position'].shift(1) * df_1['pricediff']

    df_1['total_pnl'] = df_1['pnl']

    df_1['Cumulative_PnL'] = df_1['total_pnl'].cumsum()

    pnl_std = df_1['total_pnl'].std()
    avg_return_per_year = df_1['total_pnl'].mean() * 365
    sharpe_ratio = avg_return_per_year / (pnl_std * math.sqrt(365))

    fig = go.Figure()

    # Adding the Cumulative PnL trace
    fig.add_trace(go.Scatter(
        x=df_1['Date'],
        y=df_1['Cumulative_PnL'],
        mode='lines',
        name='Cumulative PnL',
        line=dict(color='blue')
    ))

    # Adding the Close Price trace
    fig.add_trace(go.Scatter(
        x=df_1['Date'],
        y=df_1['Price'],
        mode='lines',
        name='Close Price',
        line=dict(color='red'),
        yaxis="y2"
    ))

    # Adding the EMA trace
    fig.add_trace(go.Scatter(
        x=df_1['Date'],
        y=df_1['ema'],
        mode='lines',
        name='Exponential Moving Average',
        line=dict(color='green'),
        yaxis="y2"
    ))

    # Setting the layout for the plot
    fig.update_layout(
        title='Exponential Moving Average',
        xaxis=dict(
            title='Time',
            tickangle=45
        ),
        yaxis=dict(
            title='Cumulative PnL',
            title_font=dict(color='blue'),  # Corrected property
            tickfont=dict(color='blue')
        ),
        yaxis2=dict(
            title='Close Price',
            title_font=dict(color='red'),  # Corrected property
            tickfont=dict(color='red'),
            overlaying='y',
            side='right'
        ),
        legend=dict(
            x=0.05, y=0.95,
            traceorder='normal',
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(255, 255, 255, 0.5)'
        )
    )

    # Adding the annotation for Sharpe Ratio
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.05, y=0.65,
        text=f'Sharpe Ratio: {sharpe_ratio:.2f}',
        showarrow=False,
        font=dict(
            size=12,
            color="black"
        ),
        align="left",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        bgcolor="white",
        opacity=0.8
    )

    # Display the plot
    fig.show()
