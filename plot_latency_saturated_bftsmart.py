import os
import re
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import ticker


def avg_throughput(filename: str):
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
            # print('Entry with error encountered')
            # continue
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
    indices = np.arange(14)
    min_start = np.min(list(latency_dict.keys()))
    for i in indices:
        if len(latency_dict[i + min_start]) == 0:
            latency_array.append(0)  # microseconds
        else:
            latency_array.append(int(np.mean(latency_dict[i + min_start])))

    latency_array = np.array(latency_array)

    shift_by = 10
    print(filename)
    mean_latency = np.mean(latency_array[shift_by:shift_by+60])
    stddev_latency = np.std(latency_array[shift_by:shift_by+60])
    # print(latency_array[shift_by:-shift_by])
    # print(f"Mean latency: {mean_latency}")
    # print()
    return mean_latency, stddev_latency


dirname = "./final-measurements/bftsmart-data/saturation"

files = [
    '1-bftsmart_2023-11-11T12:05:48.085445421.csv',
    '2-bftsmart_2023-11-11T12:07:42.384087078.csv',
    '4-bftsmart_2023-11-11T12:09:36.734609910.csv',
    '8-bftsmart_2023-11-11T12:11:31.152302325.csv',
    '16-bftsmart_2023-11-11T12:13:25.558831711.csv',
    '32-bftsmart_2023-11-11T12:15:20.146565544.csv',
    '64-bftsmart_2023-11-11T12:17:14.775572774.csv',
    '128-bftsmart_2023-11-11T12:19:09.523212838.csv',
    '256-bftsmart_2023-11-11T12:21:04.421154592.csv',
    '512-bftsmart_2023-11-11T12:22:58.943155216.csv',
    # '640-X-X-bftsmart_2023-11-12T03:28:24.780210469.csv',
    '768-X-X-bftsmart_2023-11-12T03:30:25.476540055.csv',
    # '896-X-X-bftsmart_2023-11-12T03:32:26.305658703.csv',
    '1024-bftsmart_2023-11-11T12:24:57.606276800.csv',
    # '1152-X-X-bftsmart_2023-11-12T03:34:30.086754261.csv',
    '1280-X-X-bftsmart_2023-11-12T03:36:36.348887690.csv',
    # '1408-X-X-bftsmart_2023-11-12T03:38:45.051205156.csv',
    '1536-X-X-bftsmart_2023-11-12T03:40:54.816173342.csv',
    # '1664-X-X-bftsmart_2023-11-12T03:43:09.266926423.csv',
    # '1792-X-X-bftsmart_2023-11-12T03:45:23.397717774.csv',
    # '1920-X-X-bftsmart_2023-11-12T03:47:38.670898080.csv',
    '2048-bftsmart_2023-11-11T12:27:04.751887064.csv',
    '4096-bftsmart_2023-11-11T12:29:23.744032952.csv',
    # '8192-bftsmart_2023-11-11T12:32:33.758968421.csv',
]
indices = []
data = []
stddev = []
for filename in files:
    match = re.search("([0-9]+)-(X-X-)?bftsmart.*", filename)
    num_clients = int(match.group(1))
    mean_latency, stddev_latency = avg_throughput(os.path.join(dirname, filename))
    indices.append(num_clients)
    data.append(mean_latency)
    stddev.append(stddev_latency)
    print(mean_latency, stddev_latency)
# ax.annotate("Follower Crash", xy=(34, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
# ax.annotate("Follower Restart", xy=(44, 10000), xytext=(5, 250), arrowprops={'width': 1.5, 'headwidth': 10, 'color': 'r'}, color='r', fontsize='large')
# ax.axvline(25, ymax=0.86, color='r', linestyle='--', zorder=1)
# ax.text(17, 300, 'Follower\nCrash', color='r')
# ax.axvline(36, ymax=0.84, color='b', linestyle='--', zorder=1)
# ax.text(38, 285, 'Follower\nRejoins\nCluster', color='b')

# ax.legend(['Performance'])
df = pd.DataFrame(index=indices, data=data)
print(indices)
print(data)
ax = df.plot(linestyle='none', marker='*', color='darkgreen', clip_on=False, zorder=10, yerr=stddev, capsize=4)
ax.legend().set_visible(False)
ax.grid(True)
ax.set_xlabel('Concurrent Clients')
ax.set_ylabel('Latency [μs]')
idx = np.argmax(data)
print(f"{idx} {indices[idx]} {data[idx]}")
ax.set_xscale('log', base=2)
ax.set_yscale('symlog', base=10)
# ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:g}'.format(x)))
# ax.set_yticks(np.arange(0, 801, 100))
title = f'Throughput for {num_clients} Concurrent Client Requests'
if num_clients == 1:
    title = f'Throughput for Sequential Client Requests'

ax.set_xticks([2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 6, 2 ** 8, 2 ** 10, 2 ** 12])
yticks = [0]
yticks.extend([10 ** i for i in range(1, 8)])
ax.set_yticks(yticks)
ax.set_ylim(0, 10 ** 7)
# ax.set_title(title)
# ax.set_xlim(0, ax.get_xlim()[1])
# ax.set_xlim(0, 2**18)
# ax.set_ylim(0, 2**22)
# ax.set_ylim(0, ax.get_ylim()[1])
plt.savefig(f"final-thesis-figures/latency_concurrency_saturation_bftsmart.pdf", bbox_inches='tight', pad_inches=0.05)
plt.show()
plt.clf()
