import pandas as pd
from datetime import date
from django.http import JsonResponse


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
