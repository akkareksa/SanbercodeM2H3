# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 21:26:08 2020

@author: Kevin
"""

import json
import pandas as pd
from sklearn import preprocessing
import seaborn as sns

df_id = pd.read_json('indo.json')
df_id = df_id[['Date','Cases']]

df_in = pd.read_json('india.json')
df_in = df_in[['Date','Cases']]

df_ch = pd.read_json('china.json')
df_ch = df_ch[['Date','Cases']]

df_us = pd.read_json('usa.json')
df_us = df_us[['Date','Cases']]

# Normalized Date

scaler = preprocessing.MinMaxScaler() 
#%%
line_id = df_id.plot.line(x='Date', y='Cases', title='Corona Case in Indonesia')
#%%
line_in = df_in.plot.line(x='Date', y='Cases', title='Corona Case in India')
#%%
line_ch = df_ch.plot.line(x='Date', y='Cases', title='Corona Case in China')
#%%
line_us = df_us.plot.line(x='Date', y='Cases', title='Corona Case in USA')
#%%
#Normalized Date

#create temporary dataframe for normalied data
tdf_id = df_id.copy()
tdf_in = df_in.copy()
tdf_ch = df_ch.copy()
tdf_us = df_us.copy()

#preprocessing date in temp df
tdf_id['Date'] = pd.to_datetime(df_id['Date']).astype('int64')
tdf_in['Date'] = pd.to_datetime(df_id['Date']).astype('int64')
tdf_ch['Date'] = pd.to_datetime(df_id['Date']).astype('int64')
tdf_us['Date'] = pd.to_datetime(df_id['Date']).astype('int64')

#normalized date from -1 to 1
max_a = tdf_id.Date.max()
min_a = tdf_id.Date.min()
min_norm = -1
max_norm =1

#create new colum for normalized date (-1 to 1) (OPTIONAL/ gk perlu sebenernya)
tdf_id['NDate'] = (tdf_id.Date- min_a) *(max_norm - min_norm) / (max_a-min_a) + min_norm
tdf_in['NDate'] = (tdf_in.Date- min_a) *(max_norm - min_norm) / (max_a-min_a) + min_norm
tdf_ch['NDate'] = (tdf_ch.Date- min_a) *(max_norm - min_norm) / (max_a-min_a) + min_norm
tdf_us['NDate'] = (tdf_us.Date- min_a) *(max_norm - min_norm) / (max_a-min_a) + min_norm

#make temporary dataframe only have Normalize date and Cases before normalized data
del tdf_id['Date']
del tdf_in['Date']
del tdf_ch['Date']
del tdf_us['Date']


#use temporary dataframe to fit transform (normalized data)
tdf_id = scaler.fit_transform(tdf_id)
tdf_in = scaler.fit_transform(tdf_in)
tdf_ch = scaler.fit_transform(tdf_ch)
tdf_us = scaler.fit_transform(tdf_us)

#create normalized df from temp df (numpy arr)
ndf_id = pd.DataFrame(tdf_id, columns=['Cases','Ndate'])
ndf_in = pd.DataFrame(tdf_in, columns=['Cases','Ndate'])
ndf_ch = pd.DataFrame(tdf_ch, columns=['Cases','Ndate'])
ndf_us = pd.DataFrame(tdf_us, columns=['Cases','Ndate'])

print(ndf_ch)

#give date atribute
ndf_id['Date'] = df_id['Date']
ndf_in['Date'] = df_in['Date']
ndf_ch['Date'] = df_ch['Date']
ndf_us['Date'] = df_us['Date']

#%%
nline_id = ndf_id.plot.line(x='Date', y='Cases', title='Normalized Corona Case in Indonesia')
#%%
nline_in = ndf_in.plot.line(x='Date', y='Cases', title='Normalized Corona Case in India')
#%%
nline_ch = ndf_ch.plot.line(x='Date', y='Cases', title='Normalized Corona Case in China')
#%%
nline_us = ndf_us.plot.line(x='Date', y='Cases', title='Normalized Corona Case in USA')
#%%
#compare all normalized data
cdf_id = ndf_id.copy()
cdf_id['Country'] = "Indonesia"

cdf_in = ndf_in.copy()
cdf_in['Country'] = "India"
cdf_ch = ndf_ch.copy()
cdf_ch['Country'] = "China"
cdf_us = ndf_us.copy()
cdf_us['Country'] = "USA"

cdf = cdf_id.append(cdf_in).append(cdf_ch).append(cdf_us)
cdf.reset_index(drop=True, inplace=True)

cdf['Newdate_temp'] = pd.to_datetime(cdf.Date)

plot = sns.lineplot(data=cdf, x='Date', y='Cases', hue='Country')
plot.set(xlabel='Date',ylabel= 'Cases')
# plot.set(xlabel='Date', ylabel='Case')
plot.set_xticklabels(labels=cdf['Date'].dt.strftime('%m/%d/%Y'), rotation=30)

# cline = cdf.pivot(index='Date', columns='country', values='Cases')1
