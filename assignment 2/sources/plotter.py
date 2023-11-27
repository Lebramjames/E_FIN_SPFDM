import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from  scipy.stats  import norm


class Plotter:
    def __init__(self) -> None:
        pass
    
    def plot_2curves(self, S, F, sigma, v):
        # Create subplots using Seaborn
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        # Plot Asset Prices
        sns.lineplot(data=pd.DataFrame({'S': S[:, 0], 'F': F[:, 0]}), ax=axes[0])
        axes[0].set_xlabel('Time Steps')
        axes[0].set_ylabel('Price')
        axes[0].set_title('Asset Prices (S and F)')

        # Plot Volatility
        sns.lineplot(data=pd.DataFrame({'Stdev Heston': v[:, 0], 'Stdev SABR': sigma[:, 0]}), ax=axes[1])
        axes[1].set_xlabel('Time Steps')
        axes[1].set_ylabel('Volatility')
        axes[1].set_title('Volatility (v and sigma)')

        # Adjust layout
        plt.tight_layout()
        plt.savefig('plots/volatilityClustering.png')
        plt.show()

    def plot_2logcurves(self, S_heston, F_sabr, j):
        # Create subplots using Seaborn
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        # Plot Heston Log Returns in the first subplot
        sns.lineplot(data=pd.DataFrame({'Heston': S_heston[:-1, j]}), ax=axes[0])
        axes[0].set_xlabel('Time Steps')
        axes[0].set_ylabel('Log Returns')
        axes[0].set_title('Heston Log Returns')

        # Plot SABR Log Returns in the second subplot
        sns.lineplot(data=pd.DataFrame({'SABR': F_sabr[:-1, j]}), ax=axes[1])
        axes[1].set_xlabel('Time Steps')
        axes[1].set_ylabel('Log Returns')
        axes[1].set_title('SABR Log Returns')

        # Adjust layout
        plt.tight_layout()
        plt.savefig('plots/logReturnsComparison.png')
        plt.show()

    def __mean_stdev(self, data):
        mean = np.mean(data, axis=0)
        stdev = np.std(data, axis=0)
        return mean, stdev

    def plot_hist(self, heston_logreturns, sabr_logreturns):
        mean_heston_logreturns, std_returns_heston = self.__mean_stdev(heston_logreturns)
        mean_sabr_logreturns, std_returns_sabr = self.__mean_stdev(sabr_logreturns)

        # Create histograms for Heston model log-returns (only the first path)
        plt.figure(figsize=(12, 6))

        plt.subplot(1, 2, 1)
        plt.hist(heston_logreturns[:, 0], bins=30, density=True, alpha=0.6, label=f'Log-Returns (Path 1)')

        x_heston = np.linspace(np.min(heston_logreturns[:, 0]), np.max(heston_logreturns[:, 0]), 100)
        pdf_heston = norm.pdf(x_heston, loc=mean_heston_logreturns[0], scale=std_returns_heston[0])
        plt.plot(x_heston, pdf_heston, 'r-', lw=2, label='Normal Distribution')
        plt.xlabel('Log-Returns (Heston)')
        plt.ylabel('Probability Density')
        plt.title('Histogram of Log-Returns vs. Normal Distribution (Heston)')
        plt.legend()

        # Create histograms for SABR model log-returns (only the first path)
        plt.subplot(1, 2, 2)
        plt.hist(sabr_logreturns[:, 0], bins=30, density=True, alpha=0.6, label=f'Log-Returns (Path 1)')

        x_sabr = np.linspace(np.min(sabr_logreturns[:, 0]), np.max(sabr_logreturns[:, 0]), 100)
        pdf_sabr = norm.pdf(x_sabr, loc=mean_sabr_logreturns[0], scale=std_returns_sabr[0])
        plt.plot(x_sabr, pdf_sabr, 'r-', lw=2, label='Normal Distribution')
        plt.xlabel('Log-Returns (SABR)')
        plt.ylabel('Probability Density')
        plt.title('Histogram of Log-Returns vs. Normal Distribution (SABR)')
        plt.legend()

        plt.tight_layout()
        plt.savefig('plots/histPlots.png')
        plt.show()  


    def plot_bs_SABR_volatility(self, option_prices_sabr, option_prices_bs, moneyness_levels):

        # Plot option prices based on implied volatility
        plt.figure(figsize=(10, 6))
        for option_type in ['Call', 'Put']:
            for moneyness in moneyness_levels:
                option_label = f'{option_type} {moneyness}'
                mc_prices = [option_prices_sabr[f'{option_type} {moneyness}'] for moneyness in moneyness_levels]
                bs_prices = [option_prices_bs[f'{option_type} {moneyness}'] for moneyness in moneyness_levels]
                plt.plot(moneyness_levels, mc_prices, label=f'MC {option_label}')
                plt.plot(moneyness_levels, bs_prices, label=f'BS {option_label}', linestyle='--')

        plt.xlabel('Moneyness')
        plt.ylabel('Option Price')
        plt.title('Option Prices Comparison (MC vs. BS) based on Implied Volatility')
        plt.legend()
        plt.grid(True)
        plt.show()