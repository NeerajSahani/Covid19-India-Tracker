import pandas as pd


def get_day_wise(country='india'):
    return pd.read_json('https://api.covid19api.com/total/dayone/country/{0}/status/confirmed'.format(country))
