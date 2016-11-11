from lib.timecards import Timecards
from lib.roster import Roster
import vcr

@vcr.use_cassette('fixtures/vcr_cassettes/timecards.yaml')
def test_create_timecard_object():
    timecards = Timecards("2016-10-23")
    assert len(timecards.timecards) == 1284

@vcr.use_cassette('fixtures/vcr_cassettes/timecards.yaml')
def test_merge_roster():
    timecards = Timecards("2016-10-23")
    r = Roster().roster
    output = timecards.merge_roster(r)
    assert output["employee"][0] == r["employee"][158]
    assert output["Updated Billable Category"][0] == "Primary"
