#!/usr/bin/env python3

import datetime
import json
import hmac
import hashlib
import os
import requests
import time

def current_time_in_millis():
  return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp() * 1000)

def as_bytes(s):
  return bytes(s.encode())

class Client(object):
  def __init__(self, key, secret):
    self.key      = key
    self.secret   = secret
    self.base_url = "https://api.bitvavo.com"
    self.version  = "v2"
 
  def _create_signature(self, timestamp,  method, resource, body=""):
    payload   = str(timestamp) + method + "/{}/".format(self.version) + resource + body
    signature = hmac.new(
                  self.secret.encode("utf-8"), 
                  payload.encode("utf-8"), 
                  hashlib.sha256).hexdigest() 

    return signature
  
  def _do_get_request(self, resource, is_private=False):
    headers = {}
    url     = "%s/%s/%s" % (self.base_url, self.version, resource)
    
    if is_private:
      time      = current_time_in_millis()
      signature = self._create_signature(time, "GET", resource)
      headers   = {
        "Bitvavo-Access-Key": self.key,
        "Bitvavo-Access-Signature": signature,
        "Bitvavo-Access-Timestamp": str(time)
      }

    r = requests.get(url, headers=headers)

    return r.content
    
  def get_balance(self):
    get_request = self._do_get_request("balance", is_private=True)

    return get_request

  def get_time(self):
    get_request = self._do_get_request("time")

    return get_request

def main():
  # fetch api keys from Bitvavo and set as environment variable
  key    = os.environ["BITVAVOKEY"]
  secret = os.environ["BITVAVOSECRET"]

  client = Client(key, secret)
  
main()
