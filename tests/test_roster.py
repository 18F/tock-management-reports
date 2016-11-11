from lib.roster import Roster

def test_create_roster_object():
    r = Roster()
    assert len(r.roster) == 193
    assert r.roster["employee"][146] == "aaron.snow"
