import pprint

from libsaas.services import base

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


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    o = CEX()

    pp.pprint(o.ticker())
    pp.pprint(o.order_book())
