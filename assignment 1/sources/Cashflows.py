# https://canvas.vu.nl/courses/72644/files/folder/Assignments
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from scipy.interpolate import interp1d


class Cashflows():

    def __init__(self,):
        return

    def determine_discount_rate(self, payment_frequency, yield_curve, one_curve=True):
        """
        Determine discount rates based on yield curve and payment frequency.

        Parameters:
            payment_frequency (float): Payment frequency (e.g., 0.25 for quarterly, 0.5 for semi-annual, 1 for annual).
            yield_curve (dict): Dictionary containing yield curve data, including zero rates and Euribor rates.
            one_curve (bool): Boolean flag to indicate whether to use a single curve or two curves.

        Returns:
            list or tuple: List of zero rates or tuple of zero rates and floating discount rates.

        This function determines discount rates based on the provided yield curve data and payment frequency.
        If 'one_curve' is True, it returns the zero rates for the specified payment frequency.
        If 'one_curve' is False, it calculates interpolated zero rates and floating discount rates for the given
        payment frequency and returns a tuple containing zero rates and floating discount rates.
        """
        supported_frequencies = [0.25, 0.5, 1.0]

        if one_curve:
            zero_rates = yield_curve['zero_rate']
            if payment_frequency in supported_frequencies:
                return zero_rates
            else:
                raise ValueError(
                    "Unsupported payment frequency. Only 0.25 (quarterly), 0.5 (semi-annual), and 1.0 (annual) are supported.")
        else:
            zero_rates = yield_curve['zero_rate']
            euribor_rates = yield_curve['euribor']

            # Supported payment frequencies
            supported_frequencies = [0.25, 0.5, 1.0]
            if payment_frequency in supported_frequencies:
                return zero_rates, euribor_rates

    def interpolating_zero_rate(self, zero_curve, payment_dates):
        """
        Interpolate zero rates for a list of payment dates using a zero curve.

        Parameters:
            zero_curve (pd.Series): A Pandas Series containing zero rates for various maturities.
            payment_dates (list): List of payment dates corresponding to the zero rate interpolation.

        Returns:
            np.array: An array of interpolated zero rates for the provided payment dates.

        This function interpolates zero rates for a list of payment dates based on a given zero curve. It calculates the
        time to maturity in years for each payment date, then uses interpolation to estimate the zero rates for those
        dates. The function returns an array of interpolated zero rates.
        """

        start_date = payment_dates[0]
        years_to_maturity = (
            payment_dates - start_date).total_seconds() / (365 * 24 * 60 * 60)
        interpolating_function = interp1d(
            zero_curve.index, zero_curve, fill_value="extrapolate", bounds_error=False)
        interpolated_rates = interpolating_function(years_to_maturity)

        return interpolated_rates
        
    # IN:

    def calculate_fixed_cashflow(self, notional_amount, payment_dates, start_date, payment_frequency, fixed_rate, amortization_schedule):
        """
        Calculate fixed cash flows for an interest rate swap.

        Parameters:
            notional_amount (float): The initial notional amount.
            start_date (pd.Timestamp): The start date of the interest rate swap.
            end_date (pd.Timestamp): The end date of the interest rate swap.
            payment_frequency (float): Payment frequency (e.g., 0.5 for semi-annual).
            fixed_rate (float): The fixed interest rate for the swap.

        Returns:
            tuple: A tuple containing a list of fixed cash flows and payment dates.

        This function calculates fixed cash flows for an interest rate swap with a fixed rate. It determines payment dates
        based on the specified payment frequency, then computes the fixed cash flows for each payment date, excluding the
        start date, and returns them as a list along with the payment dates.
        """
        fixed_cash_flows = []

        for date in payment_dates:
            if date != start_date:
                current_notional = amortization_schedule[date] if amortization_schedule else notional_amount
                fixed_cash_flow = current_notional * fixed_rate * payment_frequency
                fixed_cash_flows.append(fixed_cash_flow)
        return np.array(fixed_cash_flows)

    def calculate_floating_cashflow(self, notional_amount, payment_dates, start_date, months, payment_frequency, reference_rate, amortization_schedule):
        """
        Calculate floating cash flows for an interest rate swap.

        Parameters:
            notional_amount (float): The initial notional amount.
            start_date (pd.Timestamp): The start date of the interest rate swap.
            end_date (pd.Timestamp): The end date of the interest rate swap.
            payment_frequency (float): Payment frequency (e.g., 0.5 for semi-annual).
            reference_rate (dict): Dictionary containing reference rates for different tenors.

        Returns:
            list: A list of floating cash flows.

        This function calculates floating cash flows for an interest rate swap with a reference rate. It determines payment
        dates based on the specified payment frequency, then computes the floating cash flows for each payment date,
        excluding the start date, using the corresponding reference rate for the given tenor.
        """

        floating_cashflows = []

        if isinstance(reference_rate, dict):
            rate_key = f'{months}months'
            rate = reference_rate.get(rate_key, None)
            if rate is None:
                raise ValueError(
                    f"No rate found for {rate_key} in reference_rate dictionary")
        else:
            interpolated_rates = self.interpolating_zero_rate(
                reference_rate, payment_dates)
            print(interpolated_rates)
        for idx, date in enumerate(payment_dates):
            if date != start_date:
                print(reference_rate)
                if not isinstance(reference_rate, dict):

                    rate = interpolated_rates[idx]
                print(rate)
                current_notional = amortization_schedule[date] if amortization_schedule else notional_amount
                floating_cash_flow = current_notional * rate * payment_frequency
                floating_cashflows.append(floating_cash_flow)

        return np.array(floating_cashflows)

    # OUT: DISCOUNTED

    def discount_cash_flows(self, cash_flows, payment_dates, zero_curve, payment_frequency):
        """
        Calculate the discounted cash flows for a given set of cash flows and payment dates using a zero curve.

        Parameters:
            cash_flows (list): List of cash flow values.
            payment_dates (list): List of payment dates corresponding to the cash flows.
            zero_curve (dict): Dictionary containing zero rates for various maturities.
            payment_frequency (float): Payment frequency (e.g., 0.5 for semi-annual).

        Returns:
            float: The sum of the discounted cash flows.
        """

        discounted_cash_flows = []
        start_date = payment_dates[0]

        # Interpolate the zero rates for the cash flow dates
        interpolated_rates = self.interpolating_zero_rate(zero_curve, payment_dates)
        
        for cash_flow, rate, date in zip(cash_flows, interpolated_rates, payment_dates):
            ttm = (date - start_date).days / 365.0  # Time to maturity in years
            discount_factor = np.exp(-rate *
                                     np.round(ttm, 3) / payment_frequency)
            discounted_cash_flows.append(cash_flow * discount_factor)

        return sum(discounted_cash_flows)
