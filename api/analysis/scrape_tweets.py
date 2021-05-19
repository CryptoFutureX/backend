import twint
import pandas
import datetime


def scrape_tweets():
    c = twint.Config()
    c.Search = 'Bitcoin'
    c.Min_likes = 5
    c.Since = str(datetime.datetime.now() - datetime.timedelta(days=4))[:-7]
    c.Min_retweets = 5
    c.Min_replies = 2
    c.Hide_output = True
    c.Store_csv = True
    c.Output = './tweets.csv'

    twint.run.Search(c)


scrape_tweets()
