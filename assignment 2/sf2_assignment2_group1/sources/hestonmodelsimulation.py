import pandas as pd
import numpy as np

class HestonModelAssetSimulation:

    def __init__(self, rf_rate, start_date=0, end_date=1) -> None:
        """
        Initializes the HestonModelAssetSimulation class.

        Parameters:
        - rf_rate: Risk-free interest rate.
        - start_date: Start date for the simulation (default is 0).
        - end_date: End date for the simulation (default is 1).
        """
        self.start_date = start_date
        self.end_date = end_date
        self.outputdir = 'output'
        self.rf_rate = rf_rate

    def _create_empty_frame(self):
        """
        Creates an empty pandas DataFrame with columns for OHLCV (Open, High, Low, Close, Volume) data.

        Returns:
        - An empty DataFrame with the specified columns.
        """
        date_range = pd.date_range(start=self.start_date, end=self.end_date, freq='B')
        zeros = pd.Series(np.zeros(len(date_range)))

        return pd.DataFrame({
            'date': date_range,
            'open': zeros,
            'high': zeros,
            'low': zeros,
            'close': zeros,
            'volume': zeros
        })[['date', 'open', 'high', 'low', 'close', 'volume']]

    def create_heston_model_asset(self, init_asset, variance, delta_t, wiener_asset):
        """
        Simulates the asset price path using the Heston model.

        Parameters:
        - init_asset: Initial asset price.
        - variance: Current variance.
        - delta_t: Time step size.
        - wiener_asset: Brownian motion increment for the asset.

        Returns:
        - Simulated asset price.
        """
        asset_path = np.exp((self.rf_rate - 0.5 * variance) * delta_t + np.sqrt(variance * delta_t) * wiener_asset)
        return init_asset * asset_path

    def create_heston_model_variance(self, kappa, theta, delta_t, sigma, init_variance, wiener_asset):
        """
        Simulates the variance path using the Heston model.

        Parameters:
        - kappa: Heston model parameter kappa.
        - theta: Heston model parameter theta.
        - delta_t: Time step size.
        - sigma: Heston model parameter sigma.
        - init_variance: Initial variance.
        - wiener_asset: Brownian motion increment for the asset.

        Returns:
        - Updated variance.
        """
        variance_path = kappa * (theta - init_variance) * delta_t + sigma * np.sqrt(init_variance * delta_t) * wiener_asset
        return init_variance + variance_path

    def heston_model_sim(self, S0, v0, rho, kappa, theta, sigma, T, N, M):
        """
        Simulates the Heston model for asset prices and volatilities.

        Parameters:
        - S0: Initial asset price.
        - v0: Initial volatility.
        - rho: Heston model parameter rho (correlation).
        - kappa: Heston model parameter kappa.
        - theta: Heston model parameter theta.
        - sigma: Heston model parameter sigma.
        - T: Total time (maturity).
        - N: Number of time steps.
        - M: Number of simulations.

        Returns:
        - S: Simulated asset price paths.
        - v: Simulated volatility paths.
        """
        delta_t = T / N
        mu = np.array([0, 0])

        cov = np.array([[1, rho],
                        [rho, 1]])

        S = np.full(shape=(N + 1, M), fill_value=S0)
        v = np.full(shape=(N + 1, M), fill_value=v0)

        Z = np.random.multivariate_normal(mu, cov, (N, M))

        for i in range(1, N + 1):
            S[i] = self.create_heston_model_asset(S[i - 1], v[i - 1], delta_t, Z[i - 1, :, 0])
            v[i] = np.maximum(self.create_heston_model_variance(kappa, theta, delta_t, sigma, v[i - 1], Z[i - 1, :, 1]), 0)

        return S, v
