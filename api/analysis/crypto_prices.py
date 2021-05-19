# import cryptocompare
# import datetime

# def convertAnythingToString(x) :
#     y = f""""{x}"""
#     return y


# f = open("Output.txt", 'w')

# x = cryptocompare.get_coin_list(format=False)
# # print(x['BTC'])
# x = cryptocompare.get_price('BTC', currency='INR')
# # print(x)
# x = cryptocompare.get_historical_price(
#     'BTC', 'USD', datetime.datetime(2017, 6, 6))
# # print(x)
# x = cryptocompare.get_historical_price_day('BTC','USD')
# f.write(convertAnythingToString(x))


# f.close()

import os
import csv
import cryptocompare
from datetime import date
from datetime import datetime
from dateutil import tz
india_tz = tz.gettz('Asia/Kolkata')


def timeConversion(x):
    ts = int(x)
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


num = int(input())
BASE_PATH = './api/analysis'


with open(os.path.join(BASE_PATH, 'prices.csv'), 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['DateTime', 'Price Lag 0', 'Price Lag 1', 'Price Lag 2',
                    'Price Lag 3', 'Price Lag 4', 'Price Lag 5', 'Price Lag 6'])
    z = cryptocompare.get_historical_price_day(
        'BTC', 'USD', toTs=date.today(), limit=num)
    tempPriceArr = []
    x = -1

    for y in z[::-1]:
        tempPriceArr.append(y['close'])

    def priceLagCheckFunction(x, i):
        if x+i < num:
            return tempPriceArr[x+i]

    for y in z[::-1]:
        x += 1
        writer.writerow([timeConversion(y['time']), tempPriceArr[x], priceLagCheckFunction(x, 1), priceLagCheckFunction(
            x, 2), priceLagCheckFunction(x, 3), priceLagCheckFunction(x, 4), priceLagCheckFunction(x, 5), priceLagCheckFunction(x, 6)])


# with open('bitcoinPrices.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['DateTime', 'Open', 'High', 'Low', 'Close'])
#     z = cryptocompare.get_historical_price_day('BTC', 'USD', limit=30)

#     for y in z:
#         writer.writerow([timeConversion(y['time']), y['open'],
#                          y['high'], y['low'], y['close']])


# {'time': 1491350400, 'high': 1143.84, 'low': 1110.06, 'open': 1141.77, 'volumefrom': 69469.37,
#     'volumeto': 78335573.66, 'close': 1129.87, 'conversionType': 'direct', 'conversionSymbol': ''}
