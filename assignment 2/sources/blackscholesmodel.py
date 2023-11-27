import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import norm

class BlackScholes:
    def __init__(self) -> None:
        pass

    def calc_blackscholes(S0, K, sigma, T, r):
        """
        Calculate European call price using the Black scholes formula

        Input: 
        - K (int) strike price
        - r (double) monthly interest
        - S0 (int): initial stock value
        - sigma (float): volatility (stdev)
        - T (float): time till maturity

        Output: 
        - C (float): Black scholes valuation 
        """
        # ITM probability:
        d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

        # OTM probability
        d2 = d1 - sigma * np.sqrt(T)

        # Call price:
        C = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        print(f'Black-Scholes call option valuation: {np.round(C, 2)}')
        return C
