# Keyboard Design Frequency Graphs

This repository contains bar graphs comparing **bigram** and **skipgram** frequencies in English according to the _iWeb corpus_ (more specifically the free samples of it avaiable).  Analyzing **bigram** and **skipgram** frequencies is important for the creation of alternative layouts, as an optimal arragment should try to limit the occurence of bigrams and skipgrams typed using the same finger. To better understand why avoiding this is ideal, see my paper [A Data-Driven Approach to Keyboard Optimization](https://github.com/sekaha/DDAKO/blob/main/Paper.pdf).

### Overview

- **Bigrams**: Two-character sequences appearing in English text, e.g., `th`, `he`, and `er`. 
- **Skipgrams** Two-character sequences with the intervening character removed, e.g., `te` in `the`, `my` in `may`.

### Graph Features

- **Handling Zipf’s Law**: Y-scale is adjusted to accommodate unequal letter frequencies, preventing the data of less frequent letters from being unreadable.
- **Custom Color Palette**: Frequencies are visualized using a color-blind accessible and perceptually uniform color scale via OKLab for clear interpretation across the different scales.
- **Sorted Bars**: The bars are sorted in descending order based on bigram frequency, visually prioritizing the most important bigrams for keyboard optimization, with skipgrams as a secondary factor for consideration.
- **Stacked bars** represent both bigram and skipgram frequencies, with skipgram occurrences placed on top of bigrams and shaded darker. This helps visualize the overall importance of a key combination.

### Normalization

- **Shift**-key variations are combined, e.g., `;` and `:`, and `e` and `E`.
- The Letter pairs are **noramlized** to be directionally independent, e.g., `th` and `ht`.

### Generating the Graphs Yourself

Run `generate.py` to generate the graphs. Change the `VALID_CHARS` constant to control which characters you generate graphs for. The only prerequisite is that you have python and matplotlib:
```bash
pip install matplotlib
```

### Graphs
![Skipgram and Bigram Comparison for A](out/A_Stats.png)
![Skipgram and Bigram Comparison for B](out/B_Stats.png)
![Skipgram and Bigram Comparison for C](out/C_Stats.png)
![Skipgram and Bigram Comparison for D](out/D_Stats.png)
![Skipgram and Bigram Comparison for E](out/E_Stats.png)
![Skipgram and Bigram Comparison for F](out/F_Stats.png)
![Skipgram and Bigram Comparison for G](out/G_Stats.png)
![Skipgram and Bigram Comparison for H](out/H_Stats.png)
![Skipgram and Bigram Comparison for I](out/I_Stats.png)
![Skipgram and Bigram Comparison for J](out/J_Stats.png)
![Skipgram and Bigram Comparison for K](out/K_Stats.png)
![Skipgram and Bigram Comparison for L](out/L_Stats.png)
![Skipgram and Bigram Comparison for M](out/M_Stats.png)
![Skipgram and Bigram Comparison for N](out/N_Stats.png)
![Skipgram and Bigram Comparison for O](out/O_Stats.png)
![Skipgram and Bigram Comparison for P](out/P_Stats.png)
![Skipgram and Bigram Comparison for Q](out/Q_Stats.png)
![Skipgram and Bigram Comparison for R](out/R_Stats.png)
![Skipgram and Bigram Comparison for S](out/S_Stats.png)
![Skipgram and Bigram Comparison for T](out/T_Stats.png)
![Skipgram and Bigram Comparison for U](out/U_Stats.png)
![Skipgram and Bigram Comparison for V](out/V_Stats.png)
![Skipgram and Bigram Comparison for W](out/W_Stats.png)
![Skipgram and Bigram Comparison for X](out/X_Stats.png)
![Skipgram and Bigram Comparison for Y](out/Y_Stats.png)
![Skipgram and Bigram Comparison for Z](out/Z_Stats.png)
![Skipgram and Bigram Comparison for ;](out/;_Stats.png)
![Skipgram and Bigram Comparison for '](out/'_Stats.png)
![Skipgram and Bigram Comparison for ,](out/,_Stats.png)
![Skipgram and Bigram Comparison for .](out/._Stats.png)
![Skipgram and Bigram Comparison for /](out/_Stats.png)
