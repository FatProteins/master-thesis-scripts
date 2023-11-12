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
            start_timestamp = int(split[3])
            end_timestamp = int(split[4])
            success = split[2]
            if success != 'true':
                # print('Entry with error encountered')
                continue
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
            latency_array.append(0)  # microseconds
        else:
            latency_array.append(int(np.mean(latency_dict[i + min_start])))

    latency_array = np.array(latency_array)

    shift_by = 10
    print(filename)
    mean_latency = np.mean(latency_array[shift_by:shift_by+60])
    stddev_latency = np.std(latency_array[shift_by:shift_by+60])
    print(latency_array[shift_by:-shift_by])
    print(f"Mean latency: {mean_latency}")
    print()
    return mean_latency, stddev_latency


dirname = "./saturated-data/third_saturation_measurement"
# if len(sys.argv) != 2:
#     if fname not in globals():
#         raise ValueError(f"Unexpected number of program arguments: ${len(sys.argv)}")
#     else:
#         filename = fname
# else:
#     filename = sys.argv[1]

files = [
    '1-kv_pairs_2023-11-06T01-49-24.csv',
    '2-kv_pairs_2023-11-06T01-49-38.csv',
    '3-kv_pairs_2023-11-06T01-49-52.csv',
    '4-kv_pairs_2023-11-06T01-50-06.csv',
    '5-kv_pairs_2023-11-06T01-50-20.csv',
    '10-kv_pairs_2023-11-06T01-50-34.csv',
    '20-kv_pairs_2023-11-06T01-50-48.csv',
    '30-kv_pairs_2023-11-06T01-51-02.csv',
    '40-kv_pairs_2023-11-06T01-51-16.csv',
    '50-kv_pairs_2023-11-06T01-51-30.csv',
    '100-kv_pairs_2023-11-06T01-51-44.csv',
    '400-kv_pairs_2023-11-06T01-51-58.csv',
    '700-kv_pairs_2023-11-06T01-52-12.csv',
    '1000-kv_pairs_2023-11-06T01-52-26.csv',
    '2000-kv_pairs_2023-11-06T01-52-40.csv',
    '3000-kv_pairs_2023-11-06T01-52-54.csv',
    '4000-kv_pairs_2023-11-06T01-53-08.csv',
    '5000-kv_pairs_2023-11-06T01-53-22.csv',
    '6000-kv_pairs_2023-11-06T01-53-36.csv',
    '7000-kv_pairs_2023-11-06T01-53-50.csv',
]
doubled_files = [
    '1-kv_pairs_2023-11-06T02-44-36.csv',
    '2-kv_pairs_2023-11-06T02-44-50.csv',
    '4-kv_pairs_2023-11-06T02-45-04.csv',
    '8-kv_pairs_2023-11-06T02-45-18.csv',
    '16-kv_pairs_2023-11-06T02-45-32.csv',
    '32-kv_pairs_2023-11-06T02-45-46.csv',
    '64-kv_pairs_2023-11-06T02-46-00.csv',
    '128-kv_pairs_2023-11-06T02-46-14.csv',
    '256-kv_pairs_2023-11-06T02-46-28.csv',
    '512-kv_pairs_2023-11-06T02-46-42.csv',
    '1024-kv_pairs_2023-11-06T02-46-56.csv',
    '2048-kv_pairs_2023-11-06T02-47-10.csv',
    '4096-kv_pairs_2023-11-06T02-47-24.csv',
    '8192-kv_pairs_2023-11-06T02-47-38.csv',
    '16384-kv_pairs_2023-11-06T02-47-52.csv',
    '32768-kv_pairs_2023-11-06T02-48-06.csv',
    '65536-kv_pairs_2023-11-06T02-48-20.csv',
]
third_files = [
    '1-kv_pairs_2023-11-06T02-57-33.csv',
    '2-kv_pairs_2023-11-06T02-57-47.csv',
    '4-kv_pairs_2023-11-06T02-58-01.csv',
    '8-kv_pairs_2023-11-06T02-58-15.csv',
    '16-kv_pairs_2023-11-06T02-58-29.csv',
    '32-kv_pairs_2023-11-06T02-58-43.csv',
    '64-kv_pairs_2023-11-06T02-58-57.csv',
    '128-kv_pairs_2023-11-06T02-59-11.csv',
    '256-kv_pairs_2023-11-06T02-59-25.csv',
    '512-kv_pairs_2023-11-06T02-59-39.csv',
    '1024-kv_pairs_2023-11-06T02-59-53.csv',
    '2048-kv_pairs_2023-11-06T03-00-07.csv',
    '4096-kv_pairs_2023-11-06T03-00-21.csv',
    '8192-kv_pairs_2023-11-06T03-00-35.csv',
    '16384-kv_pairs_2023-11-06T03-00-49.csv',
    '32768-kv_pairs_2023-11-06T03-01-03.csv',
    '65536-kv_pairs_2023-11-06T03-01-17.csv',
    '131072-kv_pairs_2023-11-06T03-01-31.csv',
    # '262144-kv_pairs_2023-11-06T03-01-45.csv',
    # '524288-kv_pairs_2023-11-06T03-02-00.csv',
    # '1048576-kv_pairs_2023-11-06T03-02-15.csv',
]
new_files = [
    '1-kv_pairs_2023-11-11T13-56-12.csv',
    '2-kv_pairs_2023-11-11T13-58-08.csv',
    '4-kv_pairs_2023-11-11T14-00-03.csv',
    '8-kv_pairs_2023-11-11T14-01-59.csv',
    '16-kv_pairs_2023-11-11T14-03-55.csv',
    '32-kv_pairs_2023-11-11T14-05-50.csv',
    '64-kv_pairs_2023-11-11T14-07-46.csv',
    '128-kv_pairs_2023-11-11T14-09-43.csv',
    '256-kv_pairs_2023-11-11T14-11-39.csv',
    '512-kv_pairs_2023-11-11T14-13-35.csv',
    '1024-kv_pairs_2023-11-11T14-15-31.csv',
    '2048-kv_pairs_2023-11-11T14-17-28.csv',
    '4096-kv_pairs_2023-11-11T14-19-25.csv',
    '8192-kv_pairs_2023-11-11T14-21-21.csv',
    # '8704-kv_pairs_2023-11-12T02-22-45.csv',
    # '9216-kv_pairs_2023-11-12T02-24-43.csv',
    # '9728-kv_pairs_2023-11-12T02-26-48.csv',
    # '10240-kv_pairs_2023-11-12T02-28-46.csv',
    # '10752-kv_pairs_2023-11-12T02-30-44.csv',
    # '11264-kv_pairs_2023-11-12T02-32-43.csv',
    # '11776-kv_pairs_2023-11-12T02-34-41.csv',
    '12288-kv_pairs_2023-11-12T02-36-39.csv',
    # '12800-kv_pairs_2023-11-12T02-38-37.csv',
    # '13312-kv_pairs_2023-11-12T02-40-36.csv',
    # '13824-kv_pairs_2023-11-12T02-42-34.csv',
    # '14336-kv_pairs_2023-11-12T02-44-32.csv',
    # '14848-kv_pairs_2023-11-12T02-46-30.csv',
    # '15360-kv_pairs_2023-11-12T02-48-28.csv',
    # '15872-kv_pairs_2023-11-12T02-50-26.csv',
    '16384-kv_pairs_2023-11-11T14-23-18.csv',
    '32768-kv_pairs_2023-11-11T14-25-16.csv',
    '65536-kv_pairs_2023-11-11T14-27-14.csv',
]
indices = []
data = []
stddev = []
for filename in new_files:
    match = re.search("([0-9]+)-kv_pairs.*", filename)
    num_clients = int(match.group(1))
    mean_latency, stddev_latency = avg_throughput(os.path.join('./final-measurements/etcd-data/saturation', filename))
    indices.append(num_clients)
    data.append(mean_latency)
    stddev.append(stddev_latency)
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

ax.set_xticks([2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 6, 2 ** 8, 2 ** 10, 2 ** 12, 2 ** 14, 2 ** 16])
ax.set_xlim(0, 2 ** 17)
yticks = [0]
yticks.extend([10**i for i in range(1, 8)])
ax.set_yticks(yticks)
ax.set_ylim(0, 10**7)
# ax.set_title(title)
# ax.set_xlim(0, ax.get_xlim()[1])
# ax.set_xlim(0, 2**18)
# ax.set_ylim(0, 2**22)
# ax.set_ylim(0, ax.get_ylim()[1])
plt.savefig(f"final-thesis-figures/latency_concurrency_saturation_etcd.pdf", bbox_inches='tight', pad_inches=0.05)
plt.show()
plt.clf()
