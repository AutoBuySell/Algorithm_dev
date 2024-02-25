import numpy as np
import traceback

from .assets import Equity_Manual_v2

def getNewPosition_Manual_v2(asset: Equity_Manual_v2, test_end_point: int = 0) -> tuple[bool]:
    '''
    asset: asset object
    test_end_point: set to 0 for real-time judging, or set as a number larger than 0 for testing
    '''

    try:
        data_np = np.array(asset.data['o'])

        # For testing, use sliced data
        if test_end_point != 0:
            data_np = data_np[:test_end_point + 1]

        # The last point is the moment of judging
        current_price = data_np[-1]

    except:
        print(traceback.format_exc())