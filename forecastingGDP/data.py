import pandas as pd

from fredapi import Fred

SERIES = {
    'gdp':'GDPC1',
    'prod_indus':'INDPRO',
    #'Manufacturing Production'
    'BusinessExpectations':'ATLSBUSRGEP',
    'Capacity_Utilization':'TCU',
    #'manuf_ISM':'ISM'

    'Manufacturers_New_Orders':'AMTMNO',
    'New_Orders_Non_defense_capital_good_ex_air':'NEWORDER',
    #'Building_permits'
    #'Housing_Starts'
    #'Construction Spending'
    #'new_car'
    #'Crude Oil Production'
    'Chicago_Fed_Activity_Index':'CFNAI',
    'University_of_Michigan_Consumer_Sentiment':'UMCSENT',
    #Philadelphia FedManufacturing Index

    'Advance_Retail_Sales':'MARTSMPCSM44000USS',
    'Real_Disposable_Personal_Income':'DSPIC96',
    'Personal_Consumption_Expenditure':'PCEC96',

    #Initial Jobless Claims
    'Unemployment_Rate':'UNRATE',
    'Employment_Leve':'CE16OV',
    'Non_farm_payroll':'PAYEMS',
    'Not in Labor Force':'LNU05026648',

    #'Average Hourly Wages'
    'Consumer_Price_Index':'CPIAUCSL',
    'Personal_Consumption_Expenditure_ex_food':'PCEPILFE',
    'Producer_Price_Index':'PPIACO',
    #'Oil Price'
    #'Unit Labour Cost'
    'Imports_Goods_Services':'IEAMGSN',
    'Exports_Goods_Services':'IEAXGS',
    'Imports_Goods_from_China':'IMPCH',

    'BofA_US_High_Yield_Index':'BAMLH0A0HYM2',
    'S&P_500':'SP500',
    'VIX_Volatility':'VIXCLS',
    '10YUST':'DGS10',
    '10YUST_2YUST':'T10Y2Y',
    'US_Dollar Index':'DTWEXAFEGS',
}

SERIES_ID = list(SERIES.values())

FREQUENCY = 'q'

FRED = Fred()

def get_data():
    '''returns a dataframe with GDP related series'''
    data = {}
    for series_id in SERIES_ID:
        data[series_id] = FRED.get_series(series_id, frequency=FREQUENCY)
    return pd.DataFrame(data)
