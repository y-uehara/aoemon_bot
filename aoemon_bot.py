#!/usr/bin/python3

import requests
import time
import json
import datetime
from requests_oauthlib import OAuth1Session

consumer_key = "XXXXX"
consumer_secret = "XXXXX"
access_token = "XXXXX"
access_token_secret = "XXXXX"

my_screen_name = "XXXXX"
log_path = "XXXXX"

class MyBot:
  def __init__(self):
    self.twitter = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)
    self.pollingTime = 70
    self.headers = {"content-type": "application/json"}
    
    self.log_fp = open(log_path, mode="a")
    
  def __del__(self):
    self.log_fp.close()

  def receive_dm(self):
    url = "https://api.twitter.com/1.1/direct_messages/events/list.json"
    ret_json = self.twitter.get(url, headers = self.headers)
    return json.loads(ret_json.text)

  def send_dm(self, target, msg_text):
    url = "https://api.twitter.com/1.1/direct_messages/events/new.json"
    param = {"event": {"type": "message_create", "message_create": {"target": {"recipient_id": target}, "message_data": {"text": msg_text}}}}
    self.twitter.post(url, headers = self.headers, data = json.dumps(param))

  def get_user_screen_name(self, user_id):
    url = "https://api.twitter.com/1.1/users/show.json?user_id=" + user_id
    ret_json = self.twitter.get(url, headers = self.headers)
    return (json.loads(ret_json.text))["screen_name"]

  def run(self):
    # get timestamp of last message
    ret = self.receive_dm()
    last_timestamp = max(i["created_timestamp"] for i in ret["events"])
  
    self.log("last timestamp: " + last_timestamp)
    while True:
      messages = ret["events"]
      new_messages = [m for m in messages if m["created_timestamp"] > last_timestamp]
      new_messages.sort(key=(lambda x: x["created_timestamp"]))
      for m in new_messages:
        sender_name = self.get_user_screen_name(m["message_create"]["sender_id"])
        msg_text = m["message_create"]["message_data"]["text"]
        self.log("timestamp :" + m["created_timestamp"] + m["message_create"]["message_data"]["text"] + " from " + sender_name)
        if sender_name != my_screen_name:
          ret_msg = self.dispatch(msg_text)
          self.send_dm(m["message_create"]["sender_id"], ret_msg)
        last_timestamp = m["created_timestamp"]
      time.sleep(self.pollingTime)
      ret = self.receive_dm()

  def dispatch(self, cmd_text):
    self.log("dispatch: " + cmd_text)
    if cmd_text == "exit":
      exit()
    elif cmd_text.startswith("echo "):
      return cmd_text[5:]
    elif cmd_text == "ip":
      return requests.get("http://inet-ip.info/ip").text
      
  def log(self, log_msg):
    log_str = "{0:[%m/%d %H:%M.%S]} ".format(datetime.datetime.now()) + log_msg + "\n"
    print(log_str)
    self.log_fp.write(log_str)
      
if __name__ == "__main__":
  bot = MyBot()
  bot.run()

