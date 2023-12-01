import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from  scipy.stats  import norm
from scipy.linalg import cholesky


class BachelierModel():
    def __init__(self):
        pass    

    def calculate_bachelier_option_price(self, F, K, stdev, T, r, t = 0, option_type="EU_CALL"):
        """
        Calculate Bachelier option price.
        """
        d1 = (F - K) / (stdev * np.sqrt(T - t))


        if option_type == "EU_CALL":
            call_price = np.exp(-r * (T - t)) * ((F - K) * norm.cdf(d1) + stdev * np.sqrt(T - t) * norm.pdf(d1))
            return call_price

        elif option_type == "EU_PUT":
            put_price = np.exp(-r * (T - t)) * ((K - F) * norm.cdf(-d1) + stdev * np.sqrt(T - t) * norm.pdf(-d1))
            return put_price

        else:
            raise ValueError("Invalid option_type. Use 'EU_CALL' or 'EU_PUT'.")

    def daily_volatility_bachelier(self, S0, sigma, corr):
        return np.sqrt((sigma[0] * S0[0])**2 + (sigma[1]  * S0[1])**2 - 2*sigma[0] *sigma[1] *corr * S0[0] * S0[1])
