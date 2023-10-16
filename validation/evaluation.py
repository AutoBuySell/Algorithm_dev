from manual_algorithms.dkqp_231016.assets import Equity_Manual_v1
from manual_algorithms.dkqp_231016.judge import getNewPosition_Manual_v1
from manual_algorithms.dkqp_231016.order import makeOrders_Manual_v1

from validation.visualization import visualize_points

SYMBOLS_FOR_EVALUATION = ['TSLA', 'AAPL', 'META', 'NVDA', 'NFLX', 'ROKU']

def trading_point_evaluation():
  results = {}

  for symbol in SYMBOLS_FOR_EVALUATION:
    asset = Equity_Manual_v1(symbol)
    results[symbol] = []
    data = asset.data['o']
    for i in range(1, len(data)):
      buySig, sellSig = getNewPosition_Manual_v1(asset, i)
      if buySig:
        results[symbol].append(('buy', i, data[i]))
      if sellSig:
        results[symbol].append(('sell', i, data[i]))

    visualize_points(asset, results[symbol])

  return results