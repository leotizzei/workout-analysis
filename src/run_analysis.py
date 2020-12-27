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


def convert_min_per_km_to_m_per_s(minutes: int, seconds: int):
    """
    """
    total_seconds = minutes * 60 + seconds
    return 1000 / total_seconds


def convert_m_per_s_to_min_per_km(mps: float):
    pass


def analyze_laps(laps: list, plot: boolean = True):
    mps = convert_min_per_km_to_m_per_s(minutes=z[0], seconds=z[1])
    g.axhline(mps, label=label, c=c)
    
    if plot:    
        plt.legend(labels)
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
