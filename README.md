# Quantitative-Analysis
Quantitative analysis uses mathematical models, market data, and fixed rules to develop trading strategies. It relies on backtesting to evaluate performance but must avoid overfitting to ensure real-world effectiveness.

# Bitcoin Historical Data Quantitative Analysis Backtest
By applying a simple Exponential Moving Average (EMA) strategy to Bitcoin price action, we can backtest different EMA lengths to find the optimal parameters for maximum returns. Using the Sharpe ratio as our key metric, we aim to maximize risk-adjusted returns.  

After running the optimization in Python, the best parameters identified are:  
- **Optimal rolling window for MA:** 57.01  
- **Optimal threshold gap:** 0.0398  
- **Maximum Sharpe Ratio:** 1.88  

This strategy yielded a **400% return over a 4-year period** in Bitcoin data, demonstrating the potential of quantitative optimization.

![image](https://github.com/user-attachments/assets/e59d52e0-3f8f-440d-86d2-c78fd20391e8)


Please refer and download to the python file (EMA backtest.py) and the csv file (Bitcoin Historical Data) to test run the backtest
