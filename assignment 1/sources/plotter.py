import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):

        return

    def save_fig(self, name):
        plt.savefig(
            fr'D:\studie\main_studie\files\stochastics_finance\E_FIN_SPFDM-1\assignment 1\plots\{name}.png')

    def plot_bumps(self, Scenarios, bumps, maturities):
        plt.figure(figsize=(12, 8))

        # Plot a line for each maturity
        for maturity in maturities:
            rates = [Scenarios['scenario2'][maturity][f'{bump*10000}bp'] for bump in bumps]
            plt.plot(bumps * 10000, rates, marker='o', label=f'Maturity {maturity} years')

        plt.title('Swap Rates Sensitivity to Zero Curve Bumps')
        plt.xlabel('Bump in Basis Points')
        plt.ylabel('Swap Rate')
        plt.legend()
        plt.grid(True)
        self.save_fig('part1_2_bumps')

        plt.show()

    def plot_swap_rates(self, Scenarios):
        plt.figure(figsize=(10, 6))

        for maturity in Scenarios['scenario2']['part2']:

            years_to_maturity = maturity
            swap_rates = [rate for rate in Scenarios['scenario2']['part2']
                          [maturity]['amortization']]

            plt.plot([years_to_maturity] * len(swap_rates),
                     swap_rates, 'o-', label=f'Maturity {maturity} years')

        plt.title('Swap Rates vs Years to Maturity')
        plt.xlabel('Years to Maturity')
        plt.ylabel('Swap Rate')
        plt.legend()
        plt.grid(True)
        self.save_fig('part1_2_swap_amortization')
        plt.show()

    def plot_amortization_schedules(self, Scenarios):
        plt.figure(figsize=(10, 6))

        # Create a marker for each amortization schedule in the legend
        markers = ['o', 's', '^']
        labels = ['Amortization Full',
                  'Amortization Half', 'Amortization Zero']

        # Plot each maturity
        for idx, (maturity, data) in enumerate(Scenarios['scenario2']['part2'].items()):
            # Extract amortization schedules for each maturity
            amortization_schedules = data['amortization_schedule']
            swap_rates = data['amortization']

            # Plot amortization schedules
            for i, amortization in enumerate(amortization_schedules):
                plt.plot(maturity, swap_rates[i], markers[i],
                         label=labels[i] if idx == 0 else "", color='C'+str(idx))

        plt.title('Amortization Schedules vs Years to Maturity')
        plt.xlabel('Years to Maturity')
        plt.ylabel('Swap Rate')
        plt.legend()
        plt.grid(True)
        self.save_fig('part1_2_amortization')
        plt.show()

    def plot_bumped_swap_rates(self, Scenarios, maturities):
        plt.figure(figsize=(12, 8))

        # Loop over each bump scenario and plot the swap rates
        for bump_label, swap_rates in Scenarios['scenario3'].items():
            # Convert maturity years from integers to strings for plotting
            maturity_years = [str(maturity) for maturity in maturities]
            plt.plot(maturity_years, swap_rates,
                     marker='o', label=f'Bump {bump_label}')

        plt.title('Swap Rates vs Maturities for Different Bumps')
        plt.xlabel('Years to Maturity')
        plt.ylabel('Swap Rate')
        plt.legend()
        plt.grid(True)
        self.save_fig('part1_3_bumpedswap')
        plt.show()


    def plot_zerorates(self, zero_curve, european_zerorates):
        
        plt.plot(zero_curve.index, zero_curve['Zero Rates'], marker='o', label='Bootstrapped Zero Curve')
        # plt.plot(bond_maturities, yields, marker='x', linestyle='--', label='Yield Curve')
        plt.plot(european_zerorates.index, european_zerorates, marker='s', linestyle='-', label='European Zero Rates')

        plt.title('Zero Curve and Yield Curve Comparison')
        plt.xlabel('Years to Maturity')
        plt.ylabel('Rate')
        plt.legend()
        plt.grid(True)
        self.save_fig('part1_1_bootstrappedrates')
        plt.show()