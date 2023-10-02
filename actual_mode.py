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
from scipy import stats
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
late_learn = df[df['run'].isin([5, 6])].copy()


roi_ls = [1,2,51,52,53,14,15,16,17,18,20,23,24,25,65,67,68,70,74,77,31,32,33,34,35,38,39,40,41,42,43,44,48,80,82,83,88,90,91,92,93,94] # only DMN regions this time

for i in range(len(roi_ls)):
    roi = roi_ls[i]
    m_reg = hddm.HDDMRegressor(late_learn, [f"v ~ roi{roi} * C(type,Treatment('prototype'))", \
                                        f"a ~ roi{roi} * C(type,Treatment('prototype'))",\
                                        f"t ~ roi{roi}* C(type,Treatment('prototype'))"],
                                    p_outlier=0.05)  
    m_reg.find_starting_values()
    m_reg.sample(2000, burn=1000)
    x_min = min(late_learn[f'roi{roi}'])
    x_max= max(late_learn[f'roi{roi}'])
    x = np.linspace(x_min, x_max, 20)
    x_2d = x[:, np.newaxis]
    
    ################### calculate Threshold actual values ###########################
    a_Intercept = m_reg.nodes_db.node["a_Intercept"]
    a_roi = m_reg.nodes_db.node[f"a_roi{roi}"]
    a_exception = m_reg.nodes_db.node["a_C(type, Treatment('prototype'))[T.exception]"]
    a_rf = m_reg.nodes_db.node["a_C(type, Treatment('prototype'))[T.rule follower]"]
    a_roi_exception = m_reg.nodes_db.node[f"a_roi{roi}:C(type, Treatment('prototype'))[T.exception]"]
    a_roi_rulefollower = m_reg.nodes_db.node[f"a_roi{roi}:C(type, Treatment('prototype'))[T.rule follower]"]
    
    a_Prototype = x_2d * a_roi.trace() + a_Intercept.trace()    
    a_RuleFollower = a_rf.trace() + a_Intercept.trace() + x_2d * (a_roi.trace() + a_roi_rulefollower.trace())
    a_Exception= a_Intercept.trace() + a_exception.trace() + x_2d * (a_roi.trace() + a_roi_exception.trace())

    a_Prototype = a_Prototype.T
    a_RuleFollower = a_RuleFollower.T
    a_Exception = a_Exception.T
    
    # Calculate the median for each column
    medians_p = np.median(a_Prototype, axis=0)
    medians_rf = np.median(a_RuleFollower, axis=0)
    medians_e = np.median(a_Exception, axis=0)
    
    a_median_dict = {'a_proto': medians_p, 'a_rf': medians_rf, 'a_excep': medians_e}
    # Stack the matrices vertically
    stacked_matrix = np.vstack([matrix for matrix in a_median_dict.values()])

    # Create a DataFrame from the stacked matrix
    df = pd.DataFrame(stacked_matrix)
    # Save the DataFrame to a CSV file
    df.to_csv(f'a_ROI{roi}_medians.csv', index=False, header=False)  # Set header=False to omit column headers
    ################### calculate drift rate actual values ###########################
    v_Intercept = m_reg.nodes_db.node["v_Intercept"]
    v_roi = m_reg.nodes_db.node[f"v_roi{roi}"]

    v_exception = m_reg.nodes_db.node["v_C(type, Treatment('prototype'))[T.exception]"]
    v_rf = m_reg.nodes_db.node["v_C(type, Treatment('prototype'))[T.rule follower]"]
    v_roi_exception = m_reg.nodes_db.node[f"v_roi{roi}:C(type, Treatment('prototype'))[T.exception]"]
    v_roi_rulefollower = m_reg.nodes_db.node[f"v_roi{roi}:C(type, Treatment('prototype'))[T.rule follower]"]

    # putting it together 
    v_Prototype =  v_Intercept.trace() + x_2d * v_roi.trace()
    v_RuleFollower = v_rf.trace() + v_Intercept.trace() + x_2d * (v_roi.trace() + v_roi_rulefollower.trace())
    v_Exception= v_Intercept.trace() + v_exception.trace() + x_2d * (v_roi.trace() + v_roi_exception.trace())
    v_Prototype = v_Prototype.T
    v_RuleFollower = v_RuleFollower.T
    v_Exception = v_Exception.T

    medians_p = np.median(v_Prototype, axis=0)
    medians_rf = np.median(v_RuleFollower, axis=0)
    medians_e = np.median(v_Exception, axis=0)
    
    v_medians_dict = {'v_proto': medians_p, 'v_rf': medians_rf, 'v_excep': medians_e}
    # Stack the matrices vertically
    stacked_matrix = np.vstack([matrix for matrix in v_medians_dict.values()])

    # Create a DataFrame from the stacked matrix
    df = pd.DataFrame(stacked_matrix)
    # Save the DataFrame to a CSV file
    df.to_csv(f'v_ROI{roi}_medians.csv', index=False, header=False)  # Set header=False to omit column headers
################### calculate decision time actual values ###########################
    t_Intercept = m_reg.nodes_db.node["t_Intercept"]
    t_roi = m_reg.nodes_db.node[f"t_roi{roi}"]

    t_exception = m_reg.nodes_db.node["t_C(type, Treatment('prototype'))[T.exception]"]
    t_rf = m_reg.nodes_db.node["t_C(type, Treatment('prototype'))[T.rule follower]"]
    t_roi_exception = m_reg.nodes_db.node[f"t_roi{roi}:C(type, Treatment('prototype'))[T.exception]"]
    t_roi_rulefollower = m_reg.nodes_db.node[f"t_roi{roi}:C(type, Treatment('prototype'))[T.rule follower]"]

    # putting it together 
    t_Prototype =  t_Intercept.trace() + x_2d * t_roi.trace()
    t_RuleFollower = t_rf.trace() + t_Intercept.trace() + x_2d * (t_roi.trace() + t_roi_rulefollower.trace())
    t_Exception= t_Intercept.trace() + t_exception.trace() + x_2d * (t_roi.trace() + t_roi_exception.trace())
    t_Prototype = t_Prototype.T
    t_RuleFollower = t_RuleFollower.T
    t_Exception = t_Exception.T
    
    # plotting
    medians_p = np.median(t_Prototype, axis=0)
    medians_rf = np.median(t_RuleFollower, axis=0)
    medians_e = np.median(t_Exception, axis=0)
    
    
    t_medians_dict = {'t_proto': medians_p, 't_rf': medians_rf, 't_excep': medians_e}
    # Stack the matrices vertically
    stacked_matrix = np.vstack([matrix for matrix in t_medians_dict.values()])

    # Create a DataFrame from the stacked matrix
    df = pd.DataFrame(stacked_matrix)
    # Save the DataFrame to a CSV file
    df.to_csv(f't_ROI{roi}_medians.csv', index=False, header=False)  # Set header=False to omit column headers