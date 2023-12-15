import numpy as np
from scipy.stats import norm
from scipy.linalg import cholesky

class BachelierModel():
    def __init__(self):
        # The constructor for BachelierModel doesn't currently initialize any attributes.
        pass    

    def calculate_bachelier_option_price(self, F, K, stdev, T, r, t=0, option_type="EU_CALL"):
        """
        Calculate the option price using the Bachelier model which assumes a normal distribution for the underlying asset.
        
        Parameters:
        - F (float): The current price of the underlying asset (forward price).
        - K (float): The strike price of the option.
        - stdev (float): The standard deviation of the underlying asset's returns, a proxy for volatility.
        - T (float): The time to maturity of the option (in years).
        - r (float): The risk-free interest rate, expressed as a decimal.
        - t (float, optional): The current time, with t=0 representing the valuation date. Defaults to 0.
        - option_type (str, optional): The type of option to be priced, 'EU_CALL' for European call options or 'EU_PUT' for European put options. Defaults to 'EU_CALL'.
        
        Returns:
        - float: The price of the call or put option as specified by the option_type parameter.
        """
        # Calculate the d1 term used in the Bachelier option pricing formula.
        d1 = (F - K) / (stdev * np.sqrt(T - t))

        # If the option type is a European call, calculate and return the call option price.
        if option_type == "EU_CALL":
            call_price = np.exp(-r * (T - t)) * ((F - K) * norm.cdf(d1) + stdev * np.sqrt(T - t) * norm.pdf(d1))
            return call_price

        # If the option type is a European put, calculate and return the put option price.
        elif option_type == "EU_PUT":
            put_price = np.exp(-r * (T - t)) * ((K - F) * norm.cdf(-d1) + stdev * np.sqrt(T - t) * norm.pdf(-d1))
            return put_price

        # If the option type provided is neither 'EU_CALL' nor 'EU_PUT', raise a ValueError.
        else:
            raise ValueError("Invalid option_type. Use 'EU_CALL' or 'EU_PUT'.")

    def daily_volatility_bachelier(self, S0, sigma, corr):
        """
        Calculate the daily volatility of a portfolio of two assets using the Bachelier model.
        
        Parameters:
        - S0 (array-like): An array containing the initial prices of the two assets.
        - sigma (array-like): An array containing the volatilities of the two assets.
        - corr (float): The correlation coefficient between the two assets, ranging from -1 to 1.
        
        Returns:
        - float: The daily volatility of the portfolio as calculated by the Bachelier model.
        """
        # Using the Bachelier model, calculate the daily volatility considering the correlation between assets.
        return np.sqrt((sigma[0] * S0[0])**2 + (sigma[1] * S0[1])**2 - 2 * sigma[0] * sigma[1] * corr * S0[0] * S0[1])
