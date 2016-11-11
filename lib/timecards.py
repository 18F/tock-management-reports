import os
import requests
import pandas as pd
import json
from lib.roster import Roster

class Timecards:
    def __init__(self, start_date):
        r = Roster().roster
        self.timecards = self.get_timecards(start_date)
        self.timecards = self.merge_roster(r)

    def get_timecards(self, start_date):
        headers = {'Authorization': 'Token ' + os.environ.get('TOCK_API_KEY')}
        url = 'https://tock.18f.gov/api/timecards.json?date=' + str(start_date)
        tock_data = requests.get(url, headers=headers).json()
        timecards = pd.read_json(json.dumps(tock_data))
        return timecards

    def merge_roster(self, roster):
        return self.timecards.merge(roster, left_on="user", right_on="employee", how="left")
