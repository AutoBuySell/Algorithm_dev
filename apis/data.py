import requests
import os
import traceback
from dotenv import load_dotenv

load_dotenv(verbose=True)

dataServerUrl = os.getenv('DATA_SERVER_URL')

headers = {
    'accept': 'application/json',
}

def req_data_historical(symbol: str, timeframe: str, startDate: str, endDate: str) -> None:
    '''
    Request to data server to update historical data
    '''

    try:
        response = requests.post(
            url=dataServerUrl + '/dataArchiving/historical',
            headers=headers,
            json={
                'symbol': symbol,
                'timeframe': timeframe,
                'startDate': startDate,
                'endDate': endDate
            }
        )

        assert response.status_code == 201, response.message

    except:
        print(traceback.format_exc())
