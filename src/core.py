from pytrends.request import TrendReq
import pandas as pd
import numpy as np
import warnings
import time
from datetime import datetime
from random import randint


class Gtrend(object):

    def __init__(self):
        pass

    def initialize(self, username, password, **kwargs):
        self.pytrend = TrendReq(google_username=username,google_password=password,
                                hl=kwargs.get('hl', 'en-US'))

    def get_weekly_trend(self, key_word, start_date, end_date, **kwargs):
        """Return weekly trend data of single keyword"""
        self.pytrend.build_payload(kw_list=[key_word],
                                   cat=kwargs.get('cat', 0),
                                   timeframe=start_date + ' ' + end_date,
                                   geo=kwargs.get('geo', '')
                                   )
        trend = self.pytrend.interest_over_time()
        assert (trend.index==pd.DatetimeIndex(start=start_date,end=end_date,freq='W')).all(), 'Non-weekly trend freq'
        return trend

    def get_daily_trend(self, key_word, start_date, end_date, **kwargs):
        """Return daily trend data of single keyword"""
        time_range = self.date_range(start_date, end_date, kwargs.get('gap', '240 days'))

        def _trend():
            for start,end in time_range:
                self.pytrend.build_payload(kw_list=[key_word],
                                           cat=kwargs.get('cat', 0),
                                           timeframe=start.strftime('%Y-%m-%d') + ' ' + end.strftime('%Y-%m-%d'),
                                           geo=kwargs.get('geo', '')
                                           )
                trend = self.pytrend.interest_over_time()
                assert (trend.index==pd.DatetimeIndex(start=start,end=end,freq='D')).all(), 'Non-daily trend freq.'
                yield trend

        return pd.concat([t for t in _trend()])

    def kwords_trend(self, kw_lst, start_date, end_date, freq, **kwargs):

        def _ktrend():
            for w in kw_lst:
                if freq=='D':
                    yield self.get_daily_trend(w, start_date, end_date, **kwargs)
                elif freq=='W':
                    yield self.get_weekly_trend(w, start_date, end_date, **kwargs)

        trend = pd.concat([t for t in _ktrend()], axis=1)
        trend['mean'] = trend.apply(np.mean, axis=1).round().apply(int)
        return trend


    @staticmethod
    def date_range(start_date, end_date, gap='240 days'):
        """

        :param start_date:
        :param end_date:
        :param gap: 240 d is daily threshold, 5 y is weekly threshold
        :return:
        """
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        dif = pd.Timedelta(gap)
        intv = np.ceil((end - start) / dif)
        prev = None
        for i in range(int(intv) + 1):
            now = (start + dif * i)
            if now > end:
                now = end
            if prev is not None:
                yield (prev, now)
            prev = now
            if i > 0:
                prev += pd.Timedelta('1 D')

    @staticmethod
    def geohelper(return_type='dataframe'):
        geocodes = pd.read_csv('aux_data/ISO 3166-1-alpha-2.csv')
        if return_type=='dataframe':
            return geocodes.set_index('Name')
        elif return_type=='dict':
            return geocodes.set_index('Name')['Code'].to_dict()
        else:
            warnings.warn('Non valid return_type: %s'%return_type)



gt = Gtrend()
gt.initialize(username='',password='')
d_trend = gt.get_daily_trend('loreal', '2014-01-01', '2016-12-24')
w_trend = gt.get_weekly_trend('loreal', '2011-10-24', '2016-12-24')

trend = gt.kwords_trend(kw_lst=['oreal','loreal','loreal paris'],
                        start_date='2014-01-01',
                        end_date='2016-12-24',
                        freq='W',
                        geo='US')




