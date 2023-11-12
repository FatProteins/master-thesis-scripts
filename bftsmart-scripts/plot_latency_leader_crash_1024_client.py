import random
import re
import sys
from collections import defaultdict

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy
import numpy as np
import pandas as pd


def plot_performance(filename: str, ax=None):
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
            if len(split) != 5:
                continue
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
    indices = np.arange(80)
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
        shift_by = 10
        rdf = pd.DataFrame(index=indices[shift_by:] - shift_by, data=latency_array[shift_by:]) \
            # .rolling(1, center=True).mean()
        rdf_portion = rdf[0:]
        print(rdf_portion)
        rdf_ax = rdf_portion.plot(color='k')
        # rdf_ax.axvline(25, color='r', linestyle='--', zorder=1)
        # rdf_ax.text(26, 100, 'Follower Crash', color='r')
        # rdf_ax.axvline(35, color='r', linestyle='--')
        # rdf_ax.arrow(10, 300, 14, 133, width=1, color='k')
        return rdf_ax


filename = "../bftsmart-performance/leader-crash/1024-bftsmart_2023-11-11T10:49:54.282016992.csv"
# if len(sys.argv) != 2:
#     if fname not in globals():
#         raise ValueError(f"Unexpected number of program arguments: ${len(sys.argv)}")
#     else:
#         filename = fname
# else:
#     filename = sys.argv[1]


match = re.search("([0-9]+)-bftsmart.*", filename)
num_clients = int(match.group(1))
ax = plot_performance(filename)
# ax.annotate("Follower Crash", xy=(34, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
# ax.annotate("Follower Restart", xy=(44, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
# ax.axvline(25, color='r', linestyle='--', zorder=1)
# ax.text(18, 2050000, 'Leader\nCrash', color='r')
# ax.axvline(36, color='b', linestyle='--', zorder=1)
# ax.text(37, 2000000, 'Crashed Leader\nRejoins\nAs Follower', color='b')
# ax.axvline(27, color='darkorange', linestyle='--', zorder=1)
# ax.text(28, 2000000, 'New\nLeader\nElected', color='darkorange')

# ax.legend(['Performance'])
ax.legend().set_visible(False)
ax.set_xlabel('Seconds')
ax.set_ylabel('Latency [μs]')
ax.set_xticks(np.arange(0, 65, 5))
ax.set_yscale('symlog', base=10)
# ax.set_yticks(np.arange(0, 3000001, 200000))

# ax.set_xlim(0, ax.get_xlim()[1])
ax.set_xlim(0, 60)
ax.set_ylim(0, ax.get_ylim()[1])
# ax.ticklabel_format(style='plain')
# ax.get_yaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
# ax.set_ylim(0, ax.get_ylim()[1])
# plt.savefig(f"latency_leader_crash_{num_clients}_client_right.pdf", bbox_inches='tight', pad_inches=0.05)
plt.show()
plt.clf()
