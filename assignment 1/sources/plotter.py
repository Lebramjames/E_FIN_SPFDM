import matplotlib.pyplot as plt


class Plotter:
    def __init__(self):

        return

    def save_fig(self, name):
        plt.savefig(
            fr'D:\studie\main_studie\files\stochastics_finance\E_FIN_SPFDM-1\assignment 1\plots\{name}.png')

    def plot_amortization_schedules(self, Scenarios, maturities):
        """
        plot scaneraio 2: amortizaiton
        """
        plt.figure(figsize=(10, 6))
        for amortization, rates in Scenarios['scenario2'].items():
            if amortization == 100:
                plt.plot(maturities, rates, label=f'No Amortization')
            else:
                plt.plot(maturities, rates,
                         label=f'Amortizated till {amortization}')

        plt.title('Swap Rates for Different Amortization Schedules')
        plt.xlabel('Maturity (Years)')
        plt.ylabel('Swap Rate (%)')
        plt.grid(True)
        plt.legend()
        plt.savefig('plots/amortizing_schedule.png')
        plt.show()

    def plot_bumped_swap_rates(self, Scenarios, maturities, fixed_rate):
        """
        used for scenario 3
        """
        plt.figure(figsize=(12, 8))

        # Loop over each bump scenario and plot the swap rates
        for bump_label, swap_rates in Scenarios['scenario3'].items():
            # Convert maturity years from integers to strings for plotting
            maturity_years = [str(maturity) for maturity in maturities]
            plt.plot(maturity_years, swap_rates,
                     marker='o', label=f'Bump {bump_label}')

        plt.title(
            f'Swap Rates vs Maturities for Different Bumps (fixed rate: {fixed_rate*100}%, notional amount 100)')
        plt.xlabel('Years to Maturity')
        plt.ylabel('Swap Value')

        plt.legend()
        plt.grid(True)
        self.save_fig('part1_3_bumpedswap')
        plt.show()

    def plot_zerorates(self, zero_curve, european_zerorates, zero_rates_rf):
        """
        used for bootstrap method
        """
        plt.plot(zero_curve.index,
                 zero_curve['Zero Rates'], label='Bootstrapped Zero Curve')
        # plt.plot(bond_maturities, yields, marker='x', linestyle='--', label='Yield Curve')
        plt.plot(european_zerorates.index, european_zerorates,
                 linestyle='-', label='European Zero Rates')
        plt.plot(zero_rates_rf.index, zero_rates_rf, linestyle='-',
                 label='Zero Rates Discounted (Risk Free)')

        plt.title('Zero Curve and Yield Curve Comparison')
        plt.xlabel('Years to Maturity')
        plt.ylabel('Rate')
        plt.legend()
        plt.grid(True)
        self.save_fig('part1_1_bootstrappedrates')
        plt.show()

    def plot_scenario2_bumps(self, Scenarios, maturities):
        fig, axs = plt.subplots(3, 3, figsize=(20, 16))
        fig.suptitle(
            'Swap Rates for Various Basis Points and Payment Frequencies')

        # Iterate over each subplot
        for i, (bp, data) in enumerate(Scenarios['scenario2'].items()):
            row, col = divmod(i, 3)
            ax = axs[row, col]
            for freq, rates in data.items():
                ax.plot(maturities, rates, label=f'Freq: {freq} years')
            ax.set_title(f'Basis Points: {bp}')
            ax.set_xlabel('Maturity (Years)')
            ax.set_ylabel('Swap Rate (%)')
            ax.grid(True)
            ax.legend()
            # Setting the same y-axis range for all plots
            ax.set_ylim(2.5, 3.5)

        # Adjust layout
        plt.tight_layout()
        plt.subplots_adjust(top=0.95)

        plt.savefig('plots/swaprates_bumps2_.png')
        plt.show()
