import pandas as pd
import re
# import json

class Roster:
    def __init__(self):
        self.roster = self.get_roster()

    def get_roster(self):
        r = pd.read_csv('data/roster.csv')
        r["employee"] = r["Email (UID)"].apply(lambda x: re.sub('@gsa.gov', '', x).lower())
        return r
