import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from  scipy.stats  import norm


class Plotter:
    def __init__(self) -> None:
        pass
    

    # %% Question 1:

    def plot_simpayoffs(self, payoffs, mean_payoff):
        # Create a Seaborn histogram
        plt.figure(figsize=(10, 6))
        sns.histplot(payoffs, bins=30, kde=True, color='blue')
        plt.xlabel("Payoff")
        plt.ylabel("Frequency")
        plt.title("Distribution of Option Payoffs")
        plt.axvline(x=mean_payoff, color='red', linestyle='--', label=f'Mean Payoff = {mean_payoff:.2f}')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_diffcorrelation_payoffs(self, payoffs, correlations, spreads):
        plt.figure(figsize=(10, 6))
        
        # Calculate lower and upper bounds for the spread range
        lower_bounds = np.array(payoffs) - np.array(spreads)
        upper_bounds = np.array(payoffs) + np.array(spreads)
        
        # Clip the lower bounds to 0
        lower_bounds = np.maximum(lower_bounds, 0)
        
        # Plot option payoffs
        sns.lineplot(x=correlations, y=payoffs, label="Option Payoffs", color='b')
        
        # Plot the spread range around the mean, considering the lower bounds
        plt.fill_between(correlations, lower_bounds, upper_bounds, color='r', alpha=0.3, label="Spread Range")
        
        plt.xlabel("Correlation")
        plt.ylabel("Option Payoff")
        plt.title("Option Payoff vs. Correlation with Spread Range (Standard Deviation)")
        plt.grid(True)
        plt.legend()
        plt.show()



    def plot_histogramfutureprices(self, future_prices, mean_future):
        plt.figure(figsize=(10, 6))
        sns.histplot(future_prices, bins=30, kde=True, color='blue')
        plt.axvline(x=mean_future, color='red', linestyle='--', label=f'Mean Future = {mean_future:.2f}')
        plt.xlabel("Future Prices")
        plt.ylabel("Frequency")
        plt.title("Distribution of Future Prices")
        plt.grid(True)
        plt.show()




    def plot_stocks(self,stocks, n_sim):
        # Plotting
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

        # Adding legends to the plots
        # axes[0].legend()
        # axes[1].legend()

        plt.tight_layout()
        axes[0].grid(True)
        axes[1].grid(True)
        plt.show()

    def plot_futures(self, futures, n_sim):
        # Assuming futures is a list of lists (each inner list is a path of prices for one simulation)
        fig, ax = plt.subplots(figsize=(12, 5))

        for sim in range(n_sim):
            # Plot each simulation
            ax.plot(futures[sim], label=f'Sim {sim+1}')

        ax.set_title('Future Price Paths')
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Future Price')
        
        # Uncomment below if you want to show legend
        # ax.legend()

        ax.grid(True)
        plt.tight_layout()
        plt.show()








    # %%  Question 2:
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