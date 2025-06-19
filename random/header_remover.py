import argparse
import os
import time
import numpy as np
import pandas as pd
    
def head_rm(filename):
    with open(filename, 'r+') as fp:
        # Read all lines into a list
        lines = fp.readlines()
        
        # Replace the first line
        lines[0] = "t mx my mz m1_x m1_y m1_z m2_x m2_y m2_z m3_x m3_y m3_z\n"
        
        # Go back to the beginning of the file
        fp.seek(0)
        
        # Write all lines back to the file
        fp.writelines(lines)
        
        # Truncate the remaining part of the file if the new content is shorter
        fp.truncate()

def create_phi_file(filename):
    # Read the input file using space as separator (handle multiple spaces)
    df = pd.read_csv(filename, sep=r"\s+")

    # Extract relevant columns
    t = df["t"]
    m1_y = df["m1_y"]
    m1_x = df["m1_x"]

    # Compute phi using atan2
    phi = np.rad2deg(np.unwrap(np.arctan2(m1_y, m1_x)))
    # Create a new DataFrame with desired columns
    result_df = pd.DataFrame({
        "t": t,
        "phi": phi
    })

    # Save to new file in the same directory
    directory = os.path.dirname(filename)
    output_path = os.path.join(directory, 'phi_data.txt')
    result_df.to_csv(output_path, index=False, sep=' ')

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Creates dataframes from table.txt in MuMax3")
    parser.add_argument("--force", action="store_true", help="Force creating dataframe even if the file already exists.")
    args = parser.parse_args()

    start = time.time()
    rootdir = os.path.abspath(os.path.dirname(__file__))

    for root, dirs, files in os.walk(rootdir, topdown=True):
        imgdir = os.path.join(root, 'tab.txt')
        tabdir = os.path.join(root, 'table.txt')
        if os.path.isfile(tabdir):
            if os.path.isfile(imgdir) and not args.force:
                print(f"The file '{imgdir}' is already rendered. Skipping...")
            else:
                if os.path.isfile(tabdir):
                    head_rm(tabdir)
                    create_phi_file(tabdir)

    end = time.time()
    print('Done in {:6.3f}s'.format(end - start))