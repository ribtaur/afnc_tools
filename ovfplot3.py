import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
import time

# Enable LaTeX rendering
plt.rc('text', usetex=True)
plt.rc('text.latex', preamble=r'\usepackage{siunitx}')

def parse_ovf1(filename, getnodes):
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Extract metadata
    xnodes = ynodes = znodes = None
    data_start = None
    for i, line in enumerate(lines):
        if 'xnodes' in line:
            xnodes = int(line.split()[-1])
        elif 'ynodes' in line:
            ynodes = int(line.split()[-1])
        elif 'znodes' in line:
            znodes = int(line.split()[-1])
        elif 'Title' in line:
            title = line.split()[-1]
        elif '# Begin: Data Text' in line:
            data_start = i + 1
            break

    if None in (xnodes, ynodes, znodes) or data_start is None:
        raise ValueError("Could not parse OVF1 header properly")

    # Load data
    data = []
    for line in lines[data_start:]:
        if '# End:' in line:
            break
        parts = line.strip().split()
        if len(parts) == 3:
            data.append([float(p) for p in parts])

    data = np.array(data)
    data = data.reshape((znodes, ynodes, xnodes, 3))
    if getnodes == 0:
        return data, xnodes, ynodes, znodes, title
    else:
        return data, title

def plot_central_row(filename):
    data, xnodes, ynodes, znodes, title = parse_ovf1(filename)
    mid_z = znodes // 2
    mid_y = ynodes // 2
    title=title.strip('_')[:1]
    row_data = data[mid_z, mid_y, :, :]
    x = np.arange(xnodes)
    #y = np.zeros_like(x)

    u = row_data[:, 0]
    v = row_data[:, 1]
    w = row_data[:, 2]

    #plt.figure(figsize=(10, 2))
    #plt.quiver(x, y, u, v, scale=1, scale_units='xy', angles='xy')
    plt.title(title+' Central Row')
    plt.xlabel('X')
    #plt.axis('equal')
    #plt.plot(x, u, 'r', x, v, 'g', x, w, 'b', label=['m_x','m_y','m_z'])
    plt.plot(x, u, 'r', label=(title+'x'))
    plt.plot(x, v, 'g', label=(title+'y'))
    plt.plot(x, w, 'b', label=(title+'z'))
    plt.grid(True)
    plt.ylim([-1,1])
    plt.legend(loc='lower right')
    #plt.legend(loc='lower right', bbox_to_anchor=(0.5, -0.05))
    directory = os.path.split(filename)[0]
    plt.savefig(os.path.join(directory, title+'.png'),bbox_inches='tight',dpi=300)
    plt.close()
    #plt.show()

def plot_cw_ang(filenames, onlytxt = 0):
    data1, xnodes, ynodes, znodes, title1 = parse_ovf1(filenames[0], 0)
    data2, title2 = parse_ovf1(filenames[1], 1)
    data3, title3 = parse_ovf1(filenames[2], 1)
    mid_z = znodes // 2
    mid_y = ynodes // 2
    title1=title1.strip('_')
    title2=title2.strip('_')
    title3=title3.strip('_')
    
    fig, ax = plt.subplots()

    for i, data in enumerate([data1, data2, data3]):
        row_data = data[mid_z, mid_y, :, :]
        u = row_data[:, 0]
        v = row_data[:, 1]
        #w = row_data[:, 2]
        theta = np.atan2(v,u)
        #theta = np.where(theta < 0, theta + 2*np.pi, theta)
        theta = np.unwrap(theta)
        theta = np.rad2deg(theta)
        
        if i == 0:
            theta1 = theta
            #phi1 = phi
        elif i == 1:
            theta2 = theta
            #phi2 = phi
    
    #y = np.zeros_like(x)
    x = np.arange(xnodes)

    # Write x and theta1 to a text file
    directory = os.path.split(filenames[0])[0]
    txt_filepath = os.path.join(directory, 'theta1_data.txt')
    with open(txt_filepath, 'w') as f:
        f.write("x theta1\n")
        for xi, t1 in zip(x, theta1):
            f.write(f"{xi} {t1}\n")
    
    # Skip rendering plots if onlytxt is 1
    if onlytxt == 1:
        return

    #plt.figure(figsize=(10, 2))

    xticks = np.arange(0, xnodes+1, int(xnodes/4))
    xlabels = xticks - int(xnodes/2)  # Shift center to 0
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels)

    plt.title(r'$\varphi_1$, Fila central')
    plt.xlabel(r'$x$ $\unit{\nm}$')
    #plt.xticks(np.arange(0,1024,128))
    plt.ylabel(r'$\varphi$',rotation=0)
    plt.yticks(np.arange(-435,435,15))
    #plt.axis('equal')
    #plt.plot(x, u, 'r', x, v, 'g', x, w, 'b', label=['m_x','m_y','m_z'])
    plt.plot(x, theta1, 'r', label=r'$\vec{m}_1$')

    # Add a horizontal line at y=0
    #plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    # Add a vertical line at x=256
    plt.axvline(x=xnodes/2, color='black', linestyle='--', linewidth=0.8)

    plt.margins(0.05)

    plt.grid(True)
    #plt.ylim([0,360])
    directory = os.path.split(filenames[0])[0]
    plt.savefig(os.path.join(directory, 'angle.png'),bbox_inches='tight',dpi=300)

    plt.title('Theta, Central Row')
    plt.yticks(np.arange(-435,435,30))
    plt.plot(x, theta2, 'g', label=r'$\vec{m}_2$')
    plt.plot(x, theta, 'b', label=r'$\vec{m}_3$')

    plt.legend(loc='lower right')
    #plt.legend(loc='lower right', bbox_to_anchor=(0.5, -0.05))
    
    fig.savefig(os.path.join(directory, 'angles.png'),bbox_inches='tight',dpi=300)
    plt.close(fig)
    #plt.show()

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Render plots from OVF files.")
    parser.add_argument("--force", action="store_true", help="Force rendering even if the image already exists.")
    parser.add_argument("--txt", action="store_true", help="Force creating txt even if image is skipped.")
    parser.add_argument("--full", action="store_true", help="Uses full OVF file instead of strip")
    args = parser.parse_args()

    start = time.time()
    rootdir = os.path.abspath(os.path.dirname(__file__))
    mags = ['m1', 'm2', 'm3']

    for root, dirs, files in os.walk(rootdir, topdown=True):
        imgdir = os.path.join(root, 'angles.png')
        tabdirs = [None, None, None]
        for i, mag in enumerate(mags):
            if args.full:
                tabdirs[i] = os.path.join(root, mag + '_000002.ovf')
            else:
                tabdirs[i] = os.path.join(root, mag + '__yrange64_000000.ovf')
        if os.path.isfile(tabdirs[0]):
            if os.path.isfile(imgdir) and not args.force:
                print(f"The file '{imgdir}' is already rendered. Skipping...")
                if args.txt:
                    print(f"Writing txt...")
                    plot_cw_ang(tabdirs, 1)
                continue
            else:
                if os.path.isfile(tabdirs[0]):
                    plot_cw_ang(tabdirs)
                    # plot_central_row(tabdirs[0])

    end = time.time()
    print('Done in {:6.3f}s'.format(end - start))