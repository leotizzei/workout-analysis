
from strava_client import StravaClient
from db_conn import ActivityConn, Activity, Lap, LapConn
from datetime import datetime


def _make_activity(data):
    start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%dT%H:%M:%SZ").date()
    start_date_local = datetime.strptime(
        data.get("start_date_local"), "%Y-%m-%dT%H:%M:%SZ").date()
    a = Activity(strava_activity_id=data.get("id"),
                 distance = data.get("distance"),
                 moving_time = data.get("moving_time"),
                 elapsed_time = data.get("elapsed_time"),
                 total_elevation_gain = data.get("total_elevation_gain"),
                 activity_type = data.get("type"),
                 start_date = start_date,
                 start_date_local = start_date_local,
                 timezone = data.get("timezone"),
                 utc_offset = data.get("utf_offset"),
                 average_speed = data.get("average_speed"),
                 max_speed = data.get("max_speed"),
                 has_heartrate = data.get("has_heartrate"),
                 workout_type = data.get("workout_type"))
    return a


def _make_lap(data, activity_id):
    start_date = datetime.strptime(data.get("start_date"), "%Y-%m-%dT%H:%M:%SZ").date()
    start_date_local = datetime.strptime(
        data.get("start_date_local"), "%Y-%m-%dT%H:%M:%SZ").date()
    lap = Lap(

        activity_id = activity_id,
        name = data.get("name"),
        elapsed_time = data.get("elapsed_time"),
        moving_time = data.get("moving_time"),
        start_date = start_date,
        start_date_local = start_date_local,
        distance = data.get("distance"),
        start_index = data.get("start_index"),
        end_index = data.get("end_index"),
        total_elevation_gain = data.get("total_elevation_gain"),
        average_speed = data.get("average_speed"),
        max_speed = data.get("max_speed"),
        average_cadence = data.get("average_cadence"),
        average_watts = data.get("average_watts"),
        lap_index =data.get("lap_index"),
        split = data.get("split"))
    return lap


def store_data_into_db(get_all: bool = False):
    """

    """
    client = StravaClient()
    activity_conn = ActivityConn()
    lap_conn = LapConn()
    activities = client.get_activities(get_all=get_all)
    for act_raw in activities:
        activity = _make_activity(act_raw)
        activity_id = activity_conn.insert_activity(activity)
        assert activity_id is not None, "Error"
        if activity_id > 0:
            strava_activity_id = act_raw.get("id")
            laps_raw = client.get_activity_laps(activity_id=strava_activity_id)
            for lap_raw in laps_raw:
                print(lap_raw)
                lap = _make_lap(lap_raw, activity_id)
                lap_conn.insert_lap(lap)


if __name__ == "__main__":
    store_data_into_db(get_all=False)