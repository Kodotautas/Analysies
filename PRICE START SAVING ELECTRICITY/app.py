import os
from pstats import Stats
import pandas as pd
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats

#get the path of the current directory
cwd = os.getcwd()

#read xlsx file
df = pd.read_excel(f'{cwd}\data\da_and_load.xlsx')

#convert to datatime
df['datetime'] = pd.to_datetime(df['datetime'])

#get hour
df['hour'] = df['datetime'].dt.hour

#leave largest TOP 10% NP_price
percentile = df['NP_price'].quantile(0.1)
df = df[df['NP_price'] >= percentile]

#isin hour not night
df = df[df['hour'].isin([8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])]

#leave only rows previous_hour_change < 0 and next_hour_change > 0
df = df[(df['previous_hour_change'] < 0) & (df['next_hour_change'] > 0)]

#absolute value of previous_hour_change
df['previous_hour_change'] = df['previous_hour_change'].abs()

#average difference between previous_hour_change and next_hour_change
df['average_change'] = (df['previous_hour_change'] + df['next_hour_change']) / 2 * 100

# --------------------------------- PLOTTING --------------------------------- #
#scatter plot NP_price and average_change
plt.style.use("grayscale")

fig, ax = plt.subplots(figsize=(8,8))
ax.set_title("TOP 10% highest LT DA electricity prices \n & average change relationship \n (2021-2022.08.23)", fontsize=19)
ax.xaxis.tick_bottom()
ax.xaxis.set_label_position('bottom')
ax = sns.scatterplot(x='average_change', y='NP_price', data=df, ax=ax,
                    cmap='Spectral')
ax.set_ylabel('Day-ahead price, €/MWh', fontsize=18)
ax.set_xlabel('Average consumption change next hour, %', fontsize=18)
#add trendline
slope, intercept, r_value, p_value, std_err = stats.linregress(df['average_change'], df['NP_price'])
x = np.linspace(df['average_change'].min(), df['average_change'].max(), 100)
y = slope * x + intercept
ax.plot(x, y, 'r-', linewidth=2)
#value of p-value
ax.text(0.05, 0.95, f'p-value: {p_value:.2f}', transform=ax.transAxes, fontsize=18, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.savefig('NP_price_and_average_change_trendline.jpg', dpi=800, bbox_inches='tight')
plt.show()