import matplotlib.pyplot as plt
import sources.binomialtree as BinomialTree  # Ensure this module is correctly imported

class Plotter: 
    def __init__(self, strike_prices, volatilities, maturities, stock_price, risk_free_rate, steps):
        self.stock_price = stock_price
        self.strike_prices = strike_prices if strike_prices is not None else [stock_price]
        self.volatilities = volatilities if volatilities is not None else [0.05]
        self.maturities = maturities if maturities is not None else [1]
        self.risk_free_rate = risk_free_rate
        self.steps = steps

    def plot_option_prices(self, prices, title, subplot_ax, x_labels, option_type):
        subplot_ax.plot(prices, label=[f'European {option_type}', f'American {option_type}'])
        subplot_ax.set_title(title)
        subplot_ax.set_xlabel(x_labels)
        subplot_ax.set_ylabel('Option Price')
        subplot_ax.legend()

    def collect_data(self, parameter_list, parameter_name, option_type):
        data = []
        for param in parameter_list:
            binomial_tree = BinomialTree.BinomialTree(
                self.stock_price, 
                self.stock_price if parameter_name != 'strike' else param, 
                self.risk_free_rate, 
                0.05 if parameter_name != 'volatility' else param, 
                1 if parameter_name != 'maturity' else param, 
                self.steps
            )
            european_price = binomial_tree.run_binomialtree(option='european', option_type=option_type)
            american_price = binomial_tree.run_binomialtree(option='american', option_type=option_type)
            data.append([european_price, american_price])
        return data

    def plot_all(self):
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))

        # Plotting for calls
        strike_prices_data_call = self.collect_data(self.strike_prices, 'strike', 'call')
        self.plot_option_prices(strike_prices_data_call, 'Call Prices vs Strike Prices', axs[0, 0], 'Strike Prices', 'call')

        volatilities_data_call = self.collect_data(self.volatilities, 'volatility', 'call')
        self.plot_option_prices(volatilities_data_call, 'Call Prices vs Volatility', axs[0, 1], 'Volatility', 'call')

        maturities_data_call = self.collect_data(self.maturities, 'maturity', 'call')
        self.plot_option_prices(maturities_data_call, 'Call Prices vs Maturities', axs[0, 2], 'Maturities', 'call')

        # Plotting for puts
        strike_prices_data_put = self.collect_data(self.strike_prices, 'strike', 'put')
        self.plot_option_prices(strike_prices_data_put, 'Put Prices vs Strike Prices', axs[1, 0], 'Strike Prices', 'put')

        volatilities_data_put = self.collect_data(self.volatilities, 'volatility', 'put')
        self.plot_option_prices(volatilities_data_put, 'Put Prices vs Volatility', axs[1, 1], 'Volatility', 'put')

        maturities_data_put = self.collect_data(self.maturities, 'maturity', 'put')
        print(self.maturities)
        self.plot_option_prices(maturities_data_put, 'Put Prices vs Maturities', axs[1, 2], 'Maturities', 'put')

        plt.tight_layout()
        plt.show()

