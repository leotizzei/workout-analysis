import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

Z1 = (8, 7)
Z2 = (7, 16)
Z3 = (6, 29)
Z4 = (5, 36)
Z5 = (5, 7)
Z6 = (4, 46)

LABELS = ["avg_speed", 'Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6']
COLORS = ['yellow', 'gray', 'blue', 'red', 'green']


def convert_min_per_km_to_m_per_s(minutes: int, seconds: int):
    """
    """
    total_seconds = minutes * 60 + seconds
    return 1000 / total_seconds


def analyze_laps(laps: list, plot: bool = True):
    """
    Parameters:
    laps: list
        list of laps (average speed) of the last activity

    """
    y = [i.get("average_speed") for i in laps]
    x = list()
    dist = 0
    for lap in laps:
        dist += float(lap.get("distance"))
        x.append(dist)

    if plot:
        sns.set_theme()
        g = sns.lineplot(x=x, y=y, marker="o")
        for pace, label, color in zip([Z1,Z2,Z3,Z4,Z5,Z6], LABELS[1:], COLORS):
            mps = convert_min_per_km_to_m_per_s(pace[0], pace[1])
            g.axhline(mps, label=label, c=color)

        plt.legend(LABELS)
        plt.show()


def main():
    # laps_raw = strava_client.get_laps_of_last_run()
    # with open("laps.txt", "w+") as f:
    #     f.write(str(laps_raw))
    with open("laps.txt", "r") as f:
        laps = json.load(f)
    analyze_laps(laps=laps, plot=True)


if __name__ == '__main__':
    main()
