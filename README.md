# TOOLS FOR DOMAIN WALL ANALYSIS USING MUMAX_AFNC

Intended use:

1. Save the magnetizations in OVF_TEXT format, and if possible crop it like this:
"save(Crop(m1, 0, Nx, Ny/2, Ny/2 + 1, 0, Nz))" to reduce computing time significantly.

2. Run **ovfplot3.py** to extract the coordinates of the central row (central Z, central Y and X as the independent variable) into text files and plots. There are different arguments the script can be called upon
   - *--full* : if you are using the uncropped OVF file
   - *--force* : the script skips rendering and extracting data from a OVF file if it spots an already rendered image in the directory. Use this argument if you want to overwrite the existing files.
   - *--text* : same as --force but only to force creating text files.

3. Run **datasplit_smart.py** to split the text files into different domain walls.
4. Run **nonlinearfit_split** to adjust each split according to the Walker's Ansatz. Creates a plot with original data and the fitted model as well as different text files with such data and files containing the adjusted parameters for each segment.
   - *--force* : to force re-adjusting the data and overwriting the images and text files
6. Run **paramtable_split.py** to gather the parameters from each segment and directory and neatly store them in a dataframe, saved as a txt file. This table can be easily analysed with the pandas package.

There are multiple edge cases where these instructions don't work, for the moment I recommend you use 128 cells in the Y axis. If you don't you'll need to use the *--full* argument.
