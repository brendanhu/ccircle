--- ACCOUNT ------------------------------------------------------------------

account.getBalance() -> Real Number

  Get the amount of money in your account

account.getShares(sym) -> Integer

  Get the number of shares of the given stock that you currently own

--- MARKET -------------------------------------------------------------------

market.buy(account, sym, quantity) -> None

  Buy 'quantity' shares of the stock with symbol 'sym' using 'account'
  You must have enough money in your account or the function will fail!

market.getPrice(sym) -> Real Number

  Return the current price of the given stock

market.getHistory(sym) -> List

  Return a list of historical prices for the given stock

market.getStockSymbols() -> List

  Return a list of all the stock symbols

market.sell(account, sym, quantity) -> None

  Sell 'quantity' shares of the stock with symbol 'sym' using 'account'
  You must have enough shares in your account or the function will fail!
