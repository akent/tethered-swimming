from oauth.oauth import OAuthRequest, OAuthSignatureMethod_HMAC_SHA1
from hashlib import md5
import pprint
import json, time
import random, math, re, urllib, urllib2


STREAM_URL = "https://userstream.twitter.com/2/user.json"
CONSUMER_KEY = 'xxx'
CONSUMER_SECRET = 'xxx'
ACCESS_TOKEN = 'xxx'
ACCESS_TOKEN_SECRET = 'xxx'

class Token(object):
    def __init__(self,key,secret):
        self.key = key
        self.secret = secret

    def _generate_nonce(self):
        random_number = ''.join(str(random.randint(0, 9)) for i in range(40))
        m = md5(str(time.time()) + str(random_number))
        return m.hexdigest()

access_token = Token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
consumer = Token(CONSUMER_KEY,CONSUMER_SECRET)

parameters = {
    'oauth_consumer_key': CONSUMER_KEY,
    'oauth_token': access_token.key,
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_timestamp': str(int(time.time())),
    'oauth_nonce': access_token._generate_nonce(),
    'oauth_version': '1.0',
}


oauth_request = OAuthRequest.from_token_and_callback(access_token,
                http_url=STREAM_URL,
                parameters=parameters)
signature_method = OAuthSignatureMethod_HMAC_SHA1()
signature = signature_method.build_signature(oauth_request, consumer, access_token)

parameters['oauth_signature'] = signature

data = urllib.urlencode(parameters)

req = urllib2.urlopen("%s?%s" % (STREAM_URL,data))
buffer = ''


# We're using urllib2 to avoid external dependencies
# even though pyCurl actually handles the callbacks
# much more gracefully than this clumsy method.
# We read a byte at a time until we find a newline
# which indicates the end of a chunk.

import parse

while True:

    chunk = req.read(1)
    if not chunk:
        print buffer
        break

    chunk = unicode(chunk)
    buffer += chunk

    tweets = buffer.split("\n",1)
    if len(tweets) > 1:
        try:
            parse.print_tweet(tweets[0])
        except Exception as e:
            print tweets[0]
        buffer = tweets[1]
