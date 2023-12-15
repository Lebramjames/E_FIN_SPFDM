import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy import stats

class Plotter:
    def __init__(self) -> None:
        # Constructor for the Plotter class. Currently, it does not initialize any attributes.
        pass

    def plot_simpayoffs(self, payoffs, mean_payoff):
        # Plots a histogram of simulated option payoffs with a kernel density estimate (KDE).
        plt.figure(figsize=(10, 6))
        sns.histplot(payoffs, bins=30, kde=True, color='blue')
        plt.xlabel("Payoff")
        plt.ylabel("Frequency")
        plt.title("Distribution of Option Payoffs")
        # Draws a vertical line representing the mean payoff.
        plt.axvline(x=mean_payoff, color='red', linestyle='--', label=f'Mean Payoff = {mean_payoff:.2f}')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_diffcorrelation_payoffs(self, payoffs, correlations, spreads):
        # Plots the relationship between the option payoffs and their correlations, 
        # with the spread range represented as a shaded region.
        plt.figure(figsize=(10, 6))

        # Calculates the lower and upper bounds of the spread range.
        lower_bounds = np.array(payoffs) - np.array(spreads)
        upper_bounds = np.array(payoffs) + np.array(spreads)
        lower_bounds = np.maximum(lower_bounds, 0)

        # Plots the option payoffs as a line plot.
        sns.lineplot(x=correlations, y=payoffs, label="Option Payoffs", color='b')
        # Shades the area between the lower and upper bounds of the spread.
        plt.fill_between(correlations, lower_bounds, upper_bounds, color='r', alpha=0.3, label="Spread Range")
        plt.xlabel("Correlation")
        plt.ylabel("Option Payoff")
        plt.title("Option Payoff vs. Correlation with Spread Range (Standard Deviation)")
        plt.grid(True)
        plt.legend()
        plt.show()

    def plot_strikeprices(self, strikeprices, bs_prices, bachelier_prices, monte_carlo_prices):
        # Plots the option prices for different strike prices using three different pricing models.
        plt.figure(figsize=(10, 6))
        plt.plot(strikeprices, bs_prices, label='Black-Scholes', marker='o')
        plt.plot(strikeprices, bachelier_prices, label='Bachelier', marker='x')
        plt.plot(strikeprices, monte_carlo_prices, label='Monte Carlo', marker='s')
        plt.xlabel('K')
        plt.ylabel('Option Price')
        plt.title('Option Prices vs. Strike prices')
        plt.legend()
        plt.grid()
        plt.show()  

    def plot_histogramfutureprices(self, future_prices, mean_future):
        # Plots a histogram of future prices with a KDE and a line for the mean future price.
        plt.figure(figsize=(10, 6))
        sns.histplot(future_prices, bins=30, kde=True, color='blue')
        # Draws a vertical line representing the mean future price.
        plt.axvline(x=mean_future, color='red', linestyle='--', label=f'Mean Future = {mean_future:.2f}')
        plt.xlabel("Future Prices")
        plt.ylabel("Frequency")
        plt.title("Distribution of Future Prices")
        plt.grid(True)
        plt.show()

    def plot_stocks(self, stocks, n_sim):
        # Plots the price paths for two stocks across multiple simulations.
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        for sim in range(n_sim):
            # Stock 1 (S1) for each simulation
            axes[0].plot(stocks[0, :, sim], label=f'Sim {sim+1}')
            axes[0].set_title('Stock 1 (S1) Price Paths')
            axes[0].set_xlabel('Time Steps')
            axes[0].set_ylabel('Stock Price')

            # Stock 2 (S2) for each simulation
            axes[1].plot(stocks[1, :, sim], label=f'Sim {sim+1}')
            axes[1].set_title('Stock 2 (S2) Price Paths')
            axes[1].set_xlabel('Time Steps')
            axes[1].set_ylabel('Stock Price')

        # Commented out legend code - can be enabled if legend is required.
        # axes[0].legend()
        # axes[1].legend()

        plt.tight_layout()
        axes[0].grid(True)
        axes[1].grid(True)
        plt.show()

    def plot_futures(self, futures, n_sim):
        # Plots the future price paths for multiple simulations.
        fig, ax = plt.subplots(figsize=(12, 5))

        for sim in range(n_sim):
            # Plot each simulation
            ax.plot(futures[sim], label=f'Sim {sim+1}')

        ax.set_title('Future Price Paths')
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Future Price')
        
        # Legend is commented out but can be included by removing the comment.
        # ax.legend()

        ax.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_lognormaldistribution(self, spread_data):
        """
        Plot the spread data and fit a log-normal distribution to it.
        
        Parameters:
        - spread_data (array-like): An array containing the spread data to be plotted.
        
        Generates a plot of the spread data with a histogram and a fitted log-normal distribution.
        """
        # Plot a histogram of the spread data with a kernel density estimate.
        sns.histplot(spread_data, bins=100, kde=True, color='b', label='Spread Data', stat='density')

        # Fit a log-normal distribution to the data and plot the probability density function.
        shape, loc, scale = stats.lognorm.fit(spread_data)
        x = np.linspace(min(spread_data), max(spread_data), 100)
        pdf = stats.lognorm.pdf(x, shape, loc=loc, scale=scale)
        plt.plot(x, pdf, 'r-', label='Log-Normal Fit')

        # Label the axes and add a legend to the plot.
        plt.xlabel('Spread')
        plt.ylabel('Probability Density')
        plt.legend()

        # Display the plot.
        plt.show()
