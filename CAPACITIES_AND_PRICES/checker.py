import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------------- DATA READING ------------------------------- #
#read dataset xlsx file
df = pd.read_excel('dataset.xlsx')

#datetime to to_datetime
df['datetime'] = pd.to_datetime(df['datetime'])

#choose columns
df = df[['Lithuania DA price', 'LT_WIND_FORECAST', 'SE4 > LT capacity', 'EE > LV capacity', 'PL > LT capacity', 'FI > EE capacity' , 'LV > LT capacity']]

#create mask
mask = np.triu(np.ones_like(df.corr(), dtype=np.bool))

#adjust mask
mask = mask[1:, :-1]
corr = df.corr().iloc[1:,:-1].copy()

#plot heatmap with seaborn
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(8,8))
ax.set_title("Lithuania electricity price correlation in 2022", fontsize=20)
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')
ax = sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', ax=ax, 
               cmap='Spectral', vmin=-1, vmax=1, cbar_kws={"shrink": .8}, 
               square=True, annot_kws={"size": 14})

#save figure with seaborn
plt.savefig('heatmap.jpg', dpi=200, bbox_inches='tight')
