'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021
@Student Name  : Zilong Zheng, Yinan Du, Brian Luu
@Date          : Nov 2021
'''

import pandas as pd
import datetime
import yfinance as yf
from stock import Stock
from DCF_model import DiscountedCashFlowModel
from TA import SimpleMovingAverages, ExponentialMovingAverages, RSI

def run():
    '''
    Read in the input file.
    Call the DCF to compute its DCF value and add the following columns to the output file.
    You are welcome to add additional valuation metrics as you see fit
    Symbol
    EPS Next 5Y in percent
    DCF Value
    Current Price
    Sector
    Market Cap
    Beta
    Total Assets
    Total Debt
    Free Cash Flow
    P/E Ratio
    Price to Sale Ratio
    RSI
    10 day EMA
    20 day SMA
    50 day SMA
    200 day SMA
    '''
    input_fname = "StockUniverse.csv"
    output_fname = "StockUniverseOutput.csv"

    start_date = datetime.date(2020, 12, 1)
    as_of_date = datetime.date(2021, 12, 5)
    df = pd.read_csv(input_fname)


    # TODO
    DCF = []
    current_price = []
    sector = []
    market_cap = []
    beta = []
    total_assets = []
    total_debt = []
    free_cashflow = []
    p_e_ratio = []
    p_s_ratio = []
    rsi_list = []
    day_10_ema = []
    day_20_sma = []
    day_50_sma = []
    day_200_sma = []

    for index, row in df.iterrows():

        stock = Stock(row['Symbol'], 'annual')
        model = DiscountedCashFlowModel(stock, as_of_date)

        short_term_growth_rate = float(row['EPS Next 5Y in percent'])/100
        medium_term_growth_rate = short_term_growth_rate/2
        long_term_growth_rate = 0.04

        model.set_FCC_growth_rate(short_term_growth_rate, medium_term_growth_rate, long_term_growth_rate)

        # pull additional fields
        # ...

        # DCF Value
        try:
            fair_value = model.calc_fair_value()
            DCF.append(fair_value)
        except:
            DCF.append('blank')
            
        # current price
        try:
          current_price.append(stock.get_current_price())
        except:
          current_price.append('blank')

        #sector
        try:
            result = yf.Ticker(stock.symbol)
            sector.append(result.info['sector'])
        except:
            sector.append('blank')

        # market cap
        try:
          market_cap.append(stock.get_market_cap())
        except:
          market_cap.append('blank')

        # beta
        try:
          beta.append(stock.get_beta())
        except:
          beta.append('blank')

        # total assets
        try:
          total_assets.append(stock.get_cash_and_cash_equivalent())
        except:
          total_assets.append('blank')

        #total debt
        try:
          total_debt.append(stock.get_total_debt())
        except:
          total_debt.append('blank')

        # free cash flow
        try:
          free_cashflow.append(stock.get_free_cashflow())
        except:
          free_cashflow.append('blank')

        # P/E Ratio
        try:
          p_e_ratio.append(stock.get_pe_ratio())
        except:
          p_e_ratio.append('blank')

        # P/S ratio
        try:
          p_s_ratio.append(stock.get_price_to_sales())
        except:
          p_s_ratio.append('blank')

        # 10 day ema
        periods = [10, 20, 50, 200]
        stock.get_daily_hist_price(start_date, as_of_date)
        emas = ExponentialMovingAverages(stock.ohlcv_df, periods)
        emas.run()
        e1 = emas.get_series(10)
        day_10_ema.append(e1['2021-12-03'])

        # 20 day sma
        smas = SimpleMovingAverages(stock.ohlcv_df, periods)
        smas.run()
        s1 = smas.get_series(20)
        day_20_sma.append(s1['2021-12-03'])

        # 50 day sma
        s2 = smas.get_series(50)
        day_50_sma.append(s2['2021-12-03'])

        # 200 day sma
        s3 = smas.get_series(200)
        day_200_sma.append(s3['2021-12-03'])

        #rsi
        rsi_indicator = RSI(stock.ohlcv_df)
        rsi_indicator.run()
        rsi_list.append(rsi_indicator.rsi['2021-12-03'])

    # save the output into a SwotockUniverseOutput.csv file

    # ....
    df['DCF value'] = DCF
    df['Current Price'] = current_price
    df['Sector'] = sector
    df['Market Cap'] = market_cap
    df['Beta'] = beta
    df['Total Assets'] = total_assets
    df['Total Debt'] = total_debt
    df['Free Cash Flow'] = free_cashflow
    df['P/E Ratio'] = p_e_ratio
    df['P/S Ratio'] = p_s_ratio
    df['RSI'] = rsi_list
    df['10 day EMA'] = day_10_ema
    df['20 day SMA'] = day_20_sma
    df['50 day SMA'] = day_50_sma
    df['200 day SMA'] = day_200_sma

    df.to_csv(output_fname, index = False)

    print(df)
    # end TODO


if __name__ == "__main__":
    run()
