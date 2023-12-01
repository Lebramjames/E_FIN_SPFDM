import numpy as np


class BivariateMonteCarlo: 
    def __init__(self) -> None:
        pass
    
    def generate_correlated_normals(self, n_steps, n_sim, rho):
        """
        Generates correlated normal random samples.

        Args:
        - n_sim (int): Number of simulations.
        - correlation (float): Correlation coefficient between two variables.

        Returns:
        - correlated_samples (numpy.ndarray): Array of correlated normal samples.
        """

        # genreate normal samples:
        x1 = np.random.normal(0, 1, (n_steps, n_sim))
        x2 = np.random.normal(0, 1, (n_steps, n_sim))

        epsilon1 = x1
        epsilon2 = rho * x1 + x2 * np.sqrt(1 - rho ** 2)

        return (epsilon1, epsilon2)

    def simulate_bivariate_monte_carlo(self, S0, sigma, rho=0.3, n_steps=252, n_sim=1000):
        """
        Simulates a bivariate Monte Carlo experiment for a financial model.

        Args:
        - S0 (list): Initial stock prices for two assets.
        - variance (list): Variances of two assets.
        - correlation (float): Correlation coefficient between the asset returns.
        - steps (int): Number of time steps.
        - n_sim (int): Number of Monte Carlo simulations.

        Returns:
        - payoffs (numpy.ndarray): Array of simulated payoffs.
        """
        payoffs = np.zeros(n_sim)
        stock = np.zeros((2, n_steps+1, n_sim))
        stock[0][:][:] = S0[0]
        stock[1][:][:] = S0[1]

        # dt = T / n_steps
        epsilon = self.generate_correlated_normals(n_steps, n_sim, rho)
        for t in range(1, n_steps+ 1):
            for i in range(2):
                stock[i][t] = stock[i][t-1] + sigma[i] * stock[i][t-1] * epsilon[i][t-1]

        return stock 
    
    def monte_carlo_option_price(self, S1, S2, T, r, K):
        payoffs = np.maximum(S1[-1] - S2[-1] - K, 0) * np.exp(-r*T)
        option_price = np.mean(payoffs) * np.exp(-r*T)
        spread = S1[-1] - S2[-1]
        return option_price, payoffs, spread 
    
    def calculate_spread_volatility(self, sigma1, sigma2, rho, w1=1, w2=-1):
        """
        Calculate the volatility of the spread using the portfolio variance formula.

        Args:
        - sigma1 (float): Volatility of the first asset (S1).
        - sigma2 (float): Volatility of the second asset (S2).
        - rho (float): Correlation between the two assets.
        - w1 (float, optional): Weight of the first asset in the portfolio (default is 1).
        - w2 (float, optional): Weight of the second asset in the portfolio (default is -1).

        Returns:
        - spread_volatility (float): Volatility of the spread.
        """

        # Calculate the volatility of the spread using the portfolio variance formula
        spread_volatility = np.sqrt((w2**2 * sigma1**2) + (w1**2 * sigma2**2) + (2 * w1 * w2 * sigma1 * sigma2 * rho))

        return spread_volatility
