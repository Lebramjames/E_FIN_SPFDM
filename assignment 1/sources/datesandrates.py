import pandas as pd


class DatesAndRates():

    def __init__(self, ):
        return

    def calc_interpolatingrate(self, date, zero_rate_series):
        before = zero_rate_series[zero_rate_series.index <= date]
        after = zero_rate_series[zero_rate_series.index > date]

        if not before.empty and not after.empty:
            before_date, before_rate = before.index[-1], before.iloc[-1]
            after_date, after_rate = after.index[0], after.iloc[0]

            # Exponential interpolation
            rate = before_rate * \
                (after_rate / before_rate) ** ((date -
                                                before_date) / (after_date - before_date))
        elif not before.empty:
            # If the date is beyond the range, use the closest known rate

            rate = before.iloc[-1]
        elif not after.empty:
            # If the date is before the range, use the closest known rate
            rate = after.iloc[0]
        else:
            raise ValueError("Zero rate series is empty")

        return rate

    def get_paymentdates(self, maturity, first_receiving_date, payment_frequency):
        current_date = first_receiving_date
        payment_dates = []

        while current_date <= maturity:
            payment_dates.append(current_date)
            current_date += payment_frequency

        return payment_dates

    def get_euribordata(self, payment_dates, euribor):

        euribor_series = pd.Series(euribor, index=euribor.keys())
        euribor_data = self.calc_interpolatingrate(
            payment_dates[0], euribor_series)
        return euribor_data

    def align_zero_rates(self, payment_dates, zero_rate_series):
        rates = []

        for date in payment_dates:
            rate = self.calc_interpolatingrate(date, zero_rate_series)
            rates.append(rate)

        payment_dates_with_rates = dict(zip(payment_dates, rates))
        return payment_dates_with_rates

    def run(self, maturity, first_receiving_date, payment_frequency, zero_rate_series, euribor):

        payment_dates = self.get_paymentdates(
            maturity, first_receiving_date, payment_frequency)
        zero_rates_aligned = self.align_zero_rates(
            payment_dates, zero_rate_series)

        euribor_aligned = self.get_euribordata(payment_dates, euribor)
        
        return payment_dates, zero_rates_aligned, euribor_aligned

    def create_amortization_schedule(self, notional_amount, final_notional, payment_frequency, maturity, first_receiving_date):
        payment_dates = self.get_paymentdates(
            maturity, first_receiving_date, payment_frequency)
        num_periods = len(payment_dates)

        amortization_steps = (
            notional_amount - final_notional) / (num_periods - 1)

        notional_amounts = []

        for i in range(num_periods):
            amortized_notional = notional_amount - i * amortization_steps
            notional_amounts.append(amortized_notional)
        return dict(zip(payment_dates, notional_amounts))


    def calculate_swap_rate(self, df, basis_points): 
        adjustments = basis_points/1000 #to decimals
        return df + adjustments
    
