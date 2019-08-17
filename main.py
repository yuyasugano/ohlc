#!/usr/bin/python
import csv
import time
import json
import requests
import numpy as np
import pandas as pd
from datetime import datetime

headers = {'Content-Type': 'application/json'}
api_url_base = 'https://public.bitbank.cc'
pair = 'btc_jpy'
period = '1min'

today = "{0:%Y%m%d}".format(datetime.today())

def api_ohlcv():
    api_url = '{0}/{1}/candlestick/{2}/{3}'.format(api_url_base, pair, period, today)
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        ohlcv = json.loads(response.content.decode('utf-8'))['data']['candlestick'][0]['ohlcv']
        return ohlcv
    else:
        return None

def main():
    ohlc = api_ohlcv()
    open, high, low, close, volume, timestamp = [],[],[],[],[],[]

    for i in ohlc:
        open.append(i[0])
        high.append(i[1])
        low.append(i[2])
        close.append(i[3])
        volume.append(i[4])
        time_str = str(i[5])
        timestamp.append(datetime.fromtimestamp(int(time_str[:10])).strftime('%Y/%m/%d %H:%M:%M'))

    date_time_index = pd.to_datetime(timestamp) # convert to DateTimeIndex type
    df = pd.DataFrame({'open': open, 'high': high, 'low': low, 'close': close}, index=date_time_index) # volume is not contained
    # adjustment for JST if required
    # df.index += pd.offsets.Hour(9)

    print(df.head(5))
    df.to_csv('ohlc.csv') # export as csv

if __name__ == '__main__':
    main()

