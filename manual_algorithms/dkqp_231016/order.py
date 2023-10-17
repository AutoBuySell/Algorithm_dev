def makeOrders_Manual_v1(asset, side, price):
  '''
  orders: (list of symbols to order, list of 'buy' or 'sell' orders per asset)
  obj_assets: dict of asset objects
  '''

  ordered = False

  symbol = asset.symbol

  buy_power = asset.buy_power
  current_position = asset.current_position

  if side == 'sell' and current_position > 0:
    qty = int(current_position / 3) if current_position >= 3 else current_position
    asset.buy_power += qty * price
    asset.current_position -= qty
    if qty > 0:
      ordered = True

    # print('sell: ', symbol, ', qty: ', qty, ', price: ', price)
  elif side == 'buy' and buy_power > 0:
    qty = int(buy_power / 3 / price)
    asset.buy_power -= qty * price
    asset.current_position += qty
    if qty > 0:
      ordered = True

    # print('buy: ', symbol, ', qty: ', qty, ', price: ', price)

  return ordered
