# manage data and fit
import numpy as np
import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Enable LaTeX rendering
plt.rcParams['text.usetex'] = True

# Least squares
from scipy.optimize import curve_fit

def f_model(x,q,d):
    return (2/3)*np.rad2deg(np.arctan(np.exp((x-q)/d))) + 15

def f_model_diff(x,q,d):
    return (1/3)*np.rad2deg(np.arctan(np.exp((x-q)/d))) + 15

def f_model_m(x,q,d):
    return (2/3)*np.rad2deg(np.arctan(np.exp(-(x-q)/d))) + 15

def f_model_diff_m(x,q,d):
    return (1/3)*np.rad2deg(np.arctan(np.exp(-(x-q)/d))) + 15

def ModelFit(filepath,i):
    # Load the data
    df = pd.read_csv(filepath, sep=" ")
    title = (os.path.basename(os.path.dirname(filepath)))
    if args.seg:
        title = title + ' Segmento {}'.format(i)
    # Fit the model
    if (max(df["theta1"])-min(df["theta1"]) > 45):
        isdiff = False
        
        if df["theta1"][0] < 30:
            popt, pcov = curve_fit(
                f=f_model,       # model function
                xdata=df["x"],   # x data
                ydata=df["theta1"],   # y data
                p0=(240, 5),      # initial value of the parameters
            )
            df["model"] = f_model(df["x"], popt[0], popt[1])
        else:
            popt, pcov = curve_fit(
            f=f_model_m,       # model function
            xdata=df["x"],   # x data
            ydata=df["theta1"],   # y data
            p0=(240, 5),      # initial value of the parameters
            )
            df["model"] = f_model_m(df["x"], popt[0], popt[1])
    else:
        isdiff = True
        if df["theta1"][0] < 30:
            popt, pcov = curve_fit(
            f=f_model_diff,       # model function
            xdata=df["x"],   # x data
            ydata=df["theta1"],   # y data
            p0=(240, 5),      # initial value of the parameters
            )
            df["model"] = f_model_diff(df["x"], popt[0], popt[1])
        else:
            popt, pcov = curve_fit(
            f=f_model_diff_m,       # model function
            xdata=df["x"],   # x data
            ydata=df["theta1"],   # y data
            p0=(240, 5),      # initial value of the parameters
            )
            df["model"] = f_model_diff_m(df["x"], popt[0], popt[1])
    
    rows =  df.shape[0]
    q = popt[0] - rows/2
    perr = np.sqrt(np.diag(pcov))
    Dq, Dd = perr

    # Create the plot
    fig, ax = plt.subplots()
    axb = ax.twinx()
    
    
    # Separate dense and scarce data
    dense = (df["x"] >= popt[0] - 2.5*popt[1]) & (df["x"] <= popt[0] + 2.5*popt[1])
    sparsel = (df["x"] < popt[0] - 2.5*popt[1])
    sparser = (df["x"] > popt[0] + 2.5*popt[1])

    sparsel_x = df["x"][sparsel][::4]
    sparsel_y = df["theta1"][sparsel][::4]
    dense_x = df["x"][dense]
    dense_y = df["theta1"][dense]
    sparser_x = df["x"][sparser][::4]
    sparser_y = df["theta1"][sparser][::4]

    # Plot the line first
    ax.plot(df["x"], df["model"], color="red", linewidth=1.75, label="Modelo \n q     = {:.2f}\n $\Delta$ = {:.2f}".format(q,popt[1]),zorder=2)

    #ax.plot(df["x"][::8],df["theta1"][::8],'o', markersize=3.5, markerfacecolor='none', label='Simulación',zorder=10,color="black")
    ax.plot(sparsel_x,sparsel_y,'o', markersize=3.5, markerfacecolor='none',zorder=10,color="black")
    ax.plot(dense_x,dense_y,'o', markersize=3.5, markerfacecolor='none', label='Simulación',zorder=10,color="black")
    ax.plot(sparser_x,sparser_y,'o', markersize=3.5, markerfacecolor='none',zorder=10,color="black")
    
    # Add grid, labels, and ticks
    
    xticks = np.arange(0, rows+1, int(rows/8))
    xlabels = xticks - rows/2  # Shift center to 0

    ax.set_title('{}'.format(title))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)

    plt.xlim([rows/4,3*rows/4])
    
    if isdiff:
        ax.set_yticks(np.arange(15,16,60))
        axb.set_ylim(ax.get_ylim())
        axb.set_yticks(np.arange(45,46,60))
    else:
        ax.set_yticks(np.arange(15,76,60))
        axb.set_ylim(ax.get_ylim())
        axb.set_yticks(np.arange(45,46,60))
    
    ax.set_ylabel(r'Ángulos fáciles $K_{3b}>0$')
    #ax.tick_params(axis='y', labelcolor='blue')
    axb.set_ylabel(r'Ángulos fáciles $K_{3b}<0$')
    #axb.tick_params(axis='y', labelcolor='green')

    ax.grid(True,which="both",zorder=0)
    axb.grid(True,which="both",zorder=0.01)
    ax.set_xlabel('X en nm')
    #ax.set_ylabel(r'$\theta$', rotation=0)
    
    # Add a vertical line at x=256
    ax.axvline(x=rows/2, color='black', linestyle='--', linewidth=0.8)
    
    l =ax.legend(loc='lower right',bbox_to_anchor=(0.99, 0.2))
    l.set_zorder(15)

    # Save the plot
    directory = os.path.split(filepath)[0]
    fig.savefig(os.path.join(directory, 'segment_{}_model.png'.format(i)), bbox_inches='tight', dpi=300)
    plt.close(fig)

    # Save the updated DataFrame to a file
    df.to_csv(os.path.join(directory, 'segment_{}_model.txt'.format(i)), index=None, sep=' ')

    # Save params
    f = open(os.path.join(directory, "params_{}.txt".format(i)),"w")
    f.write("{}\n".format(title))
    f.write("q = {}\n".format(q))
    f.write("Delta = {}\n".format(popt[1]))
    f.write("q_err = {}\n".format(Dq))
    f.write("Delta_err = {}\n".format(Dd))
    f.write("TH1 = {}\n".format(df["theta1"][0]))
    f.write("TH2 = {}".format(df["theta1"].values[-1]))
    f.close

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Render plots from OVF files.")
    parser.add_argument("--force", action="store_true", help="Force rendering even if the image already exists.")
    parser.add_argument("--seg", action="store_true", help="Prints the segment name in the title of the plot")
    args = parser.parse_args()

    start = time.time()
    rootdir = os.path.abspath(os.path.dirname( __file__ ))
    #rootdir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

    for root, dirs, files in os.walk(rootdir,topdown=True):
        for i in range(3):
            tabdir = os.path.join(root,'segment_{0}.txt'.format(i))
            imgdir = os.path.join(root,'segment_{0}_model.png'.format(i))
            if os.path.isfile(imgdir) and not args.force:
                print(f"The file '{imgdir}' is already rendered. Skipping...")
                pass
            else:
                if os.path.isfile(tabdir):
                    ModelFit(tabdir,i)
    
    end = time.time()
    print('Done in {:6.3f}s'.format(end - start))