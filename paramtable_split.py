import numpy as np
import os

def ParamFetch(filepath,i):
    # Get q and delta from params.txt
    with open(filepath, 'r') as f:
        lines = f.readlines()

    q = delta = Dq = Ddelta = a11 = a12 = kb = th1 = th2 = None
    for i, line in enumerate(lines):
        if 'q =' in line:
            q = np.float32(line.split()[-1])
        elif 'Delta =' in line:
            delta = np.float32(line.split()[-1])
        elif 'q_err =' in line:
            Dq = np.float32(line.split()[-1])
        elif 'Delta_err =' in line:
            Ddelta = np.float32(line.split()[-1])
        elif 'TH1 =' in line:
            th1 = np.float32(line.split()[-1])
        elif 'TH2 =' in line:
            th2 = np.float32(line.split()[-1])
    f.close()

    # Get A11, A12, K3b from log.txt
    directory = os.path.split(filepath)[0]
    with open(os.path.join(directory,"log.txt"), 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        if 'A11 :=' in line:
            a11 = float(line.split()[-1])
        elif 'A12 :=' in line:
            a12 = float(line.split()[-1])
        elif 'K3B :=' in line:
            kb = np.float32(line.split()[-1])
        elif 'K3BL :=' in line:
            kb = np.float32(line.split()[-1])
        pass
    f.close()
    return q, delta, Dq, Ddelta, a11, a12, kb, th1, th2

rootdir = os.path.abspath(os.path.dirname( __file__ ))
#rootdir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
mainfile = os.path.join(rootdir,'paramtable.txt')

table = open(mainfile, 'w')
table.write("q d Dq Dd A11 A12 K3B TH1 TH2 seg\n")

for i in range(3):
    for root, dirs, files in os.walk(rootdir,topdown=True):
        tabdir = os.path.join(root,'params_{}.txt'.format(i))
        if os.path.isfile(tabdir):
            Params = ParamFetch(tabdir,i)
            table.write("{0} {1} {2} {3} {4} {5} {6} {7} {8} {9}\n".format(Params[0],Params[1],Params[2],Params[3],Params[4],Params[5],Params[6],Params[7],Params[8],i))