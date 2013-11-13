# core
import hashlib
import hmac
import itertools
import pprint
import time

# 3rd party
from libsaas import http, parsers
from libsaas.services import base


# local
import user

def parse_text(body, code, headers):
    print "TEXT: {0}".format(body)

def nonce():
    return int(time.time())

def signature():
    n = nonce()
    message = "{0}{1}{2}".format(n, user.username, user.api_key)
    signature = hmac.new(user.api_secret,
                         msg=message,
                         digestmod=hashlib.sha256).hexdigest().upper()
    return signature, n



class Base(base.Resource):

    def get_url(self):
        return 'https://cex.io/api'

class CEX(base.RESTResource):

    def __init__(self):
        b = Base(None)
        base.RESTResource.__init__(self, b)

    def ticker(self):
        self.path = 'ticker/GHS/BTC'
        return super(CEX, self).get()

    def order_book(self):
        self.path = 'order_book/GHS/BTC'
        return super(CEX, self).get()

    def trade_history(self):
        self.path = 'trade_history/GHS/BTC'
        return super(CEX, self).get()

    @base.apimethod
    def balance(self):
        self.path = 'balance'
        sig, n = signature()
        params = dict(
            key=user.api_key,
            signature=sig,
            nonce=n)
        request = http.Request('POST', self.get_url(), params)
        #return request, parsers.parse_json
        return request, parse_text



if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    o = CEX()

    pp.pprint(o.ticker())
    #pp.pprint(o.order_book())
    #pp.pprint(o.balance())
    #pp.pprint(o.trade_history())
