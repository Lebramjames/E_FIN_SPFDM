import numpy as np

class BinomialTree:
    def __init__(self, stock_price, strike_price, risk_free_rate, volatility, maturity, steps):
        """
        Initializes the Binomial Tree for option pricing.

        :param stock_price: Current price of the underlying stock
        :param strike_price: Strike price of the option
        :param risk_free_rate: Risk-free interest rate
        :param volatility: Volatility of the underlying stock
        :param maturity: Time to maturity of the option (in years)
        :param steps: Number of steps in the binomial tree
        """
        self.stock_price = stock_price
        self.strike_price = strike_price
        self.risk_free_rate = risk_free_rate
        self.volatility = volatility
        self.maturity = maturity
        self.steps = steps
        self.dt = maturity / steps  # Time delta per step
        self.u = np.exp(volatility * np.sqrt(self.dt))  # Upward movement factor
        self.d = 1 / self.u  # Downward movement factor
        self.p = (np.exp(risk_free_rate * self.dt) - self.d) / (self.u - self.d)  # Risk-neutral probability

    def _calculate_option_value_at_node(self, stock_price, is_call=True):
        """
        Helper function to calculate option value at a node based on stock price.

        :param stock_price: Stock price at the node
        :param is_call: Boolean flag to indicate if it's a call option. If False, it's a put option.
        :return: Option value at the node
        """
        if is_call:
            return max(stock_price - self.strike_price, 0)
        else:
            return max(self.strike_price - stock_price, 0)

    def european_binomial(self,option_type='call'):
        """
        Runs the binomial tree algorithm for a European option.

        :param option_type: Type of the option - 'call' or 'put'
        :return: Calculated option price
        """
        option_values = np.zeros(self.steps + 1)

        for i in range(self.steps + 1):
            stock_price_at_node = self.stock_price * (self.u **i) * (self.d ** (self.steps - i))
            option_values[i] = self._calculate_option_value_at_node(stock_price_at_node, is_call=option_type == 'call')

        for step in range(self.steps -1, -1, -1):
            for i in range(step+1):
                option_values[i] = (self.p * option_values[i + 1] + (1 - self.p) * option_values[i]) * np.exp(-self.risk_free_rate * self.dt)

        return option_values[0]

    def american_binomial(self, option_type='call'):
        """
        Calculate the option price for an American option using the Binomial Tree method.

        :param option_type: 'call' for a call option, 'put' for a put option
        :return: Calculated option price
        """
        option_values = np.zeros(self.steps + 1)

        # Initialize option values at maturity
        for i in range(self.steps + 1):
            stock_price_at_node = self.stock_price * (self.u ** i) * (self.d ** (self.steps - i))
            option_values[i] = self._calculate_option_value_at_node(stock_price_at_node, is_call=(option_type == 'call'))

        # Iterate backwards through the tree
        for step in range(self.steps - 1, -1, -1):
            for i in range(step + 1):
                stock_price_at_node = self.stock_price * (self.u ** i) * (self.d ** (step - i))
                early_exercise = self._calculate_option_value_at_node(stock_price_at_node, is_call=(option_type == 'call'))
                option_values[i] = max((self.p * option_values[i + 1] + (1 - self.p) * option_values[i]) * np.exp(-self.risk_free_rate * self.dt), early_exercise)

        return option_values[0]


    def run_binomialtree(self, option = 'european', option_type = 'call' ):
        """
        Runs the binomial tree algorithm based on the specified option type.

        :param option: 'european' for European option, 'american' for American option
        :param option_type: 'call' for a call option, 'put' for a put option
        :return: Calculated option price
        """
        if option == 'european':
            option_value = self.european_binomial(option_type=option_type)
        else: 
            option_value = self.american_binomial(option_type=option_type)

        return option_value
