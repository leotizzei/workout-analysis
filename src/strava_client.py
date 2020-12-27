import requests
import os
from datetime import datetime
import json
import requests
from pandas.io.json import json_normalize
import json
import csv

ACTIVITY_TYPE = 'Run'

TOKEN = os.getenv('STRAVA_TOKEN')


def auth():
    # Make Strava auth API call with your 
    # client_code, client_secret and code
    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': <>,
                                'client_secret': '<>',
                                'code': '<>',
                                'grant_type': 'authorization_code'
                                }
                    )#Save json response as a variable
    strava_tokens = response.json()# Save tokens to file
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(strava_tokens, outfile)# Open JSON file and print the file contents 
        # to check it's worked properly
    with open('strava_tokens.json') as check:
        data = json.load(check)
    print(data)


def get_laps_of_last_run() -> list:


    # Get the tokens from file to connect to Strava
    with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)# Loop through all activities
    url = "https://www.strava.com/api/v3/activities"
    access_token = strava_tokens['access_token']# Get first page of activities from Strava with all fields
    resp = requests.get(url + '?access_token=' + access_token)
    r = resp.json()
    print(r)
    runs = list()
    for a in r:
        activity_type = a.get('type')
        if activity_type == ACTIVITY_TYPE:
            start_date_str = a.get('start_date')
            act_id = a.get('id')
            runs.append( (act_id, start_date_str))
    sorted_runs = sorted(runs, key=lambda k: k[1])
    last_run = sorted_runs[-1]
    
    url = "https://www.strava.com/api/v3/activities/{}/laps".format(last_run[0])
    print(url)
    resp = requests.get(url + '?access_token=' + access_token)
    laps = resp.json()
    return laps




if __name__ == '__main__':
    before = int(datetime(2020,12,25,0,0).timestamp())
    # auth()
    get_activities(before=before)
