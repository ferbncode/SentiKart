import os
import tweepy 
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json


#Use your keys
consumer_key = 'Rbqi1HwrlKqf3AVfC4mEONZnv'
consumer_secret = 'CPx9hRTy3lbp0qrXnpEFo3h62T4uUZgr6UUER7Tx05ChlXkdmj' 
access_token = '4676147216-vOlNmlVSpkVCFaHS956CgGGVDZvsPD4EXGP6Msw'
access_secret = '88s1ezHTOzuIpfy9ZJ4HBqewoVCdfh6vR4pXJUagZ4j3l'

os.environ['http_proxy']='172.16.24.3:3128'
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

print(api.me().name)
