import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# Enable LaTeX rendering
plt.rcParams['text.usetex'] = True

rootdir = os.path.abspath(os.path.dirname( __file__ ))
filepath = os.path.join(rootdir,'paramtable.txt')
df = pd.read_csv(filepath, sep=" ")

x = 1 / np.sqrt(df["K3B"])
y = df["d"]
yerr = abs(df["Dd"])

fig, ax = plt.subplots()
ax.plot(x,y,'o', markersize=3.5)
plt.errorbar(x, y, yerr, fmt='o',ms=1)
plt.grid(True)
ax.set_xlabel(r'$\frac{1}{\sqrt{K_{3b}}}$')
ax.set_ylabel(r'Anchura de la pared $d$')

directory = os.path.split(filepath)[0]
fig.savefig(os.path.join(directory, 'anis.png'),dpi=300) 