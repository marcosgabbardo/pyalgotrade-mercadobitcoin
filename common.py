
import pyalgotrade.logger
from pyalgotrade import broker


btc_symbol = "btcbrl"
logger = pyalgotrade.logger.getLogger("mercadobitcoin")


class BTCTraits(broker.InstrumentTraits):
    def roundQuantity(self, quantity):
        return round(quantity, 8)
