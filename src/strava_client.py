import requests
import argparse
import os
from datetime import datetime
import json
import requests
from pandas.io.json import json_normalize
import json
import csv

ACTIVITY_TYPE = 'Run'

TOKEN = os.getenv('STRAVA_TOKEN')


def auth(client_id, client_secret, code):
    # Make Strava auth API call with your 
    # client_code, client_secret and code
    print('making request: post https://www.strava.com/oauth/token client_id={} secret={} code={}'.format(client_id, client_secret, code))
    response = requests.post(
                        url = 'https://www.strava.com/oauth/token',
                        data = {
                                'client_id': client_id,
                                'client_secret': client_secret,
                                'code': code,
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
    if resp.status_code != 200:
        print('Error! status={} msg={} url={}'.format(resp.status_code, resp.text, resp.url))
        raise Exception(resp.text)
    r = resp.json()

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
 
    # create parser
    parser = argparse.ArgumentParser()
     
    # add arguments to the parser
    parser.add_argument("client_id")
    parser.add_argument("client_secret")
    parser.add_argument("code")
    args = parser.parse_args() 
    auth(args.client_id, args.client_secret, args.code)
