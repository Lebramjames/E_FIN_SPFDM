from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DistributionTest:

    def __init__(self) -> None:
        pass


    def run_Anderson_Darling_test(self, spread_data):
        # Perform the Anderson-Darling test for log-normality
        result = stats.anderson(np.log(spread_data))

        # Extract the test statistic and critical values
        test_statistic = result.statistic
        critical_values = result.critical_values

        # Print the Anderson-Darling test statistic and critical values
        print(f"Anderson-Darling Test Statistic: {test_statistic}")
        print(f"Critical Values: {critical_values}")

        # Determine if the data is log-normally distributed based on the test statistic
        # and critical values (you can adjust the significance level)
        alpha = 0.05
        if test_statistic < critical_values[2]:
            print("Spread data follows a log-normal distribution (fail to reject null hypothesis)")
        else:
            print("Spread data does not follow a log-normal distribution (reject null hypothesis)")

    def plot_lognormaldistribution(self, spread_data):
        # Plot a histogram of the data
        sns.histplot(spread_data, bins=100, kde=True, color='b', label='Spread Data', stat='density')

        # Fit a log-normal distribution to the data
        shape, loc, scale = stats.lognorm.fit(spread_data)
        x = np.linspace(min(spread_data), max(spread_data), 100)
        pdf = stats.lognorm.pdf(x, shape, loc=loc, scale=scale)
        plt.plot(x, pdf, 'r-', label='Log-Normal Fit')

        # Add labels and a legend
        plt.xlabel('Spread')
        plt.ylabel('Probability Density')
        plt.legend()

        # Show the plot
        plt.show()