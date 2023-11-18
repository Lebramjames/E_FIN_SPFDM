# https://canvas.vu.nl/courses/72644/files/folder/Assignments
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from scipy.interpolate import interp1d


class Cashflows():

    def __init__(self,):
        return

    # IN:

    def calculate_fixed_cashflow(self, notional_amount, payment_dates, payment_frequency, fixed_rate, amortization_schedule):
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
            current_notional = amortization_schedule[date] if amortization_schedule else notional_amount
            fixed_cash_flow = current_notional * fixed_rate * payment_frequency
            fixed_cash_flows.append(fixed_cash_flow)

        return np.array(fixed_cash_flows)

    def calculate_floating_cashflow(self, notional_amount, payment_dates, payment_frequency, floating_rate_curve, amortization_schedule, euribor_swap):
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

        for idx, date in enumerate(payment_dates):
            current_notional = amortization_schedule[date] if amortization_schedule else notional_amount
            if idx == 0:
                rate_forward = 0.029
                floating_cash_flow = current_notional * \
                    rate_forward * payment_frequency
            else:
                rate1 = floating_rate_curve[date-payment_frequency]
                rate2 = floating_rate_curve[date]

                maturity1 = payment_dates[idx-1]
                maturity2 = payment_dates[idx]

                rate_forward = self.calc_forward_rate(
                    rate1, rate2, maturity1, maturity2)
                floating_cash_flow = current_notional * \
                    (1/payment_frequency)*(np.exp(rate_forward /
                                                  (1/payment_frequency))-1) * payment_frequency

            floating_cashflows.append(floating_cash_flow)
        return np.array(floating_cashflows)

    def calc_forward_rate(self, rate1, rate2, maturity1, maturity2):
        """
        Calculate the forward rate between two periods.

        Parameters:
            rate1 (float): The interest rate for the first period.
            rate2 (float): The interest rate for the second period.
            maturity1 (float): The maturity of the first rate.
            maturity2 (float): The maturity of the second rate.

        Returns:
            float: The calculated forward rate.
        """
        rate_forward = (rate2 * maturity2 - rate1 *
                        maturity1) / (maturity2 - maturity1)
        return rate_forward

    # OUT: DISCOUNTED

    def discount_cash_flows(self, cash_flows, payment_dates, discount_rate_cash_flow):
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
        discount_factor_list = []

        for cash_flow, date in zip(cash_flows, payment_dates):
            discount_factor = np.exp(
                -discount_rate_cash_flow[date] * date)
            discount_factor_list.append(discount_factor)
            discounted_cash_flows.append(cash_flow * discount_factor)

        return sum(discounted_cash_flows), discount_factor_list,discounted_cash_flows

