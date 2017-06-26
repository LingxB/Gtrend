#!/usr/bin/python3
# coding: utf-8

# MUST install tweepy library: 'easy_install tweepy'
# MUST mkdir 'data/' for output directory
# Tracking keywords defined in line 23, more about rules: https://dev.twitter.com/streaming/overview/request-parameters#track
# More tweepy: http://docs.tweepy.org/en/v3.5.0/index.html
# token, key, secrets here: https://apps.twitter.com/


from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
import time
import json


access_token = '742286224229052416-VQn5AHRI94X3BfMFKZQWZ8AJxdecCBG'
access_token_secret = 'bPagRzh7rY8A6WzH2EkC516qBEy9LcpoLqks6OwXpBQqT'
consumer_key = 'RaRrJTiRGRh524J6f7CtNiShB'
consumer_secret = 'CDJfleMBz8vDWCwgpVrWyBs9bDm4o2EWD629qi4gkWub70WQmb'


keyword = ['costacoffee'] # including eveything contains 'costacoffee' eg. @CostaCoffee, #costacoffee, costaCoffee...
lang = None # Target language eg. 'en'
wdir = 'data/' # Output Directory
fname = 'twitter_streamdata_' # Outputfile name eg. fname+keyword.jason


class MyListener(StreamListener):
    
    def on_data(self, data):
        try:
            with open(wdir+fname+'_'.join(keyword)+'.json','a') as f:
                f.write(data)
                print(json.loads(data)['created_at'], json.loads(data)['text'])
                return True
        except BaseException as e:
            print('Error on_data: %s' %str(e))
            time.sleep(5)
            return True
    
    def on_error(self, status):
        print('Error: %s' %status)
        print('Pausing 15m to avoid Twitter Rate Limits...')
        time.sleep(15.1*60)
        return True
    

if __name__ == '__main__':

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    twitter_stream = Stream(auth, MyListener())
    print('Running, waiting for tweets...')
    twitter_stream.filter(track=keyword,languages=lang)
    






