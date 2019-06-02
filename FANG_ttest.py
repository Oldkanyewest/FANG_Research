import pandas as pd
import pandas_datareader as web
import matplotlib as plt
import datetime as dt
from scipy import stats

pd.set_option('display.max_columns', 30)

symbols = ['FB', 'AMZN', 'NFLX', 'GOOGL']

start = dt.datetime(2016, 1, 1)

end = dt.datetime(2018, 12, 31)


def archivedata(tickers, start, end):
    for i in tickers:
        file = web.DataReader(i, 'iex', start, end)
        file.to_csv('{}_Data.csv'.format(str(i)))
        return


def joindataframe(tickers):
    if 'SPY' not in tickers:
        index = pd.read_csv('SPY_Data.csv', index_col='date', parse_dates=True, usecols=['date', 'close'])
        index = index.rename(columns={'close': 'SPY_close'})
    for i in tickers:
        if i not in index:
            dframe = pd.read_csv('{}_Data.csv'.format(str(i)), index_col='date', parse_dates=True, usecols=['date', 'close'])
            dframe = dframe.rename(columns={'close': '{}_close'.format(str(i))})
            index = index.join(dframe, how='left')
    return index


def geomean(array):
    gfactor = 1 + .01 * array
    product = gfactor.product()
    return product ** (1/len(array))


def seperator():
    print('*' * 100)
    return


fang = joindataframe(symbols)

print(fang.head())

fang['SPY pct_chg'] = fang['SPY_close'].pct_change() * 100

fang['FANG pct_chg'] = fang['FB_close'] + fang['AMZN_close'] + fang['NFLX_close'] + fang['GOOGL_close']

fang['FANG pct_chg'] = fang['FANG pct_chg'].pct_change() * 100

fang['SPY pct_chg'].fillna(0, inplace=True)
fang['FANG pct_chg'].fillna(0, inplace=True)

print(fang.head())


def geomean(array):
    gfactor = 1 + .01 * array
    product = gfactor.product()
    return product ** (1/len(array))


spy_mean = geomean(fang['SPY pct_chg'])
FANG_mean = geomean(fang['FANG pct_chg'])

growthfactor = 1 + .01 * fang['FANG pct_chg']

testresults = stats.ttest_1samp(growthfactor, spy_mean)


def hypothesis(pval, alpha):
    if pval <= alpha:
        print('Reject Null Hypothesis')
    else:
        print('Failed to Reject Null Hypothesis')


clevel = .05
pval = testresults.pvalue

seperator()

print(' ' * 50)
print('SPY gmean: ', spy_mean)
print('FANG gmean: ', FANG_mean)
print('p-value: ', pval)
print('Alpha: ', clevel)
print(' ' * 50)
hypothesis(pval, clevel)
