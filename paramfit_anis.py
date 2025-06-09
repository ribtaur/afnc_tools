import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# Least squares
from scipy.optimize import curve_fit

# Enable LaTeX rendering
plt.rcParams['text.usetex'] = True

def model(x,a,b):
    return a*x + b

rootdir = os.path.abspath(os.path.dirname( __file__ ))
filepath = os.path.join(rootdir,'paramtable.txt')
df = pd.read_csv(filepath, sep=" ")

x = 1 / np.sqrt(df["K3B"])
y = df["d"]
yerr = abs(df["Dd"])

popt, pcov = curve_fit(
                f=model,       # model function
                xdata=x,   # x data
                ydata=y,   # y data
                p0=(1000, 0),      # initial value of the parameters
            )
df["model"] = model(x, popt[0], popt[1])

fig, ax = plt.subplots()
ax.plot(x, df["model"], color="red", linewidth=1.75, label="Modelo \n a = {:.2f}\n b = {:.2f}".format(popt[0],popt[1]),zorder=2)
ax.plot(x,y,'o', markersize=4, markerfacecolor='none', label='Simulación',zorder=10,color="black")
#plt.errorbar(x, y, yerr, fmt='o',ms=1)
plt.grid(True)
ax.set_xlabel(r'$\frac{1}{\sqrt{K_{3b}}}$')
ax.set_ylabel(r'Anchura de la pared $d$')
l =ax.legend(loc='lower right')
#l =ax.legend(loc='lower right',bbox_to_anchor=(0.99, 0.2))
l.set_zorder(15)


directory = os.path.split(filepath)[0]
fig.savefig(os.path.join(directory, 'anis.png'),dpi=300) 