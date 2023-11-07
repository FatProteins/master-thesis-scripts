import random
import re
import sys
from collections import defaultdict

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy
import numpy as np
import pandas as pd


def plot_performance(filename: str, ax=None, color=None):
    crash_end_seconds = 0
    latency_dict: defaultdict[int, list] = defaultdict(list)
    with open(filename, "r") as file:
        latencies = []
        end_times = []
        # Skip header
        file.readline()
        for line in file:
            if len(line) < 3:
                continue

            split = line.strip().split(',')
            start_timestamp = int(split[3])
            end_timestamp = int(split[4])
            success = split[2]
            # if success != 'true':
            #     print('Entry with error encountered')
            #     continue
            latency = end_timestamp - start_timestamp
            latencies.append(latency)
            start_seconds = int(start_timestamp / 1000 / 1000 / 1000)
            latency_dict[start_seconds].append(latency / 1000)  # microseconds
            end_seconds = int(end_timestamp / 1000 / 1000 / 1000)
            end_times.append(end_seconds)
            if split[0] == 'crash':
                crash_end_seconds = end_seconds
            # end_times.append(datetime.datetime.fromtimestamp())  # from nanoseconds to seconds

    latency_array = []
    indices = np.arange(90)
    min_start = np.min(list(latency_dict.keys()))
    for i in indices:
        if len(latency_dict[i + min_start]) == 0:
            latency_array.append(np.NaN)  # microseconds
        else:
            latency_array.append(int(np.mean(latency_dict[i + min_start])))

    latency_array = np.array(latency_array)

    min_end_time = np.min(end_times)
    print(f'Crash at {crash_end_seconds - min_end_time} after start')

    mean_latency = np.mean(latencies)
    print(f'Mean latency: {mean_latency}')

    # df = pd.DataFrame(np.ones(len(end_times)), index=end_times)
    # df = df.rolling(window="1S").sum()
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.precision', 3,
                           ):
        numpy.set_printoptions(threshold=sys.maxsize)
        # print(end_times)
        # print(second_counts)
        shift_by = 15
        end_shift = shift_by + 75
        rdf = pd.DataFrame(index=indices[shift_by:end_shift] - (shift_by + shift_by // 2),
                           data=latency_array[shift_by:end_shift]) \
            .rolling(15, center=True).mean()
        rdf_portion = rdf[0:]
        print(rdf_portion)
        if ax is not None:
            rdf_ax = rdf_portion.plot(color=color, ax=ax)
        else:
            rdf_ax = rdf_portion.plot(color=color)

        # rdf_ax.axvline(25, color='r', linestyle='--', zorder=1)
        # rdf_ax.text(26, 100, 'Follower Crash', color='r')
        # rdf_ax.axvline(35, color='r', linestyle='--')
        # rdf_ax.arrow(10, 300, 14, 133, width=1, color='k')
        return rdf_ax


# if len(sys.argv) != 2:
#     if fname not in globals():
#         raise ValueError(f"Unexpected number of program arguments: ${len(sys.argv)}")
#     else:
#         filename = fname
# else:
#     filename = sys.argv[1]


ax = plot_performance("fit-measurement/without_fit/1-kv_pairs_2023-11-06T20-23-22.csv", ax=None, color='royalblue')
plot_performance("fit-measurement/autonomous_mode/1-kv_pairs_2023-11-06T21-50-19.csv", ax, 'orange')
plot_performance("fit-measurement/with_fit/1-kv_pairs_2023-11-07T00-46-26.csv", ax, 'k')
# ax.annotate("Follower Crash", xy=(34, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
# ax.annotate("Follower Restart", xy=(44, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
# ax.axvline(25, ymin=0.33, color='r', linestyle='--', zorder=1)
# ax.text(18, 2050000, 'Leader\nCrash', color='r')
# ax.axvline(36, ymin=0.04, color='b', linestyle='--', zorder=1)
# ax.text(37, 2000000, 'Crashed Leader\nRejoins\nAs Follower', color='b')
# ax.axvline(27, ymin=0.24, color='darkorange', linestyle='--', zorder=1)
# ax.text(28, 2000000, 'New\nLeader\nElected', color='darkorange')

# ax.legend(['Performance'])
ax.legend(['Standalone', 'FIT Autonomous Mode', 'FIT Orchestrated Mode'], loc='lower right')
# ax.legend().set_visible(False)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Latency [μs]')
ax.set_xticks(np.arange(0, 65, 5))
# ax.set_yticks(np.arange(0, 80001, 10000))
ax.grid(True)

# ax.set_xlim(0, ax.get_xlim()[1])
ax.set_xlim(0, 60)
# ax.set_ylim(0, ax.get_ylim()[1])
ax.ticklabel_format(style='plain')
# ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
# ax.set_ylim(0, ax.get_ylim()[1])
plt.savefig("latency_fit_performance_1_client.pdf", bbox_inches='tight', pad_inches=0.05)
plt.show()
plt.clf()
