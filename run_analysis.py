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

    
    as_of_date = datetime.date(2021, 12, 1)
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
    RSI = []
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
        
        #fair_value = model.calc_fair_value()

        # pull additional fields
        # ...
        # DCF Value   

        # current price  
        try:
          current_price.append(stock.get_current_price())
        except:
          current_price.append('blank')

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

        '''    
        current_price = stock.get_current_price() # Current Price
        
        sector = yf.Ticker(stock.symbol)# Sector
        
        market_cap = stock.get_market_cap() # Market Cap
        
        beta = stock.get_beta() # Beta
        
        total_asset = stock.get_cash_and_cash_equivalent()# Total Assets
        
        total_debt = stock.get_total_debt() # Total Debt
       
        p_e_ratio = stock.get_pe_ratio() # P/E Ratio

        p_s_ratio = stock.get_price_to_sales() # Price to Sale Ratio
        
        #rsi = RSI(stock.ohlcv_df)
        #rsi_indicator = rsi.run()# RSI
        
        #ema = ExponentialMovingAverages(stock.ohlcv_df, 10)
        #ema.run()
        #day_10_ema = ema.get_series(10) # 10 day EMA
        
        #periods = [20, 50, 200]
        #smas = SimpleMovingAverages(stock.ohlcv_df, periods)
        #smas.run()
        #day_20_sma = smas.get_series(20) # 20 day SMA
        #day_50_sma = smas.get_series(50) # 50 day SMA
        #day_200_sma = smas.get_series(200) # 200 day SMA
        '''

    # save the output into a SwotockUniverseOutput.csv file

    # ....
    #print(results)
    df['DCF value'] = ''
    df['Current Price'] = current_price
    df['Sector'] = ''
    df['Market Cap'] = market_cap
    df['Beta'] = beta
    df['Total Assets'] = total_assets
    df['Total Debt'] = total_debt
    df['Free Cash Flow'] = free_cashflow
    df['P/E Ratio'] = p_e_ratio
    df['P/S Ratio'] = p_s_ratio
    df['RSI'] = ''
    df['10 day EMA'] = ''
    df['20 day SMA'] = ''
    df['50 day SMA'] = ''
    df['200 day SMA'] = ''

    df.to_csv(output_fname, index = False)
    print(df)
    # end TODO

    
if __name__ == "__main__":
    run()
