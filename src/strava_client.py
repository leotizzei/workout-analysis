import requests
import argparse
import os
from datetime import datetime
import json
import requests
from pandas.io.json import json_normalize
import json
import csv
import time


ACTIVITY_TYPE = 'Run'

TOKEN = os.getenv('STRAVA_TOKEN')
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
STRAVA_CREDENTIALS_FILE = 'strava_tokens.json'
CODE = os.getenv("CODE")


class StravaClient:

    def __init__(self):
        self.headers = {"Content-type": "application/json"}
        # Get the tokens from file to connect to Strava
        with open(STRAVA_CREDENTIALS_FILE) as json_file:
            strava_tokens = json.load(json_file)  # Loop through all activities
        expires_at = strava_tokens.get('expires_at')
        if expires_at is None or time.time() > expires_at:
            print('Token has expired, will refresh')
            access_token = self.auth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, code=CODE)

        else:
            access_token = strava_tokens['access_token']  # Get first page of activities from Strava with all fields

        self.access_token = access_token
        self.headers["Authorization"] = "Bearer {}".format(access_token)

    @staticmethod
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
        if response.status_code in [200, 201]:
            strava_tokens = response.json()# Save tokens to file
            with open(STRAVA_CREDENTIALS_FILE, 'w') as outfile:
                json.dump(strava_tokens, outfile)# Open JSON file and print the file contents
                # to check it's worked properly
            with open(STRAVA_CREDENTIALS_FILE) as check:
                data = json.load(check)
            access_token = data.get("access_token")
            return access_token
        else:
            raise Exception("Unable to get access token: {}".format(response.text))

    @staticmethod
    def _refresh_token(refresh_token: str) -> str:
        """

        """
        "http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all,profile:read_all,activity:read_all"
        url = "https://www.strava.com/oauth/token"
        payload = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
        resp = requests.post(url=url, json=payload, headers={"Content-type": "application/json"})
        if resp.status_code in [200, 201]:
            new_strava_credentials = resp.json()
            with open(STRAVA_CREDENTIALS_FILE, "w+") as f:
                c = json.dumps(new_strava_credentials)
                f.write(c)
            access_token = new_strava_credentials.get("access_token")
            return access_token
        else:
            msg = "Error! url={}\npayload={}\nstatus={}\nmsg={}".format(resp.url, payload, resp.status_code, resp.text)
            print(msg)
            raise Exception(msg)

    def get_activities(self, activity_type: str = "Run", get_all: bool = True) -> list:

        # url = "https://www.strava.com/api/v3/activities"
        url = "https://www.strava.com/api/v3/athlete/activities"
        print("getting activities {}".format(url))
        status_code = 200
        i = 1
        activities = list()
        has_finished = False
        while status_code == 200 and has_finished is False:
            params = {"page": i}
            if get_all:
                i += 1
            else:
                has_finished = True
            # resp = requests.get(url=url + '?access_token=' + self.access_token, headers=self.headers)
            resp = requests.get(url=url, params=params, headers=self.headers)
            status_code = resp.status_code
            if resp.status_code != 200:
                msg = 'Error! status={}\nmsg={}\nurl={}\nheaders={}'.format(resp.status_code, resp.text, resp.url,
                                                                            self.headers)
                print(msg)
            else:
                aux = resp.json()
                if len(aux) == 0:
                    has_finished = True
                activities.extend(aux)
                print("i={} num_activities={}".format(i, len(activities)))
        return activities

    def get_activity_laps(self, activity_id: int) -> list:

        url = "https://www.strava.com/api/v3/activities/{}/laps".format(activity_id)
        print(url)
        resp = requests.get(url + '?access_token=' + self.access_token)
        laps = resp.json()
        return laps


# if __name__ == '__main__':
#
#     # create parser
#     parser = argparse.ArgumentParser()
#
#     # add arguments to the parser
#     parser.add_argument("client_id")
#     parser.add_argument("client_secret")
#     parser.add_argument("code")
#     args = parser.parse_args()
#     auth(args.client_id, args.client_secret, args.code)
