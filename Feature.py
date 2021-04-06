
# import finlab_crypto
# import talib
# from finlab_crypto.strategy import Filter
from os import replace
import pandas as pd
from pandas.core.indexes.base import Index
import talib
from talib import abstract


## talib指標(原則所有指標，使用預設參數)
def all_talib(ohlcv, ta_list = talib.get_functions()):
    # # 確認價量資料表 df 的值都是 float 格式
    ohlcv = ohlcv[['symbol','open','high','low','close','adj close','volume']].astype('float')
    for x in ta_list:
        try:
            # x 為技術指標的代碼，透過迴圈填入，再透過 eval 計算出 output
            output = eval('abstract.'+x+'(ohlcv)')
            # 如果輸出是一維資料，幫這個指標取名為 x 本身；多維資料則不需命名
            output.name = x.lower() if type(output) == pd.Series else None
            # 原始寫法已過期 
            # output.name = x.lower() if type(output) == pd.core.series.Series else None
            # 透過 merge 把輸出結果併入 df DataFrame
            ohlcv = pd.merge(ohlcv, pd.DataFrame(output), left_on = ohlcv.index, right_on = output.index)
            ohlcv.set_index('key_0', inplace=True)
        except:
            print(x+':Error')
    ohlcv.reset_index(inplace=True)
    ohlcv = ohlcv.rename(columns={'key_0':'date'})
    ohlcv.set_index('date', inplace=True)
    return ohlcv.iloc[:,7:]

## PositiveLine：是否陽線
def positive_line(ohlcv):
    ohlcv['positive_line'] = (lambda x, y: x > y)(ohlcv.close, ohlcv.open)
    return ohlcv.positive_line

## Barefoot：開盤或收盤於最低價
def barefoot(ohlcv):
    ohlcv['barefoot'] = (lambda x, y: x == y)(ohlcv.close, ohlcv.low) | (lambda x, y: x == y)(ohlcv.open, ohlcv.low)
    return ohlcv.barefoot

## Bald：開盤或收盤於最高價
def bald(ohlcv):
    ohlcv['bald'] = (lambda x, y: x == y)(ohlcv.open, ohlcv.high) | (lambda x, y: x == y)(ohlcv.close, ohlcv.high)
    return ohlcv.bald

## entity_difference_ratio：實體佔高低點的比例
def entity_difference_ratio(ohlcv):
    ohlcv['entity_difference_ratio'] = abs(ohlcv.close-ohlcv.open)/(ohlcv.high-ohlcv.low)
    return ohlcv.entity_difference_ratio

## EntityPriceRatio：實體與收盤價的比例
def entity_price_ratio(ohlcv):
    ohlcv['entity_price_ratio'] = abs(ohlcv.close-ohlcv.open)/ohlcv.close
    return ohlcv.entity_price_ratio


if __name__ == '__main__':
    data = pd.read_csv('test-data.csv', index_col='date')

    # tempdf = pd.merge(all_talib(data),positive_line(data),left_index = True,right_index = True,how = 'outer')

    tempdf = data.join(
        all_talib(data)).join(
            positive_line(data)).join(
                barefoot(data)).join(
                    bald(data)).join(
                        entity_difference_ratio(data)).join(
                            entity_price_ratio(data))
                            
    # tempdf = tempdf + positive_line(data)
    print(tempdf)
    # all_talib(df).to_csv('./abstract.csv')