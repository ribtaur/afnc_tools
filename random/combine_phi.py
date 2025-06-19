import pandas as pd
import os
import glob
import numpy as np

def combine_phi_columns(parent_directory):
    combined_df = pd.DataFrame()

    # Find all 'phi_data.txt' files in subfolders
    pattern = os.path.join(parent_directory, '**', 'phi_data.txt')
    file_list = sorted(glob.glob(pattern, recursive=True))

    max_len = 0
    t_ref = None  # To hold the reference time column

    # First pass: find the max length
    for filepath in file_list:
        df = pd.read_csv(filepath, sep=r'\s+')
        max_len = max(max_len, len(df))
        if t_ref is None:
            t_ref = df['t'].values

    # Second pass: build DataFrame with padding
    for i, filepath in enumerate(file_list):
        df = pd.read_csv(filepath, sep=r'\s+')
        phi = df['phi'].values
        current_len = len(phi)

        # Pad with the last value if too short
        if current_len < max_len:
            pad_length = max_len - current_len
            last_val = phi[-1]
            phi = np.concatenate([phi, np.full(pad_length, last_val)])

        # First file: also add time
        if i == 0:
            combined_df['t'] = t_ref[:max_len]

        # Add phi column
        combined_df[f'phi_{i+1}'] = phi

    # Save the result
    output_path = os.path.join(parent_directory, 'combined_phi_data.txt')
    combined_df.to_csv(output_path, index=False, sep=' ')

    return combined_df


rootdir = os.path.abspath(os.path.dirname( __file__ ))
combine_phi_columns(rootdir)