import matplotlib.pyplot as plt
import numpy as np

def visualize_points(asset, points, ordered = set([])):
    ts_time = asset.data['t']
    ts_data = asset.data['o']

    buying_points = [(b[1], b[2]) for b in points if b[0] == 'buy']
    selling_points = [(s[1], s[2]) for s in points if s[0] == 'sell']

    buying_points_ordered = [b for b in buying_points if b[0] not in ordered]
    selling_points_ordered = [s for s in selling_points if s[0] not in ordered]

    fig = plt.figure(figsize=(50, 30))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(ts_time, ts_data, color='black', linewidth=0.1)

    ploted_xticks = ts_time[np.array(range(0, len(ts_time), 150))]
    ax.set_xticks(ploted_xticks)
    ax.set_xticklabels([x.split('T')[0] for x in ploted_xticks])

    ax.scatter([x[0] for x in buying_points], [x[1] for x in buying_points], s=100, c='red')
    ax.scatter([x[0] for x in selling_points], [x[1] for x in selling_points], s=100, c='blue')
    # ax.scatter([x[0] for x in exit_points], [x[1] for x in exit_points], s=100, c='orange')
    ax.scatter([x[0] for x in buying_points_ordered], [x[1] for x in buying_points_ordered], s=100, c='white', alpha=0.7)
    ax.scatter([x[0] for x in selling_points_ordered], [x[1] for x in selling_points_ordered], s=100, c='white', alpha=0.7)