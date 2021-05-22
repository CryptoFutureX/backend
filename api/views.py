import csv
from dateutil import tz
from datetime import datetime
import cryptocompare
import pandas as pd
from datetime import date
from django.http import JsonResponse
from pandas.core.tools.datetimes import to_datetime
from pandas.io.clipboards import to_clipboard


def speedometer(request):
    df = pd.read_csv('api/analysis/tweets_sentiments.csv')

    df = df.loc[df.date == '2021-05-19']
    # df = df.loc[df.date == date.today()]

    mean_pos_sen = df['pos_sentiment'].mean()
    mean_neg_sen = df['neg_sentiment'].mean()

    # print(mean_pos_sen, mean_neg_sen)

    if mean_pos_sen > mean_neg_sen:
        change = (mean_pos_sen - mean_neg_sen) * 100

    if mean_neg_sen > mean_pos_sen:
        change = (mean_pos_sen - mean_neg_sen) * 100

    return JsonResponse({'change': round(change, 3)}, safe=False)


def get_price_data(request):
    india_tz = tz.gettz('Asia/Kolkata')
    num = 7

    z = cryptocompare.get_historical_price_day(
        'BTC', 'USD', toTs=date.today(), limit=num)[:-1]

    for i in z:
        i['time'] = datetime.fromtimestamp(
            i['time']).strftime("%Y-%m-%d")

    return JsonResponse(z, safe=False)


def get_predicted_prices(request):
    df = pd.read_csv('api/analysis/predictions.csv')

    slope = df['prediction'][1] - df['prediction'][0]

    return JsonResponse({
        'x': date.today(),
        'y': [df['prediction'][1], df['prediction'][1],
              df['prediction'][1] + slope, df['prediction'][1]+slope]
    }, safe=False)
