'''

@project       : Queens College CSCI 365/765 Computational Finance
@Instructor    : Dr. Alex Pang

@Group Name    : group 11
@Student Name  : Zilong Zheng, Yinan Du, Brian Luu

@Date          : Fall 2021

A Bond Calculator Class

'''

import math
import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from bisection_method import bisection

import enum
import calendar

from datetime import date

from bond import Bond, DayCount, PaymentFrequency


def get_actual360_daycount_frac(start, end):
    day_in_year = 360
    day_count = (end - start).days
    return(day_count / day_in_year)

def get_30360_daycount_frac(start, end):
    day_in_year = 360
    day_count = 360*(end.year - start.year) + 30*(end.month - start.month - 1) + \
                max(0, 30 - start.day) + min(30, end.day)
    return(day_count / day_in_year )
    

def get_actualactual_daycount_frac(start, end):
    # TODO
    if((calendar.isleap(start.year) == 1 or calendar.isleap(end.year) == 1) and (end.year != start.year)): day_in_year = (366+365)/2
    elif(calendar.isleap(start.year) == 1 or calendar.isleap(end.year) == 1): day_in_year = 366
    else: day_in_year = 365
    
    day_count = (end - start).days
    result = (day_count / day_in_year)
    # end TODO
    return(result)

class BondCalculator(object):
    '''
    Bond Calculator class for pricing a bond
    '''

    def __init__(self, pricing_date):
        self.pricing_date = pricing_date

    def calc_one_period_discount_factor(self, bond, yld):
        #TODO
        payment_frequency = bond.payment_freq
        if payment_frequency == PaymentFrequency.ANNUAL:
            freq = 1
        elif payment_frequency == PaymentFrequency.SEMIANNUAL:
            freq = 2
        elif payment_frequency == PaymentFrequency.QUARTERLY:
            freq = 4
        elif payment_frequency == PaymentFrequency.MONTHLY:
            freq = 12
        else:
            raise Exception("Unsupported Payment Frequency")

        return 1 / (1 + yld / freq)


    def calc_clean_price(self, bond, yld):
        '''
        Calculate bond price as of the pricing_date for a given yield
        bond price should be expressed in percentage eg 100 for a par bond
        '''
        px = None
        
        one_period_factor = self.calc_one_period_discount_factor(bond, yld)
        # TODO: implement calculation here
        DF = [math.pow(one_period_factor, i+1) for i in range(len(bond.coupon_payment))]
        CF = bond.coupon_payment.copy()
        CF[-1] += bond.principal
        PVs = [ CF[i] * DF[i] for i in range(len(bond.coupon_payment))]
        TotalPV=0
        for i in PVs:
            TotalPV = TotalPV + i
            
        px = TotalPV/bond.principal
        
        return(px*100)

        # end TODO:
        

    def calc_accrual_interest(self, bond, settle_date):
        '''
        calculate the accrual interest on given a settle_date
        by calculating the previous payment date first and use the date count
        from previous payment date to the settle_date
        '''
        #todo
        prev_pay_date = bond.get_previous_payment_date(settle_date)

        if bond.day_count == DayCount.DAYCOUNT_30360:
            frac = get_30360_daycount_frac(prev_pay_date, settle_date)
            
        elif bond.day_count == DayCount.DAYCOUNT_ACTUAL_360:
            frac = get_actual360_daycount_frac(prev_pay_date, settle_date)
            
        elif bond.day_count == DayCount.DAYCOUNT_ACTUAL_ACTUAL:
            frac = get_actualactual_daycount_frac(prev_pay_date, settle_date)
        else:
            raise Exception("error Day Count")

        result=frac * bond.coupon * bond.principal / 100
        # end TODO
        return(result)

    def calc_macaulay_duration(self, bond, yld):
        '''
        time to cashflow weighted by PV
        '''
        # TODO: implement details here
        one_period_factor = self.calc_one_period_discount_factor(bond, yld)
        
        DF = [math.pow(one_period_factor, i+1) for i in range(len(bond.coupon_payment))]
        CF = [c for c in bond.coupon_payment]
        CF[-1] += bond.principal
        
        PVs = [ CF[i] * DF[i] for i in range(len(bond.coupon_payment))]
        wavg = [bond.payment_times_in_year[i] * PVs[i] for i in range(len(bond.coupon_payment))]
        result =( sum(wavg) / sum(PVs))

        # end TODO
        return(result)

    def calc_modified_duration(self, bond, yld):
        '''
        calculate modified duration at a certain yield yld
        '''
        D = self.calc_macaulay_duration(bond, yld)

        # TODO: implement details here
        one_period_factor = self.calc_one_period_discount_factor(bond, yld)
        result= D*one_period_factor
        # end TODO:
        return(result)

    def calc_yield(self, bond, bond_price):
        '''
        Calculate the yield to maturity on given a bond price using bisection method
        '''

        def match_price(yld):
            calculator = BondCalculator(self.pricing_date)
            px = calculator.calc_clean_price(bond, yld)
            return(px - bond_price)

        # TODO: implement details here
        yld, n_iteractions = bisection(match_price, 0, 1, eps=1.0e-6)
        # end TODO:
        return(yld)

    def calc_convexity(self, bond, yld):
        # calculate convexity of a bond at a certain yield yld
        #todo
        one_period_factor = self.calc_one_period_discount_factor(bond, yld)
        
        df = [math.pow(one_period_factor, i + 1) for i in range(len(bond.coupon_payment))]
        cf = bond.coupon_payment.copy()
        cf[-1] += bond.principal
        pv = [cf[i] * df[i] for i in range(len(bond.coupon_payment))]

        payment_times = bond.payment_times_in_year

        wavg = [payment_times[i] * pv[i] * (payment_times[i] + payment_times[0]) * one_period_factor ** 2
                       for i in range(len(bond.payment_times_in_year))]

        result=sum(wavg) / sum(pv)
        return(result)


##########################  some test cases ###################

def _example2():
    pricing_date = date(2021, 1, 1)
    issue_date = date(2021, 1, 1)
    engine = BondCalculator(pricing_date)

    # Example 2
    bond = Bond(issue_date, term=10, day_count = DayCount.DAYCOUNT_30360,
                 payment_freq = PaymentFrequency.ANNUAL, coupon = 0.05)

    yld = 0.06
    px_bond2 = engine.calc_clean_price(bond, yld)
    print("The clean price of bond 2 is: ", format(px_bond2, '.4f'))
    assert( abs(px_bond2 - 92.640) < 0.01)

    
def _example3():
    pricing_date = date(2021, 1, 1)
    issue_date = date(2021, 1, 1)
    engine = BondCalculator(pricing_date)

    
    bond = Bond(issue_date, term = 2, day_count =DayCount.DAYCOUNT_30360,
                 payment_freq = PaymentFrequency.SEMIANNUAL,
                 coupon = 0.08)

    yld = 0.06
    px_bond3 = engine.calc_clean_price(bond, yld)
    print("The clean price of bond 3 is: ", format(px_bond3, '.4f'))
    assert( abs(px_bond3 - 103.717) < 0.01)


def _example4():
    # unit tests
    pricing_date = date(2021, 1, 1)
    issue_date = date(2021, 1, 1)
    engine = BondCalculator(pricing_date)

    # Example 4 5Y bond with semi-annual 5% coupon priced at 103.72 should have a yield of 4.168%
    price = 103.72
    bond = Bond(issue_date, term=5, day_count = DayCount.DAYCOUNT_30360,
                payment_freq = PaymentFrequency.SEMIANNUAL, coupon = 0.05, principal = 100)
    

    yld = engine.calc_yield(bond, price)

    print("The yield of bond 4 is: ", yld)

    assert( abs(yld - 0.04168) < 0.01)
    
def _test():
    # basic test cases
    _example2()
    _example3()
    _example4()

    

if __name__ == "__main__":
    _test()
