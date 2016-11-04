from lib.month_timecards import MonthTimecards
import vcr

def test_get_sundays_in_month():
    year = 2016
    month = 10
    sundays = [sunday for sunday in MonthTimecards.get_sundays_in_month(year,month)]
    assert len(sundays) == 5

def test_create_month_timecards():
    october_month_timecards = MonthTimecards(2016,10)
    assert october_month_timecards.sundays == ['2016-10-02', '2016-10-09', '2016-10-16', '2016-10-23', '2016-10-30']

@vcr.use_cassette('fixtures/vcr_cassettes/timecards.yaml', record_mode='new_episodes')
def test_get_timecards_in_month():
    year = 2016
    month = 10
    october_month_timecards = MonthTimecards(2016,10).get_timecards_in_month()
    assert len(october_month_timecards) == 5242
