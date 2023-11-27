import numpy as np

class SABR_model_simulation:
    def __init__(self) -> None:
        pass

    def create_sabr_model_asset(self, F, sigma, beta, dW1):
        """
        Simulates the asset price path using the SABR model.

        Parameters:
        - F: Initial forward rate.
        - sigma: Initial volatility.
        - beta: SABR model parameter beta.
        - dW1: Brownian motion increment for the asset.

        Returns:
        - S: Simulated asset price path.
        """
        return F + (sigma * F ** beta) * dW1

    def create_sabr_model_sigma(self, sigma, alpha, dW2):
        """
        Simulates the volatility path using the SABR model.

        Parameters:
        - sigma: Current volatility.
        - alpha: SABR model parameter alpha.
        - dW2: Brownian motion increment for volatility.

        Returns:
        - Updated volatility.
        """
        return sigma + (alpha * sigma * dW2)
    
    def sabr_model_sim(self, F0, sigma0, rho, beta, alpha, T, N, M):
        """
        Simulates the SABR model for asset prices and volatilities.

        Parameters:
        - F0: Initial forward rate.
        - sigma0: Initial volatility.
        - rho: SABR model parameter rho (correlation).
        - beta: SABR model parameter beta.
        - alpha: SABR model parameter alpha.
        - T: Total time (maturity).
        - N: Number of time steps.
        - M: Number of simulations.

        Returns:
        - F: Simulated forward rate paths.
        - sigma: Simulated volatility paths.
        """

        delta_t = T / N
        mu = np.array([0, 0])

        cov = np.array([[1, rho],
                        [rho, 1]])

        F = np.full(shape=(N + 1, M), fill_value=F0)
        sigma = np.full(shape=(N + 1, M), fill_value=sigma0)
        Z = np.random.multivariate_normal(mu, cov, (N, M)) * np.sqrt(delta_t)

        for i in range(1, N + 1):
            F[i] = self.create_sabr_model_asset(F[i - 1], sigma[i - 1], beta, Z[i - 1, :, 0])
            sigma[i] = self.create_sabr_model_sigma(sigma[i - 1], alpha, Z[i - 1, :, 1])

        return F, sigma
