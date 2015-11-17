
from pyalgotrade import broker
from pyalgotrade.broker import backtesting

import common


class BacktestingBroker(backtesting.Broker):
    MIN_TRADE_USD = 5

    """A mercadoBitcoin backtesting broker.

    :param cash: The initial amount of cash.
    :type cash: int/float.
    :param barFeed: The bar feed that will provide the bars.
    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`
    :param fee: The fee percentage for each order. Defaults to 0.25%.
    :type fee: float.

    .. note::
        * Only limit orders are supported.
        * Orders are automatically set as **goodTillCanceled=True** and  **allOrNone=False**.
        * BUY_TO_COVER orders are mapped to BUY orders.
        * SELL_SHORT orders are mapped to SELL orders.
    """

    def __init__(self, cash, barFeed, fee=0.001):
        commission = backtesting.TradePercentage(fee)
        backtesting.Broker.__init__(self, cash, barFeed, commission)

    def getInstrumentTraits(self, instrument):
        return common.BTCTraits()

    def submitOrder(self, order):
        if order.isInitial():
            # Override user settings based on Bitfinex limitations.
            order.setAllOrNone(False)
            order.setGoodTillCanceled(True)
        return backtesting.Broker.submitOrder(self, order)

    def createMarketOrder(self, action, instrument, quantity, onClose=False):
        raise Exception("Market orders are not supported")

    def createLimitOrder(self, action, instrument, limitPrice, quantity):
        if instrument != common.btc_symbol:
            raise Exception("Only BTC instrument is supported")

        if action == broker.Order.Action.BUY_TO_COVER:
            action = broker.Order.Action.BUY
        elif action == broker.Order.Action.SELL_SHORT:
            action = broker.Order.Action.SELL

        if limitPrice * quantity < BacktestingBroker.MIN_TRADE_USD:
            raise Exception("Trade must be >= %s" % (BacktestingBroker.MIN_TRADE_USD))

        if action == broker.Order.Action.BUY:
            # Check that there is enough cash.
            fee = self.getCommission().calculate(None, limitPrice, quantity)
            cashRequired = limitPrice * quantity + fee
            if cashRequired > self.getCash(False):
                raise Exception("Not enough cash")
        elif action == broker.Order.Action.SELL:
            # Check that there are enough coins.
            if quantity > self.getShares(common.btc_symbol):
                raise Exception("Not enough %s" % (common.btc_symbol))
        else:
            raise Exception("Only BUY/SELL orders are supported")

        return backtesting.Broker.createLimitOrder(self, action, instrument, limitPrice, quantity)

    def createStopOrder(self, action, instrument, stopPrice, quantity):
        raise Exception("Stop orders are not supported")

    def createStopLimitOrder(self, action, instrument, stopPrice, limitPrice, quantity):
        raise Exception("Stop limit orders are not supported")


class PaperTradingBroker(BacktestingBroker):
    """A Mercado Bitcoin paper trading broker.

    :param cash: The initial amount of cash.
    :type cash: int/float.
    :param barFeed: The bar feed that will provide the bars.
    :type barFeed: :class:`pyalgotrade.barfeed.BarFeed`
    :param fee: The fee percentage for each order. Defaults to 0.5%.
    :type fee: float.

    .. note::
        * Only limit orders are supported.
        * Orders are automatically set as **goodTillCanceled=True** and  **allOrNone=False**.
        * BUY_TO_COVER orders are mapped to BUY orders.
        * SELL_SHORT orders are mapped to SELL orders.
    """

    pass
