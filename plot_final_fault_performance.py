import os
import re
import sys
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy
import numpy as np
import pandas as pd


def plot_overlaps(filename: str, ax=None):
    if '1024' not in filename:
        return
    crash_end_seconds = 0
    latency_dict: defaultdict[int, list] = defaultdict(list)
    overlap_dict: defaultdict[str, list] = defaultdict(list)
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
                # print('Entry with error encountered')
                # continue
            overlap_dict['start_time'].append(start_timestamp / 1000 / 1000)
            overlap_dict['end_time'].append(end_timestamp / 1000 / 1000)
            latency = end_timestamp - start_timestamp
            latencies.append(latency)
            start_seconds = int(start_timestamp / 1000 / 1000 / 1000)
            end_seconds = int(end_timestamp / 1000 / 1000 / 1000)
            latency_dict[end_seconds].append(latency / 1000)  # microseconds
            end_times.append(end_seconds)
            if split[0] == 'crash':
                crash_end_seconds = end_seconds
            # end_times.append(datetime.datetime.fromtimestamp())  # from nanoseconds to seconds

    np.min(overlap_dict['start_time'])
    df = pd.DataFrame(data=overlap_dict)
    plt.hlines(np.ones(len(df)), df.start_time, df.end_time)
    plt.show()
    plt.clf()



def plot_latency(filename: str, ax=None):
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
                # print('Entry with error encountered')
                # continue
            latency = end_timestamp - start_timestamp
            latencies.append(latency)
            start_seconds = int(start_timestamp / 1000 / 1000 / 1000)
            end_seconds = int(end_timestamp / 1000 / 1000 / 1000)
            latency_dict[start_seconds].append(latency / 1000)  # microseconds
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
    # print(f'Crash at {crash_end_seconds - min_end_time} after start')

    # print(f'Mean latency: {mean_latency}')

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
        mean_latency = np.nanmean(latency_array[shift_by:shift_by + 60])
        print(f"{filename} with overall mean latency {mean_latency}")
        print(latency_array[shift_by:shift_by + 60])
        rdf = pd.DataFrame(index=indices[shift_by:] - shift_by, data=latency_array[shift_by:])
            # .rolling(1, center=True).mean()
        rdf_portion = rdf[0:61]
        # print(rdf_portion)
        rdf_ax = rdf_portion.plot(color='darkgreen', zorder=3, marker='*', clip_on=False)
        # rdf_ax.axvline(25, color='r', linestyle='--', zorder=1)
        # rdf_ax.text(26, 100, 'Follower Crash', color='r')
        # rdf_ax.axvline(35, color='r', linestyle='--')
        # rdf_ax.arrow(10, 300, 14, 133, width=1, color='k')
        return rdf_ax


def plot_throughput(filename: str, ax=None):
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
    # print(f'Crash at {crash_end_seconds - min_end_time} after start')
    np.sort(end_times)
    unique, counts = np.unique(end_times, return_counts=True)
    seconds = []
    second_counts = []
    for i in range(unique[-1] + 1):
        seconds.append(i)
        second_counts.append(0)

    for s, c in zip(unique, counts):
        second_counts[s] = c

    seconds = np.array(seconds)
    second_counts = np.array(second_counts)

    mean_latency = np.mean(latencies)
    # print(f'Mean latency: {mean_latency}')

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
        mean_throughput = np.nanmean(counts[shift_by:shift_by + 60])
        print(f"{filename} with overall mean throughput {mean_throughput}")
        rdf = pd.DataFrame(index=seconds[shift_by:] - shift_by, data=second_counts[shift_by:])
            # .rolling(1, center=True).mean()
        rdf_portion = rdf[0:61]
        # print(rdf_portion)
        rdf_ax = rdf_portion.plot(color='k', zorder=3, marker='d', clip_on=False)
        # rdf_ax.axvline(25, color='r', linestyle='--', zorder=1)
        # rdf_ax.text(26, 100, 'Follower Crash', color='r')
        # rdf_ax.axvline(35, color='r', linestyle='--')
        # rdf_ax.arrow(10, 300, 14, 133, width=1, color='k')
        return rdf_ax

    if ax is None:
        return df.plot()
    else:
        df.plot(ax=ax)


dirs = [
    './final-measurements/bftsmart-data/faults',
    './final-measurements/etcd-data/faults',
]

for fault_dir in dirs:
    for filename in os.listdir(fault_dir):
        match = re.search("([0-9]+)-(.)-(.)-(.+)_.*", filename)
        num_clients = int(match.group(1))
        node_match = match.group(2)
        fault_match = match.group(3)
        node = 'leader' if node_match == 'A' or node_match == 'L' else 'follower'
        fault_type = 'crash' if fault_match == 'C' else 'straggler'
        proto = match.group(4)

        # plot_overlaps(os.path.join(fault_dir, filename))

        ax = plot_latency(os.path.join(fault_dir, filename))
        # ax.annotate("Follower Crash", xy=(34, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
        # ax.annotate("Follower Restart", xy=(44, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
        ax.grid(True, zorder=1)
        ax.set_xlim(0, 60)
        ax.set_xticks(np.arange(0, 65, 5))
        ax.set_ylim(0, ax.get_ylim()[1])
        yticks = ax.get_yticks()
        ax.set_ylim(0, yticks[-1] + (yticks[-1] - yticks[-2]))
        if node == 'leader':
            if fault_type == 'crash':
                ax.axvline(25, color='r', linestyle='--', zorder=2, lw=2)
                ax.text(17, ax.get_ylim()[1]*0.9, 'Leader\nCrash', color='r')
                ax.axvline(35, color='b', linestyle='--', zorder=2, lw=2)
                ax.text(37, ax.get_ylim()[1]*0.9, 'Leader\nRestart', color='b')
            else:
                ax.axvline(25, color='m', linestyle='--', zorder=2, lw=2)
                ax.text(15, ax.get_ylim()[1]*0.85, 'Leader\nStarts\nStraggling', color='m')
                ax.axvline(40, color='c', linestyle='--', zorder=2, lw=2)
                ax.text(42, ax.get_ylim()[1]*0.85, 'Leader\nStops\nStraggling', color='c')
        else:
            if fault_type == 'crash':
                ax.axvline(25, color='r', linestyle='--', zorder=2, lw=2)
                ax.text(17, ax.get_ylim()[1]*0.9, 'Follower\nCrash', color='r')
                ax.axvline(35, color='b', linestyle='--', zorder=2, lw=2)
                ax.text(37, ax.get_ylim()[1]*0.9, 'Follower\nRestart', color='b')
            else:
                ax.axvline(25, color='m', linestyle='--', zorder=2, lw=2)
                ax.text(15, ax.get_ylim()[1]*0.85, 'Follower\nStarts\nStraggling', color='m')
                ax.axvline(40, color='c', linestyle='--', zorder=2, lw=2)
                ax.text(42, ax.get_ylim()[1]*0.85, 'Follower\nStops\nStraggling', color='c')

        # ax.legend(['Performance'])
        ax.legend().set_visible(False)
        ax.set_xlabel('Seconds')
        ax.set_ylabel('Latency [μs]')
        # ax.set_yticks(np.arange(0, ax.get_ylim()[1] + 500, 500))

        # ax.set_xlim(0, ax.get_xlim()[1])
        ax.ticklabel_format(style='plain')
        # ax.set_ylim(0, ax.get_ylim()[1])
        plt.savefig(f"final-thesis-figures/auto_generated/{proto}-{fault_type}-{node}-{num_clients}-latency.pdf",
                    bbox_inches='tight',
                    pad_inches=0.05)
        # plt.show()
        plt.clf()

        ax = plot_throughput(os.path.join(fault_dir, filename))
        # ax.annotate("Follower Crash", xy=(34, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
        # ax.annotate("Follower Restart", xy=(44, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
        ax.grid(True, zorder=1)
        ax.set_xticks(np.arange(0, 65, 5))
        ax.set_xlim(0, 60)
        ax.set_ylim(0, ax.get_ylim()[1])
        yticks = ax.get_yticks()
        ax.set_ylim(0, yticks[-1] + (yticks[-1] - yticks[-2]))
        if node == 'leader':
            if fault_type == 'crash':
                ax.axvline(25, color='r', linestyle='--', zorder=2, lw=2)
                ax.text(17, ax.get_ylim()[1]*0.9, 'Leader\nCrash', color='r')
                ax.axvline(35, color='b', linestyle='--', zorder=2, lw=2)
                ax.text(37, ax.get_ylim()[1]*0.9, 'Leader\nRestart', color='b')
            else:
                ax.axvline(25, color='m', linestyle='--', zorder=2, lw=2)
                ax.text(15, ax.get_ylim()[1]*0.85, 'Leader\nStarts\nStraggling', color='m')
                ax.axvline(40, color='c', linestyle='--', zorder=2, lw=2)
                ax.text(42, ax.get_ylim()[1]*0.85, 'Leader\nStops\nStraggling', color='c')
        else:
            if fault_type == 'crash':
                ax.axvline(25, color='r', linestyle='--', zorder=2, lw=2)
                ax.text(17, ax.get_ylim()[1]*0.9, 'Follower\nCrash', color='r')
                ax.axvline(35, color='b', linestyle='--', zorder=2, lw=2)
                ax.text(37, ax.get_ylim()[1]*0.9, 'Follower\nRestart', color='b')
            else:
                ax.axvline(25, color='m', linestyle='--', zorder=2, lw=2)
                ax.text(15, ax.get_ylim()[1]*0.85, 'Follower\nStarts\nStraggling', color='m')
                ax.axvline(40, color='c', linestyle='--', zorder=2, lw=2)
                ax.text(42, ax.get_ylim()[1]*0.85, 'Follower\nStops\nStraggling', color='c')

        # ax.legend(['Performance'])
        ax.legend().set_visible(False)
        ax.set_xlabel('Seconds')
        ax.set_ylabel('Throughput [req/s]')
        ax.ticklabel_format(style='plain')
        # ax.set_ylim(0, ax.get_ylim()[1])
        plt.savefig(f"final-thesis-figures/auto_generated/{proto}-{fault_type}-{node}-{num_clients}-throughput.pdf",
                    bbox_inches='tight',
                    pad_inches=0.05)
        # plt.show()
        plt.clf()
