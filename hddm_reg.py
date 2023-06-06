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




df_orig = pd.read_csv('/data2/victoria/brain_data/brain_behav_late_learn.csv')
# df = df_orig.loc[:,['sbj','correct','rt','trial','run','type','learner','roi1']]
# df.columns = ('subj_idx','response','rt','trial','run','type','learner','roi1')
df = df_orig
df.rt = df.rt/1000
df = hddm.utils.flip_errors(df)
df = df.dropna()
# df.head()


for i in range(1,109):
    m_reg = hddm.HDDMRegressor(df,f"v ~ roi{i} * C(type,Treatment('prototype'))",
                                p_outlier=0.05)  
    m_reg.find_starting_values()
    m_reg.sample(2000, burn=1000)
    m_reg.print_stats()