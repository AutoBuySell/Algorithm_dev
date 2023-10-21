from manual_algorithms.dkqp_231016.assets import Equity_Manual_v1 as ASSETCLASS
from manual_algorithms.dkqp_231016.judge import getNewPosition_Manual_v1 as JUDGEFUNC
from manual_algorithms.dkqp_231016.order import makeOrders_Manual_v1 as ORDERFUNC

from apis.data import req_data_historical

from validation.visualization import visualize_points

SYMBOLS_FOR_EVALUATION = ['TSLA', 'AAPL', 'META', 'NVDA', 'NFLX', 'ROKU', 'NKLA']

def trading_point_evaluation(startDate: str, endDate: str, timeframe: str = '30Min'):
  '''
  매수/매도 포인트 시각화
  visualize buying/selling points

  모델 예측 포인트, 지정 포인트, 매칭 포인트 리턴
  return: A dict of keys of symbols and values of (total_predicted_points, total_selected_points, matched_points).
  predicted_points: points predicted by the model
  selected_points: points selected by human
  '''

  req_data_historical(
    symbols=SYMBOLS_FOR_EVALUATION,
    timeframe=timeframe,
    startDate=startDate,
    endDate=endDate
  )

  results = {}

  checked_selected_points = {}
  predicted_points = {}

  for symbol in SYMBOLS_FOR_EVALUATION:
    asset = ASSETCLASS(symbol, timeframe)

    checked_selected_points[symbol] = set([])
    predicted_points[symbol] = []

    data = asset.data[asset.data['t'] >= startDate][asset.data['t'] <= endDate]['o']

    judges = asset.data['judge']
    for i in data.index:
      buySig, sellSig = JUDGEFUNC(asset, i)
      if buySig:
        for j in range(i - 2, i + 3):
          if j not in checked_selected_points[symbol] and judges[j] == 1:
            checked_selected_points[symbol].add(j)
            break
        predicted_points[symbol].append(('buy', i, data[i]))
      elif sellSig:
        for j in range(i - 2, i + 3):
          if j not in checked_selected_points[symbol] and judges[j] == -1:
            checked_selected_points[symbol].add(j)
            break
        predicted_points[symbol].append(('sell', i, data[i]))

    results[symbol] = (
      len(predicted_points[symbol]),
      len(judges[judges != 0]),
      len(checked_selected_points[symbol])
    )

    visualize_points(asset, predicted_points[symbol])

  return results

def trading_margin_evaluation(startDate: str, endDate: str, timeframe: str = '30Min'):
  '''
  매수/매도 포인트 시각화
  visualize buying/selling points

  종목별 예상 수익 반환 (최종 데이터 시점)
  return: A dict of keys of symbols and values of (estimated margins, current_buy_power, current_position_value)
  '''

  req_data_historical(
    symbols=SYMBOLS_FOR_EVALUATION,
    timeframe=timeframe,
    startDate=startDate,
    endDate=endDate
  )

  predicted_points = {}
  estimated_margins = {}

  for symbol in SYMBOLS_FOR_EVALUATION:
    asset = ASSETCLASS(symbol, timeframe)
    estimated_margins[symbol] = (asset.buy_power, 0, 0)

    ordered = set([])
    predicted_points[symbol] = []

    data = asset.data[asset.data['t'] >= startDate][asset.data['t'] <= endDate]['o']

    for i in data.index:
      buySig, sellSig = JUDGEFUNC(asset, i)
      currentPrice = data[i]
      if buySig:
        isOrder, qty = ORDERFUNC(asset=asset, side='buy', currentPrice=currentPrice)
        if isOrder:
          asset.buy_power += qty * currentPrice
          asset.current_position -= qty
          ordered.add(i)
        predicted_points[symbol].append(('buy', i, currentPrice))
      elif sellSig:
        isOrder, qty = ORDERFUNC(asset=asset, side='sell', currentPrice=currentPrice)
        if isOrder:
          asset.buy_power -= qty * currentPrice
          asset.current_position += qty
          ordered.add(i)
        predicted_points[symbol].append(('sell', i, currentPrice))

    estimated_margins[symbol] = (
      asset.buy_power + asset.current_position * data[i] - estimated_margins[symbol][0],
      asset.buy_power,
      asset.current_position * data[i]
    )

    visualize_points(asset, predicted_points[symbol], ordered)

  return estimated_margins