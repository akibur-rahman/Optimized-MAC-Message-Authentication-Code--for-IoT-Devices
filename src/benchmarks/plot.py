import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def plot_results(results, message_sizes):
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('MAC Implementation Comparison', fontsize=16)
    colors = ['#FF9999', '#66B2FF', '#99FF99']

    metrics = {
        (0, 0): ('time', 'Execution Time (microseconds)'),
        (0, 1): ('memory', 'Memory Usage (bytes)'),
        (1, 0): ('cpu', 'CPU Usage (%)')
    }

    for (i, j), (metric, ylabel) in metrics.items():
        ax = axes[i, j]
        for idx, (impl_name, values) in enumerate(results[metric].items()):
            if metric == 'time':
                values = [v * 1e6 for v in values]
            ax.plot(message_sizes, values, marker='o',
                    label=impl_name, color=colors[idx])

        ax.set_xlabel('Message Size (bytes)')
        ax.set_ylabel(ylabel)
        ax.set_xscale('log')
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    plt.show()
