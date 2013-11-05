from libsaas.services import base

class Base(base.Resource):

    def get_url(self):
        return 'https://cex.io/api'

class CEX(base.RESTResource):

    def __init__(self):
        b = Base(None)
        base.RESTResource.__init__(self, b)

    def ticker(self):
        self.path = 'ticker/GHC/BTC'
        return super(CEX, self).get()


if __name__ == '__main__':
    o = CEX()
    print o.ticker()
