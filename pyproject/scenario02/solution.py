""" Your solution goes in this file! """


class StockTrader:
    def __init__(self):
        # Set variables if you want
        pass

    def getDifficulty(self):
        """ Controls how difficult the simulation is:
               0.0 -> easiest
               0.5 -> moderate
               1.0 -> hardest
        """
        return 0.0

    def getPauseTime(self):
        """ Controls how fast the simulation runs; 0 = fastest """
        return 0.1

    def getSeed(self):
        """ Use different numbers to get different random variations of the simulation """
        return 1337

    def trade(self, account, market):
        """ Analyze the market for the current day and make trades as you see fit. Try to make as much money as you can!

            This is a very basic and bad starter strategy: get a list of stocks, buy any stock that is less than $10
            (if we can afford it); sell any stock that is more than $20 (if we own it). You must do better than this!
        """
        syms = market.getStockSymbols()
        for sym in syms:
            price = market.getPrice(sym)
            if price < 10 and account.getBalance() >= price:
                market.buy(account, sym, 1)
            if price > 10 and account.getShares(sym) > 0:
                market.sell(account, sym, 1)
