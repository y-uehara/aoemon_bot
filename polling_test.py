#!/usr/bin/python3

from twython import Twython

import requests

consumer_key = 'XXXXX'
consumer_secret = 'XXXXX'
access_token = 'XXXXX'
access_token_secret = 'XXXXX'

my_screen_name = 'aoemon1'

twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)


if __name__ == "__main__":
#  stream = MyStreamer(consumer_key, consumer_secret, access_token, access_token_secret)
#  stream.user()
#  ret = twitter.verify_credentials()

  ret = twitter.get('direct_messages/events/list')
  print(ret)
