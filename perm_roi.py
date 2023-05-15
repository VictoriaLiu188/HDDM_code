import sklearn.model_selection
from sklearn.model_selection import permutation_test_score
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
import scipy.stats
# from scipy.stats import permutation_test
import random

df_orig = pd.read_csv('/data2/victoria/brain_data/brain_behav_late_learn.csv')
# df = df_orig.loc[:,['sbj','correct','rt','trial','run','type','learner','roi1']]
# df.columns = ('subj_idx','response','rt','trial','run','type','learner','roi1')
df = df_orig
df.rt = df.rt/1000
df = hddm.utils.flip_errors(df)
df = df.dropna()
roi_df = df.iloc[:,-108:]
behave_df =df.iloc[:,1:17]

roi_ls = [41]
for i in range(0,500):
    num_row = 0
    behav_shu = pd.DataFrame()
    for p in range(100,143):
        if p in behave_df['sbj'].values:
            subj_df = behave_df[behave_df['sbj']== p] #identify each subject and put into a smaller df
            nrow= len(subj_df)
            count_5 = subj_df['run'].value_counts()[5]
            count_6 = subj_df['run'].value_counts()[6]
            run_5 = [5] * count_5
            run_6 = [6] * count_6
            new_run = run_5 + run_6
            rand_5 = random.sample(range(1,count_5+1),count_5)
            rand_6 = random.sample(range(1,count_6+1),count_6)
            rand_int = rand_5 + rand_6
            subj_df['runtrial'] = rand_int
            subj_df['run'] = new_run
            subj_sorted = subj_df.sort_values(by=['run', 'runtrial'])
            behav_shu = pd.concat([behav_shu,subj_sorted], axis=0) # concat dfs vertically
    behav_shu = behav_shu.reset_index(drop=True)
    roi_df = roi_df.reset_index(drop=True)
    df_shu = pd.concat([behav_shu,roi_df], axis=1)
    for roi in roi_ls:
        m_reg = hddm.HDDMRegressor(df_shu,f"v ~ roi{roi} * C(type,Treatment('prototype'))",
                                p_outlier=0.05)  
        m_reg.sample(2000, burn=1000)
        print("DIC value: {}\n".format(m_reg.dic))
        