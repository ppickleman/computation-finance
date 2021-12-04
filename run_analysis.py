'''
@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang
@Date          : June 2021

@Student Name  : Zilong Zheng

@Date          : Nov 2021

'''

import pandas as pd
import datetime

from stock import Stock
from DCF_model import DiscountedCashFlowModel

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

    
    as_of_date = datetime.date(2021, 12, 1)
    df = pd.read_csv(input_fname)
    
    # TODO
    results = []
    for index, row in df.iterrows():
        
        stock = Stock(row['Symbol'], 'annual')
        model = DiscountedCashFlowModel(stock, as_of_date)

        short_term_growth_rate = float(row['EPS Next 5Y in percent'])/100
        medium_term_growth_rate = short_term_growth_rate/2
        long_term_growth_rate = 0.04

        model.set_FCC_growth_rate(short_term_growth_rate, medium_term_growth_rate, long_term_growth_rate)
        
        fair_value = model.calc_fair_value()

        # pull additional fields
        # ...
        # DCF Value
        AYearDF = 1 / (1 + stock.lookup_wacc_by_beta(stock.get_beta()))
        FCF = stock.get_free_cashflow() # Free Cash Flow
        DCF = 0
        for i in range(1, 6):
            DCF += FCF * (1 + short_term_growth_rate) ** i * AYearDF ** i

        CF5 = FCF * (1 + short_term_growth_rate) ** 5

        for i in range(1, 6):
            DCF += CF5 * (1 + medium_term_growth_rate) ** i * AYearDF ** (i + 5)

        CF10 = CF5 * (1 + medium_term_growth_rate) ** 5

        for i in range(1, 11):
            DCF += CF10 * (1 + long_term_growth_rate) ** i * AYearDF ** (i + 10)
        try:
            PV = stock.get_cash_and_cash_equivalent() - stock.get_total_debt() + DCF
        except KeyError:
            result = "N/A"
            
        current_price = stock.get_daily_hist_price() # Current Price
        
        # Sector
        
        market_cap = stock.get_num_shares_outstanding() * current_price # Market Cap
        
        beta = stock.get_beta() # Beta
        
        total_asset = stock.get_cash_and_cash_equivalent# Total Assets
        
        total_debt = stock.get_total_debt() # Total Debt
        
        #earning per share
        eps = get_stock_earnings_data() / stock.get_num_shares_outstand() 
        p_e_ratio = current_price / eps # P/E Ratio
        # sales per share
        sps = company sales / stock.get_num_shares_outstand()
        p_s_ratio = current_price / sps # Price to Sale Ratio
        
        rsi = RSI(stock.ohlcv_df)
        rsi_indicator = rsi.run()# RSI
        
        ema = ExpontialMovingAverages(stock.ohlcv_df, 10)
        ema.run()
        day_10_ema = ema.get_series(10) # 10 day EMA
        
        periods = [20, 50, 200]
        smas = SimpleMovingAverages(stock.ohlcv_df, periods)
        smas.run()
        day_20_sma = smas.get_series(20) # 20 day SMA
        day_50_sma = smas.get_series(50) # 50 day SMA
        day_200_sma = smas.get_series(200) # 200 day SMA
        
        

    # save the output into a StockUniverseOutput.csv file

    # ....
    
    df.to_csv(output_fname, index = False, na_rep = 'N/A')
    
    # end TODO

    
if __name__ == "__main__":
    run()
