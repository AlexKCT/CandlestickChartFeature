
# import finlab_crypto
# import talib
# from finlab_crypto.strategy import Filter
import pandas as pd

def PositiveLine(ohlcv):
    ohlcv['PositiveLine'] = (lambda x, y: x > y)(ohlcv.close, ohlcv.open)
    return ohlcv.PositiveLine

def Barefoot(ohlcv):
    ohlcv['Barefoot'] = (lambda x, y: x == y)(ohlcv.close, ohlcv.low) | (lambda x, y: x == y)(ohlcv.open, ohlcv.low)
    return ohlcv.Barefoot

def Bald(ohlcv):
    ohlcv['Bald'] = (lambda x, y: x == y)(ohlcv.open, ohlcv.high) | (lambda x, y: x == y)(ohlcv.close, ohlcv.high)
    return ohlcv.Bald

def EntityHighLowRatio(ohlcv):
    ohlcv['EntityHighLowRatio'] = abs(ohlcv.close-ohlcv.open)/(ohlcv.high-ohlcv.low)
    ohlcv.fillna(0, inplace = True)
    return ohlcv.EntityHighLowRatio

def EntityPriceRatio(ohlcv):
    ohlcv['EntityPriceRatio'] = abs(ohlcv.close-ohlcv.open)/ohlcv.close
    ohlcv.fillna(0, inplace = True)
    return ohlcv.EntityPriceRatio


if __name__ == '__main__':
    df = pd.read_csv('test-data.csv', index_col='timestamp')
    print (df)
    print (type(EntityPriceRatio(df)))
    print (EntityPriceRatio(df))
