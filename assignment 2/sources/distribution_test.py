from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DistributionTest:
    def __init__(self) -> None:
        # Constructor for the DistributionTest class. Currently, it does not initialize any attributes.
        pass

    def run_Anderson_Darling_test(self, spread_data):
        """
        Perform the Anderson-Darling test to assess the log-normality of spread data.
        
        Parameters:
        - spread_data (array-like): An array containing the spread data to be tested.
        
        Prints the test statistic and critical values, and determines whether the spread
        data is log-normally distributed.
        """
        # Perform the Anderson-Darling test for log-normality on the log-transformed data.
        result = stats.anderson(np.log(spread_data))
        test_statistic = result.statistic
        critical_values = result.critical_values

        # Print the Anderson-Darling test statistic and corresponding critical values.
        print(f"Anderson-Darling Test Statistic: {test_statistic}")
        print(f"Critical Values: {critical_values}")

        # Compare the test statistic to the critical values to determine the result.
        alpha = 0.05  # Significance level
        if test_statistic < critical_values[2]:
            print("Spread data follows a log-normal distribution (fail to reject null hypothesis)")
        else:
            print("Spread data does not follow a log-normal distribution (reject null hypothesis)")

 