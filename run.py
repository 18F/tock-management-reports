import pandas as pd
import requests
import json
import os
import warnings
warnings.filterwarnings('ignore')
import re
import pdb

def get_timecards(start_date):
    headers = {'Authorization': 'Token ' + os.environ.get('TOCK_API_KEY')}
    url = 'https://tock.18f.gov/api/timecards.json?date=' + str(start_date)
    tock_data = requests.get(url, headers=headers).json()
    timecards = pd.read_json(json.dumps(tock_data))
    return timecards

def remove_gsa_gov(email):
    return re.sub('@gsa.gov', '', email).lower()

def remove_non_billable_projects(project_name):
    if ("TTS Acq" in project_name) or ("PIF" in project_name) or ("Federalist" in project_name):
        return True
    else:
        return False

def get_roster(timecards):
    employees = pd.read_csv('data/roster.csv')
    employees["employee"] = employees["Email (UID)"].apply(remove_gsa_gov)
    employees["inTimeCards"] = employees["employee"].apply(lambda x: x in timecards.user.values)
    # roster = employees[employees["inTimeCards"] == True]
    return employees

def get_employee_unit(employee, roster):
    result = roster.loc[roster["employee"] == employee, "Team (Chapter/BU)"]
    if len(result) > 0:
        return result.values[0]
    else:
        return "N/A"

def check_understaffed(user, roster):
    row = roster.loc[roster["employee"] == user.user.values[0]]
    if len(row) > 0:
        unit = row["Team (Chapter/BU)"].values
        billable_status = row["Updated Billable Category"].values
        billed_hours = user[user["billable"]].hours_spent.sum()
        ooo = user[user["project_name"].str.contains("Out of Office")].hours_spent.sum()
        if len(unit) > 0 and len(billable_status) > 0:
            if billable_status[0] == "Primary" and billed_hours < 28:
                return pd.Series({"user":user.user.values[0], "category": "Primary", "unit":unit[0], "hours": billed_hours, "delta": 32 - billed_hours, "ooo": ooo, "understaffed": ((ooo+billed_hours)/40 < .7)})
            elif len(row) > 0 and billable_status[0] == "Partial" and billed_hours < 12:
                return pd.Series({"user":user.user.values[0], "category": "Partial", "unit":unit[0], "hours": billed_hours, "delta": 12 - billed_hours, "ooo": ooo, "understaffed": ((ooo+billed_hours)/40 < .2)})
    return pd.Series({"user": None, "category": None, "unit": None, "hours": None, "delta": None, "ooo": None, "understaffed": None})

def normalize_hours(row):
    try:
        if row["hours"] == 0:
            return pd.Series({"unit": row["unit"], "normalized": 0, "target_hours": row["hours"], "hours_spent": row["hours_spent"]})
        normalized = str(round(float(row["hours_spent"])/float(row["hours"]),2))
        return pd.Series({"unit": row["unit"], "normalized": normalized, "target_hours": row["hours"], "hours_spent": row["hours_spent"]})
    except:
        return None

if __name__ == "__main__":
    from tabulate import tabulate
    import sys

    start_date = sys.argv[1]

    timecards = get_timecards(start_date)
    roster = get_roster(timecards)
    timecards["unit"] = timecards["user"].apply(lambda x: get_employee_unit(x, roster))
    timecards["18FPL"] = ~timecards["project_name"].apply(lambda x: remove_non_billable_projects(x))

    billable_cards = timecards[(timecards["billable"] == True)]

    targets = pd.read_csv("data/targets.csv")
    print ("TOTAL NUMBER OF 18F PL BILLABLE HOURS: %s" % (billable_cards.groupby(["18FPL"]).agg({"hours_spent":sum})))

    truants = roster[~roster["employee"].isin(timecards.user)]
    truants = truants[truants["Status"] == "Current"]
    truants_result = truants["Email (UID)"].tolist()

    print("TRUANTS (%s):\n%s\n%s" % (
        len(truants_result),
        tabulate(truants.groupby('Team (Chapter/BU)').agg({'employee':'count'})),
        tabulate(truants[['Team (Chapter/BU)','employee']].sort('Team (Chapter/BU)'))
    ))

    res = billable_cards.groupby(["18FPL","unit"], as_index=False).agg({"hours_spent":sum}).merge(targets, on="unit")

    print(tabulate(res[res["18FPL"] == True].apply(lambda x: normalize_hours(x), axis=1), tablefmt="psql", headers="keys"))

    understaffed = timecards.groupby(["user"]).apply(lambda x: check_understaffed(x, roster))

    print("UNDERSTAFFING:\n")
    print("Total Delta: %s" % understaffed.delta.sum())
    print(tabulate(understaffed.dropna().sort(['unit','understaffed','delta']), tablefmt="psql", headers="keys"))

    print(tabulate(understaffed.groupby('unit').agg({'delta':sum}), tablefmt="psql", headers="keys"))

    ooo_hours = timecards[timecards["project_name"].str.contains("Out of Office")]
    real_hours = ooo_hours[ooo_hours["hours_spent"] > 0]

    print("Total Number of Out Of Office Hours: %s" % real_hours.hours_spent.sum())

    # pdb.set_trace()
