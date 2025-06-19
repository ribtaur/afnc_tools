import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Enable LaTeX rendering
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')

def plot_combined_phi(file_path):
    # Read the combined phi data
    df = pd.read_csv(file_path, sep=r'\s+')

    # Extract time
    t = df['t']

    fig, ax = plt.subplots()
    for col in df.columns:
        if col.startswith('phi_'):
            plt.plot(t*1e12, df[col])

    # Labeling
    plt.xlabel(r'Tiempo ($\unit{\ps}$)')
    plt.ylabel(r'$\varphi$',rotation=0)
    plt.title(r'Estados aleatorios con $K_{3b}<0$')
    plt.grid(True)
    yticks = np.arange(-165, 195, 30)  # Shift center to 0
    ax.set_yticks(yticks)
    # Show the plot
    plt.tight_layout()
    plt.xlim(0,12)
    directory = os.path.split(filepath)[0]
    fig.set_size_inches(3, 3.5, forward=True)
    plt.savefig(os.path.join(directory, 'random.png'),bbox_inches='tight',dpi=300)

rootdir = os.path.abspath(os.path.dirname(__file__))
filepath = os.path.join(rootdir,'combined_phi_data.txt')
plot_combined_phi(filepath)
