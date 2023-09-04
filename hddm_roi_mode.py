# warning settings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Data management
import pandas as pd
import numpy as np
import pickle

# Plotting
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

# HDDM
import hddm
from scipy.stats import norm
from sklearn.neighbors import KernelDensity
from scipy.stats import gaussian_kde


df_orig = pd.read_csv('/data/victoria/HDDM_code/full_brain_behav.csv')
df = df_orig
df.rt = df.rt/1000
df = hddm.utils.flip_errors(df)
df = df.dropna()
early_learn = df[df['run'].isin([1, 2])].copy()


roi_ls = [39,40,41,42,43,44,48,51,52,53,60,61,65,67,68,70,74,77,78,79,80,81,82,83,88,90,91,92,93,94,99,105,106]

for i in range(108):
    roi =  roi_ls[i]
    m_reg = hddm.HDDMRegressor(early_learn, [f"v ~ roi{roi} * C(type,Treatment('prototype'))", \
                                        f"a ~ roi{roi} * C(type,Treatment('prototype'))",\
                                        f"t ~ roi{roi}* C(type,Treatment('prototype'))"],
                                    p_outlier=0.05)  
    m_reg.find_starting_values()
    m_reg.sample(2000, burn=1000)
    # m_reg.print_stats()
    # Get a list of all node names in the model
    node_names = m_reg.nodes_db.node.unique()
    indices_to_remove = [6,13,20,21] # remove the empty nodes that returns nonetype
    # Create a new array without the specified indices
    nodes_array = np.delete(node_names, indices_to_remove)
    # Initialize a dictionary to store median values
    estimated_peaks = {'node_name': [], 'mode': []}
    
    # Loop through each node and calculate the peak value
    for i in range(len(nodes_array)):
        node = str(nodes_array[i])
        node_trace = m_reg.nodes_db.node[node].trace()  # Access the trace of the specific node
        # Estimate bandwidth using Scott's rule of thumb
        bandwidth = 1.06 * np.std(node_trace) * len(node_trace)**(-0.2)

        # Fit KDE to the data
        kde = KernelDensity(bandwidth=bandwidth, kernel='gaussian')
        kde.fit(node_trace[:, np.newaxis])

        # Create points for the x-axis
        x = np.linspace(node_trace.min(), node_trace.max(), 1000)
        log_density = kde.score_samples(x[:, np.newaxis])

        # Find the value of the peak
        peak_value = x[np.argmax(log_density)]
        
        # print("Estimated peak value:", peak_value)
        
        estimated_peaks['node_name'].append(node)
        estimated_peaks['mode'].append(peak_value)

    # Create a DataFrame from the medians dictionary
    mode_df = pd.DataFrame(estimated_peaks)

# Save the DataFrame to a CSV file
    mode_df.to_csv(f'roi{roi}_mode.csv')