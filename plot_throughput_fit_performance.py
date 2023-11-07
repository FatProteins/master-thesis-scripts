import random
import re
import sys

import matplotlib.pyplot as plt
import numpy
import numpy as np
import pandas as pd


def plot_performance(filename: str, ax=None, color=None):
    crash_end_seconds = 0
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
            if success != 'true':
                # print('Entry with error encountered')
                continue
            latencies.append(end_timestamp - start_timestamp)
            end_seconds = int(end_timestamp / 1000 / 1000 / 1000)
            end_times.append(end_seconds)
            if split[0] == 'crash':
                crash_end_seconds = end_seconds
            # end_times.append(datetime.datetime.fromtimestamp())  # from nanoseconds to seconds

    min_end_time = np.min(end_times)
    end_times = np.subtract(end_times, min_end_time)
    print(f'Crash at {crash_end_seconds - min_end_time} after start')
    np.sort(end_times)
    unique, counts = np.unique(end_times, return_counts=True)
    second_counts = dict(zip(unique, counts))
    for i in range(unique[-1]):
        if i not in second_counts:
            second_counts[i] = 0

    rolling_window = np.convolve(counts[5:70], np.ones(1) / 1, 'valid')
    mean_latency = np.mean(latencies)
    print(f'Mean latency: {mean_latency}')

    # df = pd.DataFrame(np.ones(len(end_times)), index=end_times)
    df = pd.DataFrame(rolling_window)
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
        rdf = pd.DataFrame(index=unique[shift_by:end_shift] - (shift_by + shift_by // 2),
                           data=counts[shift_by:end_shift]) \
            .rolling(15, center=True).mean()
        rdf_portion = rdf[0:]
        print(f'Throughput full mean: {np.mean(counts[shift_by:end_shift])}')
        # print(rdf_portion)
        if ax is not None:
            rdf_ax = rdf_portion.plot(color=color, ax=ax)
        else:
            rdf_ax = rdf_portion.plot(color=color)
        # rdf_ax.axvline(25, color='r', linestyle='--', zorder=1)
        # rdf_ax.text(26, 100, 'Follower Crash', color='r')
        # rdf_ax.axvline(35, color='r', linestyle='--')
        # rdf_ax.arrow(10, 300, 14, 133, width=1, color='k')
        return rdf_ax


filename = "fit-measurement/with_fit/4096-kv_pairs_2023-11-06T21-11-39.csv"
# if len(sys.argv) != 2:
#     if fname not in globals():
#         raise ValueError(f"Unexpected number of program arguments: ${len(sys.argv)}")
#     else:
#         filename = fname
# else:
#     filename = sys.argv[1]


match = re.search("([0-9]+)-kv_pairs.*", filename)
num_clients = int(match.group(1))
ax = plot_performance("fit-measurement/without_fit/4096-kv_pairs_2023-11-06T20-30-22.csv", ax=None, color='royalblue')
plot_performance("fit-measurement/autonomous_mode/4096-kv_pairs_2023-11-06T21-48-07.csv", ax, 'orange')
plot_performance(filename, ax, 'k')
# ax.annotate("Follower Crash", xy=(34, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
# ax.annotate("Follower Restart", xy=(44, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
# ax.axvline(25, ymax=0.8, color='r', linestyle='--', zorder=1)
# ax.text(18, 20000, 'Leader\nCrash', color='r')
# ax.axvline(36, ymax=0.78, color='b', linestyle='--', zorder=1)
# ax.text(37, 18000, 'Crashed Leader\nRejoins\nAs Follower', color='b')
# ax.axvline(27, ymin=0.02, ymax=1.0, color='darkorange', linestyle='--', zorder=1)
# ax.text(28, 58000, 'New\nLeader\nElected', color='darkorange')
# ax.annotate('', xy=(31.5, 5100), xytext=(38, 5100), arrowprops={'width': 1, 'headwidth': 6, 'color': 'darkorange'}, color='darkorange', fontsize='large')


ax.legend(['Standalone', 'FIT Autonomous Mode', 'FIT Orchestrated Mode'], loc='lower right')
# ax.legend().set_visible(False)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Throughput [req/s]')
ax.set_xticks(np.arange(0, 65, 5))
ax.set_yticks(np.arange(0, 60001, 10000))
title = f'Throughput for {num_clients} Concurrent Client Requests'
if num_clients == 1:
    title = f'Throughput for Sequential Client Requests'

# ax.set_title(title)
# ax.set_xlim(0, ax.get_xlim()[1])
ax.set_xlim(0, 60)
# ax.set_ylim(0, ax.get_ylim()[1])
ax.set_ylim(0, ax.get_ylim()[1])
ax.grid(True)
plt.savefig(f"throughput_fit_performance.pdf", bbox_inches='tight', pad_inches=0.05)
plt.show()
plt.clf()
