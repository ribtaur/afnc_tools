import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

# Least squares
from scipy.optimize import curve_fit

# Enable LaTeX rendering
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')

def model(x,a,b):
    return a*x + b

def sci_notation_latex(value, error, precision=2):
    """Returns LaTeX string for value ± error in scientific notation"""
    exponent = int(np.floor(np.log10(abs(value))))
    mantissa = value / 10**exponent
    error_mantissa = error / 10**exponent
    return r"$\left( {:.{}f} \pm {:.{}f} \right) \cdot 10^{{{}}}$".format(
        mantissa, precision, error_mantissa, precision, exponent
    )

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
                sigma=df["Dd"]
            )
df["model"] = model(x, popt[0], popt[1])

perr = np.sqrt(np.diag(pcov))
Da, Db = perr

labela = sci_notation_latex(popt[0],Da,5)
labelb = sci_notation_latex(popt[1],Db)

fig, ax = plt.subplots()
ax.plot(x, df["model"], color="red", linewidth=1, label="Modelo\n"+"a = "+labela+"\n"+"b = "+labelb,zorder=2)
ax.plot(x,y,'o', markersize=4, markerfacecolor='none', label='Simulación',zorder=10,color="black")
#plt.errorbar(x, y, yerr, fmt='o',ms=1)
plt.grid(True)
ax.set_xlabel(r'$1/\sqrt{K_{3b}}$ ($\unit{\m}^{3/2}\unit{\J}^{-1/2}$)')
ax.set_ylabel(r'$\Delta$ (\unit{\nm})')
ax.set_yticks(np.arange(0,55,5))
l =ax.legend(loc='lower right')
#l =ax.legend(loc='lower right',bbox_to_anchor=(0.99, 0.2))
l.set_zorder(15)

fig.set_size_inches(4.5,3.5)

directory = os.path.split(filepath)[0]
fig.savefig(os.path.join(directory, 'anis.png'),dpi=300,bbox_inches="tight") 