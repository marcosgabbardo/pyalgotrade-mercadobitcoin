
import urllib2
import json


class MercadobitcoinError(Exception):
    def __init__(self, message, response):
        Exception.__init__(self, message)


def json_http_request(url):
    f = urllib2.urlopen(url)
    response = f.read()
    return json.loads(response)



def get_trades():
    url = "https://www.mercadobitcoin.net/api/trades/" #.format(currency_pair)
    #try:
    ret = json_http_request(url)
    #except:
    #    raise MercadobitcoinError('Problem fetching trades')

    #print(ret)
    return ret


def get_orderbook(currency_pair):
    url = "https://www.mercadobitcoin.net/api/orderbook/" #.format(currency_pair)
   # try:
    ret = json_http_request(url)
   # except:
   #     raise MercadobitcoinError('Problem fetching trades')
    return ret
