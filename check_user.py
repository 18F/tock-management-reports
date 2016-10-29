import pandas as pd
import requests
import os
import json

def get_timecards(start_date, user_name):
    headers = {'Authorization': 'Token ' + os.environ.get('TOCK_API_KEY')}
    url = 'https://tock.18f.gov/api/timecards.json?date=' + str(start_date) + '&user=' + user_name
    tock_data = requests.get(url, headers=headers).json()
    timecards = pd.read_json(json.dumps(tock_data))
    return timecards

if __name__ == "__main__":

    from tabulate import tabulate
    import sys
    import pdb

    start_date = sys.argv[1]
    user_name = sys.argv[2].lower().replace('@gsa.gov','')

    timecards = get_timecards(start_date, user_name)

    ### Print underlying data
    print(tabulate(timecards[["hours_spent", "project_name", "notes", "billable"]].sort_values(by='billable'), tablefmt="psql"))

    ### Get Utilization
    ooo = timecards[timecards["project_name"].str.contains("Out of Office")].hours_spent.sum()
    billable = timecards[timecards["billable"] == True].hours_spent.sum()
    print("Out of Office: %s" % ooo)
    print("Billable: %s" % billable)
    print("Over 70 percent: %s" % ((billable/(40-ooo)>.7)))
