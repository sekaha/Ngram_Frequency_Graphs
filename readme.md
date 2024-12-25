# Keyboard Design Frequency Graphs

This repository contains bar graphs comparing **bigram** and **skipgram** frequencies in English according to the _iWeb corpus_ (more specifically the free samples of it avaiable).  Analyzing **bigram** and **skipgram** frequencies is important for the creation of alternative layouts, as an optimal arragment should try to limit the occurence of bigrams and skipgrams typed using the same finger. To better understand why avoiding this is ideal, see my paper [A Data-Driven Approach to Keyboard Optimization]([https://github.com/sekaha/DDAKO]).

![Skipgram and Bigram Comparison for A](/out/A_stats.png)


### Overview

- **Bigrams**: Two-character sequences appearing in English text i.e., `th`, `he`, and `er`. 
- **Skipgrams** Two-character sequences with the interveaning character removed i.e., `te` in `the`, `my` in `may`.

### Graph Features

- **Handling Zipf’s Law**: Scales are adjusted to accommodate unequal letter frequencies, preventing the data of less frequent letters from being unreadable.
- **Custom Color Palette**: Frequencies are visualized using a color-blind accessible and perceptually uniform color scale via OKLab for clear interpretation across the different scales.
- **Sorted Bars**: The bars are sorted in descending order based on bigram frequency, visually prioritizing the most important bigrams for keyboard optimization, with skipgrams as a secondary factor for consideration.
- **Stacked bars** represent both bigram and skipgram frequencies, with skipgram occurrences placed on top of bigrams and shaded darker. This helps visualize the overall importance of a key combination.

### Normalization

- **Shift**-key variations are combined (e.g., `;` and `:`, and `e` and `E` are considered equivalent).
- The Letter pairs are **noramlized** to be directionally independent (e.g., `th` and `ht` are treated the same).

### Generating the Graphs Yourself

Run `generate.py` to generate the graphs. Change the `VALID_CHARS` constant to control which characters you generate graphs for. The only prerequisite is that you have python and matplotlib:
```bash
pip install matplotlib
```
