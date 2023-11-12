import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import ticker


def avg_throughput(filename: str):
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
            latencies.append(end_timestamp - start_timestamp)
            end_seconds = int(end_timestamp / 1000 / 1000 / 1000)
            end_times.append(end_seconds)
            # end_times.append(datetime.datetime.fromtimestamp())  # from nanoseconds to seconds

    min_end_time = np.min(end_times)
    end_times = np.subtract(end_times, min_end_time)
    np.sort(end_times)
    unique, counts = np.unique(end_times, return_counts=True)
    second_counts = dict(zip(unique, counts))
    for i in range(unique[-1]):
        if i not in second_counts:
            second_counts[i] = 0

    mean_latency = np.mean(latencies)
    print(f'Mean latency: {mean_latency}')

    shift_by = 10
    print(filename)
    print(counts)
    mean_throughput = np.mean(counts[shift_by:shift_by + 60])
    stddev_throughput = np.std(counts[shift_by:shift_by + 60])
    print(f"Mean throughput: {mean_throughput}")
    print()
    return mean_throughput, stddev_throughput


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
# dirname = "./final-measurements/bftsmart-data/temp-saturation"
# files = [
#     '1-X-X-bftsmart_2023-11-12T14:19:13.564213558.csv',
#     '2-X-X-bftsmart_2023-11-12T14:21:07.021541189.csv',
#     '4-X-X-bftsmart_2023-11-12T14:23:01.367740039.csv',
#     '8-X-X-bftsmart_2023-11-12T14:24:55.945090522.csv',
#     '16-X-X-bftsmart_2023-11-12T14:26:50.301045010.csv',
#     '32-X-X-bftsmart_2023-11-12T14:28:44.991188406.csv',
#     '64-X-X-bftsmart_2023-11-12T14:30:39.573545243.csv',
#     '128-X-X-bftsmart_2023-11-12T14:32:35.584478091.csv',
#     '256-X-X-bftsmart_2023-11-12T14:34:31.242884044.csv',
#     '512-X-X-bftsmart_2023-11-12T14:36:28.068634489.csv',
#     '640-X-X-bftsmart_2023-11-12T14:38:27.034207284.csv',
#     '768-X-X-bftsmart_2023-11-12T14:40:27.970166139.csv',
#     '896-X-X-bftsmart_2023-11-12T14:42:28.151524590.csv',
#     '1024-X-X-bftsmart_2023-11-12T14:44:31.332586720.csv',
#     '1152-X-X-bftsmart_2023-11-12T14:46:35.498410603.csv',
#     '1280-X-X-bftsmart_2023-11-12T14:48:40.569337624.csv',
#     '1408-X-X-bftsmart_2023-11-12T14:50:51.659001758.csv',
#     '1536-X-X-bftsmart_2023-11-12T14:53:03.118671807.csv',
#     '1664-X-X-bftsmart_2023-11-12T14:55:13.280300789.csv',
#     '1792-X-X-bftsmart_2023-11-12T14:57:29.446527381.csv',
#     '1920-X-X-bftsmart_2023-11-12T14:59:43.965255444.csv',
#     '2048-X-X-bftsmart_2023-11-12T15:02:04.993582638.csv',
#     '4096-X-X-bftsmart_2023-11-12T15:04:24.567365102.csv',
# ]
indices = []
data = []
stddev = []
for filename in files:
    match = re.search("([0-9]+)-(X-X-)?bftsmart.*", filename)
    num_clients = int(match.group(1))
    mean_throughput, stddev_throughput = avg_throughput(os.path.join(dirname, filename))
    indices.append(num_clients)
    data.append(mean_throughput)
    stddev.append(stddev_throughput)
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
ax = df.plot(linestyle='none', marker='d', color='k', clip_on=False, zorder=10, yerr=stddev, capsize=4)
ax.legend().set_visible(False)
ax.grid(True)
ax.set_xlabel('Concurrent Clients')
ax.set_ylabel('Throughput [req/s]')
idx = np.argmax(data)
print(f"{idx} {indices[idx]} {data[idx]}")
ax.set_xscale('log', base=2)
# ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: '{:g}'.format(x)))
# ax.set_yticks(np.arange(0, 801, 100))
title = f'Throughput for {num_clients} Concurrent Client Requests'
if num_clients == 1:
    title = f'Throughput for Sequential Client Requests'

ax.set_xticks([2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3, 2 ** 4, 2 ** 6, 2 ** 8, 2 ** 10, 2 ** 12])
# ax.set_title(title)
# ax.set_xlim(0, ax.get_xlim()[1])
# ax.set_xlim(0, 2 ** 18)
ax.set_ylim(0, 80000)
# ax.set_ylim(0, ax.get_ylim()[1])
plt.savefig(f"final-thesis-figures/throughput_concurrency_saturation_bftsmart.pdf", bbox_inches='tight',
            pad_inches=0.05)
plt.show()
plt.clf()
