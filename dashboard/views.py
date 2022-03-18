from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from datetime import datetime
from datetime import date

data = {
    "date": "1/1/2020",
    "units_in_use": 0,
    "units_available": 0,
    "persons_quarantined": 0,
    "close_contacts": -1,
    "non_close_contacts": 0
}

centres = []


def bestcentres(request):
    API1 = requests.get("https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Foccupancy_of_quarantine_centres_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%7D").json()
    centres
    return render(request, 'first.html', {'centres': centres})

def days_between(d1,d2):
    d2 = datetime.strptime(d2, "%d/%m/%Y")
    return abs((d1 - d2).days)

def first(request):
    data_dict = {
        "resourse": 'http://www.chp.gov.hk/files/misc/occupancy_of_quarantine_centres_eng.csv',

        "section": 1,

        "format": "json",

        "filter": [
            [1, "eq", ["16/03/2022"]]
        ]
    }

    data_json = json.dumps(data_dict)
    API1 = requests.get("https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Foccupancy_of_quarantine_centres_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%7D").json()
    API2 = requests.get("https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fno_of_confines_by_types_in_quarantine_centres_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%7D").json()
    
    API1_useful = []

    for i in API1:
        if days_between(datetime.today(), i['As of date']) < 7:
            if data["date"] != i['As of date']:
                data["units_in_use"] = 0
                data["persons_quarantined"] = 0
                data["units_available"] = 0
                API1_useful = []
            data["date"] = i['As of date']
            data["units_in_use"] += i['Current unit in use']
            data["persons_quarantined"] += i['Current person in use']
            data["units_available"] += i['Ready to be used (unit)']
            API1_useful.append(i)

    for i in API2:
        if data["date"] == i['As of date']:
            data["non_close_contacts"] = i['Current number of non-close contacts']
            data["close_contacts"] = i['Current number of close contacts of confirmed cases']
    
    if data["non_close_contacts"] + data["close_contacts"] == data["persons_quarantined"]:
        data["count_consistent"] = True
    else:
        data["count_consistent"] = False

    ready_units = []
    
    for i in API1_useful:
        a = i['Ready to be used (unit)']
        ready_units.append(a)

    
    while (len(centres) < 3) and (len(ready_units) > 1):
        for i in API1_useful:
            if  i['Ready to be used (unit)'] == max(ready_units):
                centreinfo = {
                    "name": i['Quarantine centres'],
                    "units": i['Ready to be used (unit)']
                }
                ready_units.remove(i['Ready to be used (unit)'])
                centres.append(centreinfo)
                break
            

    return render(request, 'dashboard3.html', {'data': data, 'centres': centres})


def connected(request):
    return render(request, 'dashboard3.html', {'connected': True})

def has_data(request):
    if data["date"] != "1/1/2022":
        return render(request, 'dashboard3.html', {'has_data': True})

