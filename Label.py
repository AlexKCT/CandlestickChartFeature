
# import finlab_crypto
import talib
# from finlab_crypto.strategy import Filter
import pandas as pd

def RecordHigh(ohlcv):
    HighToday = ohlcv.high
    HighTomorrow = ohlcv.high.shift(-1).fillna(ohlcv.high)
    ohlcv.RecordHigh = HighTomorrow > HighToday
    return ohlcv.RecordHigh

def RecordLow(ohlcv):
    LowToday = ohlcv.low
    LowTomorrow = ohlcv.low.shift(-1).fillna(ohlcv.low)
    ohlcv.RecordLow = LowTomorrow < LowToday
    return ohlcv.RecordLow

def CloseMoveUp(ohlcv):
    CloseToday = ohlcv.close
    CloseTomorrow = ohlcv.close.shift(-1).fillna(ohlcv.close)
    ohlcv.CloseMoveUp = CloseTomorrow > CloseToday
    return ohlcv.CloseMoveUp

def ThreeBarrel(ohlcv, percentage=0.1,  period=8):
    # ohlcv.ThreeBarrel = ohlcv.high.shift(-period).rolling(period).max()
    ohlcv.ThreeBarrelUp = (lambda x, y: x*(1 + percentage) > y)(ohlcv.close, ohlcv.high.shift(-period).rolling(period).max())
    ohlcv.ThreeBarrelFall = (lambda x, y: x*(1 - percentage) < y)(ohlcv.close, ohlcv.low.shift(-period).rolling(period).min())
    ohlcv.ThreeBarrelCorrection = (lambda x, y: x*(1 + percentage) < y)(ohlcv.close, ohlcv.high.shift(-period).rolling(period).max()) & (lambda x, y: x*(1 - percentage) > y)(ohlcv.close, ohlcv.low.shift(-period).rolling(period).min())
    return ohlcv.ThreeBarrelUp, ohlcv.ThreeBarrelFall, ohlcv.ThreeBarrelCorrection



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
    # df.drop([len(df)-1],inplace=True) # 刪除最後一行用
    Up, Fall, Correction = ThreeBarrel(df)
    print (df.tail(10))
    print (type(ThreeBarrel(df)))
    print (Fall.tail(10))
