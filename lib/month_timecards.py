from lib.timecards import Timecards
from datetime import date, timedelta
import pandas as pd
import pdb

class MonthTimecards:
    def __init__(self, year, month):
        self.sundays = [sunday for sunday in self.get_sundays_in_month(year, month)]

    def get_timecards_in_month(self):
        """ get the timecards in the month from the sundays array"""
        week_cards = pd.DataFrame()
        for sunday in self.sundays:
            week_cards = week_cards.append(Timecards(str(sunday)).timecards)
        return week_cards

    @classmethod
    def get_sundays_in_month(cls, year, month):
        '''get all of the Sundays in the month'''
        first_day = date(year, month, 1)
        sunday = first_day + timedelta(days=(6-first_day.weekday()) % 6)

        while 1:
            if sunday.month != month:
                break
            yield sunday.isoformat()
            sunday += timedelta(days=7)
