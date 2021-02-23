import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json
import strava_client
from configparser import ConfigParser
from db_conn import ActivityConn, LapConn
import matplotlib

SECTION = "PACEZONE"
CONFIG_INI = "config.ini"


def convert_min_per_km_to_m_per_s(minutes: int, seconds: int):
    """
    """
    total_seconds = minutes * 60 + seconds
    return 1000 / total_seconds


def analyze_laps(zones: list, plot: bool = True):
    """
    Parameters:
    laps: list
        list of laps (average speed) of the last activity

    """
    activity_conn = ActivityConn()
    activities = activity_conn.query_activity()
    sorted_activities = sorted(activities, key=lambda a: a.start_date)
    last_activity = sorted_activities[-1]
    lap_conn = LapConn()
    laps = lap_conn.query_laps(activity_id=last_activity.id)
    y = [i.average_speed for i in laps]
    x = list()
    dist = 0
    for lap in laps:
        dist += float(lap.distance)
        x.append(dist)

    if plot:
        sns.set_theme()
        g = sns.lineplot(x=x, y=y, marker="o")
        labels = ["avg_speed"]
        mps_list = list()
        for zone in zones:
            pace = zone.get("pace")  # type: tuple
            label = zone.get("name")
            labels.append(label)
            mps = convert_min_per_km_to_m_per_s(pace[0], pace[1])
            mps_list.append(mps)
        
        cmap = matplotlib.cm.seismic
        nsteps = len(mps_list)
        for i in range(1, len(mps_list)):
            prev = mps_list[i-1]
            cur = mps_list[i]

            plt.axhspan(prev, cur, color=cmap(i / float(nsteps)), alpha=0.5)
        plt.legend(labels)
        plt.show()


def parse_paces():
    filename = CONFIG_INI

    parser = ConfigParser()
    parser.read(filename)
    zones = list()
    for zone in ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6" ]:

        option_min = "{}_MIN".format(zone)
        minute = int(parser.get(section=SECTION, option=option_min))
        option_sec = "{}_SEC".format(zone)
        sec = int(parser.get(section=SECTION, option=option_sec))
        p = (minute, sec)
        zones.append({"pace": p, "name": zone})
    return zones


def main():
    zones = parse_paces()
    analyze_laps(zones=zones)


if __name__ == '__main__':
    main()
