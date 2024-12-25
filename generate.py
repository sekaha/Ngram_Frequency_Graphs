from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt
from collections import defaultdict
from conversion import merge, rgb_to_hex, okhsl_to_srgb

# Constants
VALID_CHARS = "etaoinsrhldcumfgpywbvkxjzq;',./"
VALID_CHARS_SHIFT = "ETAOINSRHLDCUMFGPYWBVLXJZQ:\"<>?"
BIGRAM_FILE = 'bigrams.txt'
SKIPGRAM_FILE = '1-skip.txt'

# Color stuff
HIGH_COL = (0.28426, 0.98432, 0.88120)
LOW_COL = (0.87718, 0.84056, 0.16683)

# Utils
LOWER_CHARS = {c1 : c2 for c1, c2 in zip(VALID_CHARS_SHIFT, VALID_CHARS)}

def lower(s):
    return "".join([LOWER_CHARS[c] if c in LOWER_CHARS else c for c in s])

def get_col(freq, offset=0):
    t = (freq)/high_freq

    h, s, l = merge(LOW_COL, HIGH_COL, t)

    return rgb_to_hex(*okhsl_to_srgb(h, s, min(l+offset, 1)))

# Get bigram freqs
bigram_freqs = defaultdict(int)

with open(BIGRAM_FILE) as f:
    for l in f:
        bigram, freq = l.split('\t')
        bigram = lower(bigram)

        if all(c in VALID_CHARS for c in bigram):
            bigram_freqs[bigram] += int(freq)
            bigram_freqs[bigram[1]+bigram[0]] += int(freq)

# Get skipgram freqs
skipgram_freqs = defaultdict(int)

with open(SKIPGRAM_FILE) as f:
    for l in f:
        skipgram, freq = l.split('\t')
        skipgram = lower(skipgram)

        if all(c in VALID_CHARS for c in skipgram):
            skipgram_freqs[skipgram] += int(freq)
            skipgram_freqs[skipgram[1]+skipgram[0]] += int(freq)

# Generate the graphs
high_freq = max(*skipgram_freqs.values(), *bigram_freqs.values())
high_scale = max(bigram_freqs[c1+c2]+skipgram_freqs[c1+c2] for c1 in VALID_CHARS for c2 in VALID_CHARS)*1
bigram_cmap = LinearSegmentedColormap.from_list("custom", [get_col(v, 0.09) for v in range(0, high_freq, 20000)])

for target in VALID_CHARS:
    labels = [target+c for c in VALID_CHARS]

    indices = sorted(range(len(labels)), key=lambda i: -(bigram_freqs[labels[i]]))
    labels = [labels[i] for i in indices]

    bigram_colors = [get_col(bigram_freqs[l], 0.075) for l in labels]
    skipgram_colors = [get_col(skipgram_freqs[l], -0.075) for l in labels]

    fig, ax = plt.subplots(figsize=(24, 9))

    # Plot each bar type
    bigram_vals = [bigram_freqs[l] for l in labels]
    skipgram_vals = [skipgram_freqs[l] for l in labels]
    bigram_bar = ax.bar(labels, bigram_vals, label='bigram',  color=bigram_colors, edgecolor='white')
    skipgram_bar = ax.bar(labels, skipgram_vals, label='skipgram', bottom=bigram_vals, color=skipgram_colors, edgecolor='white')

    plt.ylabel('Cummulitative Occurence Count', fontsize=18)
    plt.title(f"{target.upper()} - Bigram (Bottom) vs. Skipgram (Top) Occurences", fontsize=24)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    # Gradient legend explanation
    bigram_sm = plt.cm.ScalarMappable(cmap=bigram_cmap, norm=plt.Normalize(vmin=0, vmax=high_freq))
    bigram_cbar = plt.colorbar(bigram_sm, ax=ax)
    bigram_cbar.ax.set_ylabel('Frequency Intensity', fontsize=18, rotation=270, labelpad=20)
    
    plt.savefig(f'out/{target.upper()}_Stats.png', format='png', dpi=300, bbox_inches='tight')
    # plt.show()
    print(f"Exported {target.upper()}_Stats.png")
    plt.close()
