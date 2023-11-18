class Bootstrap():
    euribor_rates = get_euribordata()
    euribor_rates_list = [0.03896, 0.03834, euribor_rates['3months']/100, euribor_rates['6months']/100, euribor_rates['12months']/100]

euribor_rates = {
    '1 week': euribor_rates_list[0],
    '1 month': euribor_rates_list[1],
    '3 month': euribor_rates_list[2],
    '6 months': euribor_rates_list[3],
    '12 months': euribor_rates_list[4]
}

bond_price_1procent_coupon = {
    '2 years': 95.96,
    '3 years': 94.68,
    '4 years': 93.43,
    '5 years': 92.01,
    '6 years': 90.53,
    '7 years': 88.98,
    '8 years': 87.30,
    '9 years': 85.52,
    '10 years': 83.72,
    '15 years': 75.45,
    '20 years': 69.50,
    '25 years': 64.90,
    '30 years': 60.55,
}

bond_maturities = [
    2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30
]

yields = [
    3.114, 2.878, 2.757, 2.731, 2.732, 2.753, 2.793, 2.846, 2.899, 3.066, 3.062, 3.020, 3.017
]

face_value = 100
payments_per_year = 1
coupon_rate = -1

def bond_price_from_yields(yield_rate, bond_maturities, face_value, coupon_rate, payments_per_year):
    periods = bond_maturities * payments_per_year
    discount_factor = np.exp(-yield_rate/100/payments_per_year)#1/(1+yield_rate/100/payments_per_year)
    pv_coupons = npf.pv(rate= yield_rate/100/payments_per_year, nper=periods, pmt=coupon_rate/payments_per_year, when=1)
    pv_face_value = face_value * discount_factor ** periods
    return pv_coupons + pv_face_value
    
    
def bootstrap_zero_curve(bond_price_1procent_coupon, euribor_rates, bond_maturities, face_value, payments_per_year, coupon_rate):
    zero_curve = pd.DataFrame(index=bond_maturities, columns=['Zero Rates'])
    #first_rate = pd.DataFrame(euribor_rates.iloc[:], index=1)
    #print(first_rate)
    
    for i, maturity in enumerate(bond_maturities):
        initial_gues= 0.02
        zero_rate = fsolve(lambda x: bond_price_from_yields(x, maturity, face_value, coupon_rate, payments_per_year)-bond_price_1procent_coupon[f'{maturity} years'], x0=initial_gues)[0]
        zero_curve.at[maturity] = zero_rate#+0.04
        
        #print(f'Maturity: {maturity} years, Zero Rate: {zero_rate}, Bond Price: {bond_price_from_yields(zero_rate, maturity,face_value, coupon_rate, payments_per_year)}')
    
    #print(zero_curve)
    return(zero_curve)
zero_curve = bootstrap_zero_curve(bond_price_1procent_coupon, euribor_rates, bond_maturities, face_value, payments_per_year, coupon_rate)


yield_df = pd.DataFrame({'Yields': yields}, index=bond_maturities)
#euribor_rates_list = [euribor_rates_list[4]]
#euribor_1year = pd.DataFrame(euribor_rates_list)
#zero_curve = pd.concat([euribor_1year, zero_curve], axis=1)
#euribor_1year_value = euribor_rates_list[4]

# Create a DataFrame with the selected value
#euribor_1year = pd.DataFrame([euribor_1year_value], columns=['Euribor 1 Year'], index=[1])

# Concatenate the DataFrames along axis 1 (columns)
#zero_curve = pd.concat([euribor_1year, zero_curve], axis=1)
print(zero_curve)
plt.plot(zero_curve, label = 'Zero Curve')
plt.plot(yield_df, label='yield curve')
plt.legend()
plt.show()