import numpy as np
import os

def get_split_indices(dy_dx, min_drop):
    indices = [0]
    for i in range(1, len(dy_dx) - 1):
        if dy_dx[i - 1] - dy_dx[i] > min_drop and dy_dx[i + 1] - dy_dx[i] > min_drop:
            indices.append(i)
    indices.append(len(dy_dx) - 1)
    return sorted(set(indices))

def get_split_indices_m(dy_dx, min_drop):
    indices = [0]
    for i in range(1, len(dy_dx) - 1):
        if dy_dx[i] - dy_dx[i - 1] > min_drop and dy_dx[i] - dy_dx[i + 1] > min_drop:
            indices.append(i)
    indices.append(len(dy_dx) - 1)
    return sorted(set(indices))

def DataSplit(filename):
    data = np.loadtxt(filename, skiprows=1)
    x = data[:,0]
    y = data[:,1]
    # --- Compute first derivative ---
    dy_dx = np.gradient(y, x)

    # --- Parameters ---
    initial_min_drop = 0.05
    max_dy_threshold = 75
    min_dy_threshold = 20
    max_iterations = 10  # prevent infinite loops

    # --- Smart min_drop adjustment loop ---
    min_drop = initial_min_drop
    for iteration in range(max_iterations):
        dy_dx = np.gradient(y, x)
        if y[0] < y[-1]:
            split_indices = get_split_indices(dy_dx, min_drop)
        else:
            split_indices = get_split_indices_m(dy_dx, min_drop)

        # Calculate y-range for each segment
        all_ok = True
        for i in range(len(split_indices) - 1):
            start, end = split_indices[i], split_indices[i + 1]
            y_range = y[start:end+1]
            delta_y = np.max(y_range) - np.min(y_range)

            if delta_y > max_dy_threshold:
                min_drop /= 10
                print(f"Iteration {iteration}: Δy={delta_y:.2f} too high → min_drop -> {min_drop:.6f}")
                all_ok = False
                break  # Retry with lower min_drop

            if delta_y < min_dy_threshold:
                min_drop *= 10
                print(f"Iteration {iteration}: Δy={delta_y:.2f} too low → min_drop -> {min_drop:.6f}")
                all_ok = False
                break  # Retry with higher min_drop

        if all_ok:
            print(f"Final min_drop = {min_drop:.6f}")
            break

    # --- Generate output segments ---
    for i in range(len(split_indices) - 1):
        start_idx = split_indices[i]
        end_idx = split_indices[i + 1]

        y_segment = np.copy(y)
        y_start = y[start_idx]
        y_end = y[end_idx]

        y_segment[:start_idx] = y_start
        y_segment[end_idx + 1:] = y_end

        # Reduce to range 15º to whatever
        y_segment = y_segment - min(y_segment) + 15

        # Combine with x and save
        directory = os.path.split(filename)[0]
        segment_data = np.column_stack((x, y_segment))
        outname = os.path.join(directory, 'segment_{}.txt'.format(i))
        np.savetxt(outname, segment_data, fmt='%.6f', header='x theta1', comments='')

rootdir = os.path.abspath(os.path.dirname( __file__ ))
for root, dirs, files in os.walk(rootdir,topdown=True):
        tabdir = os.path.join(root,'theta1_data.txt')
        if os.path.isfile(tabdir):
            DataSplit(tabdir)