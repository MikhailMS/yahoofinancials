# YahooFinancials Unit Tests v1.5
# Version Released: 01/27/2019
# Author: Connor Sanders
# Tested on Python 2.7, 3.3, 3.4, 3.5, 3.6, and 3.7
# Copyright (c) 2019 Connor Sanders
# MIT License

import pytest
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from yahoofinancials import YahooFinancials


# Test Configuration Variables
STOCKS        = ['AAPL', 'MSFT', 'C', 'IL&FSTRANS.NS']
CURRENCIES    = ['EURUSD=X', 'JPY=X', 'GBPUSD=X']
US_TREASURIES = ['^TNX', '^IRX', '^TYX']


# Global function to check Fundamental Test results
def check_fundamental(test_data, test_type):
    if test_type == 'bal':
        if 'balanceSheetHistoryQuarterly' in test_data and test_data['balanceSheetHistoryQuarterly']['C'] is not None:
            return True
        else:
            return False
    elif test_type == 'inc':
        if 'incomeStatementHistoryQuarterly' in test_data and \
                        test_data['incomeStatementHistoryQuarterly']['C'] is not None:
            return True
        else:
            return False
    elif test_type == 'all':
        if 'balanceSheetHistoryQuarterly' in test_data and 'incomeStatementHistoryQuarterly' in test_data and \
                        'cashflowStatementHistoryQuarterly' in test_data:
            return True
        else:
            return False


@pytest.fixture
def setup():
    proxies = {}

    data_dict = {
        'stock_single':      YahooFinancials('C', proxies=proxies),
        'stock_multi':       YahooFinancials(STOCKS, proxies=proxies),
        'treasuries_single': YahooFinancials('^IRX', proxies=proxies),
        'treasuries_multi':  YahooFinancials(US_TREASURIES, proxies=proxies),
        'currencies':        YahooFinancials(CURRENCIES, proxies=proxies)
    }

    return data_dict

def test_yf_fundamentals(setup):
    '''
    Test YahooFinancials fundamentals
    '''
    data = setup

    # Single stock test
    single_balance_sheet_data_qt    = data.get('stock_single').get_financial_stmts('quarterly', 'balance')
    single_income_statement_data_qt = data.get('stock_single').get_financial_stmts('quarterly', 'income')
    single_all_statement_data_qt    = data.get('stock_single').get_financial_stmts('quarterly',
                                                                                   ['income', 'cash', 'balance'])
    # Multi stock test
    multi_balance_sheet_data_qt    = data.get('stock_multi').get_financial_stmts('quarterly', 'balance')
    multi_income_statement_data_qt = data.get('stock_multi').get_financial_stmts('quarterly', 'income')
    multi_all_statement_data_qt    = data.get('stock_multi').get_financial_stmts('quarterly',
                                                                                 ['income', 'cash', 'balance'])
    # Single stock check
    result = check_fundamental(single_balance_sheet_data_qt, 'bal')
    assert result == True

    result = check_fundamental(single_income_statement_data_qt, 'inc')
    assert result == True

    result = check_fundamental(single_all_statement_data_qt, 'all')
    assert result == True

    # Multi stock check
    result = check_fundamental(multi_balance_sheet_data_qt, 'bal')
    assert result == True

    result = check_fundamental(multi_income_statement_data_qt, 'inc')
    assert result == True

    result = check_fundamental(multi_all_statement_data_qt, 'all')
    assert result == True

def test_yf_historical_price(setup):
    '''
    Test YahooFinancials historical prices
    '''
    data = setup

    single_stock_prices = data.get('stock_single').get_historical_price_data('2015-01-15', '2017-10-15', 'weekly')
    expect_dict = {
        'high':           49.099998474121094,
        'volume':         125737200,
        'formatted_date': '2015-01-12',
        'low':            46.599998474121094,
        'adjclose':       44.10297393798828,
        'date':           1421038800,
        'close':          47.61000061035156,
        'open':           48.959999084472656
    }
    assert single_stock_prices['C']['prices'][0] == expect_dict

def test_yf_dividend_price(setup):
    '''
    Test YahooFinancials historical stock daily dividend
    '''
    data = setup

    single_stock_dividend = data.get('stock_single').get_daily_dividend_data('1986-09-15', '1987-09-15')
    expect_dict = {"C": [{"date": 533313000, "formatted_date": "1986-11-25", "amount": 0.02999},
                         {"date": 541348200, "formatted_date": "1987-02-26", "amount": 0.02999},
                         {"date": 544714200, "formatted_date": "1987-04-06", "amount": 0.332},
                         {"date": 549120600, "formatted_date": "1987-05-27", "amount": 0.02999},
                         {"date": 552576600, "formatted_date": "1987-07-06", "amount": 0.332},
                         {"date": 557501400, "formatted_date": "1987-09-01", "amount": 0.02999}]
                  }
    assert single_stock_dividend == expect_dict

def test_yf_module_methods(setup):
    '''
    Test YahooFinancials extra module methods
    '''
    data = setup

    # Stocks
    if isinstance(data.get('stock_single').get_current_price(), float):
        assert True
    else:
        assert False
    if isinstance(data.get('stock_single').get_net_income(), int):
        assert True
    else:
        assert False

    # Treasuries
    if isinstance(data.get('treasuries_single').get_current_price(), float):
        assert True
    else:
        assert False
