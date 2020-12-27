import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import strava_client

Z1 = (8, 7)
Z2 = (7, 16)
Z3 = (6, 29)
Z4 = (5, 36)
Z5 = (5, 7)
Z6 = (4, 46)

LABELS = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6']
COLORS = ['yellow', 'gray', 'blue', 'red', 'green', 'black']

def convert_min_per_km_to_m_per_s(minutes: int, seconds: int):
    """
    """
    total_seconds = minutes * 60 + seconds
    return 1000 / total_seconds


def convert_meters_per_second_to_min_per_km(mps: float):
    pass


def analyze_laps(laps: list, plot: bool = True):
    """
    Parameters:
    laps: list
        list of laps (average speed) of the last activity

    """
    
    if plot:
        g = sns.scatterplot(x=range(0, len(laps)), y=laps)
        for pace, label, color in zip([Z1,Z2,Z3,Z4,Z5,Z6], LABELS, COLORS):
            mps = convert_min_per_km_to_m_per_s(pace[0], pace[1])
            g.axhline(mps, label=label, c=color)

        plt.legend(LABELS)
        plt.show()


def main():
    laps_raw = strava_client.get_laps_of_last_run()
    # print(laps_raw)
    avg_speed = list()
    for l in laps_raw:
        # print(l)
        # print('*' * 100)
        avg_speed.append(float(l.get('average_speed')))
    analyze_laps(laps=avg_speed, plot=True)


if __name__ == '__main__':
    main()
