from lib.timecards import Timecards
import vcr

@vcr.use_cassette('fixtures/vcr_cassettes/timecards.yaml')
def test_create_timecard_object():
    timecards = Timecards("2016-10-23")
    assert len(timecards.timecards) == 1284
