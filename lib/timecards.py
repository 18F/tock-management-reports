import os
import requests
import pandas as pd
import json

class Timecards:
    def __init__(self, start_date):
        self.timecards = self.get_timecards(start_date)

    def get_timecards(self, start_date):
        headers = {'Authorization': 'Token ' + os.environ.get('TOCK_API_KEY')}
        url = 'https://tock.18f.gov/api/timecards.json?date=' + str(start_date)
        tock_data = requests.get(url, headers=headers).json()
        timecards = pd.read_json(json.dumps(tock_data))
        return timecards
