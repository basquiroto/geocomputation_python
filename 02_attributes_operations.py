# %%
# https://py.geocompx.org/02-attribute-operations

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import rasterio

# %%
path = 'C:/Users/ferna/Downloads/geocompx-geocompy-e3c5197/'

world = gpd.read_file(path + 'data/world.gpkg')
src_elev = rasterio.open(path + 'output/elev.tif')
src_grain = rasterio.open(path + 'output/grain.tif')
src_multi_rast = rasterio.open(path + 'data/landsat.tif')

# %%
world.iloc[0:3, :] # implicit numpy index (start is inclusive and end exclusive)

# %%
world.loc[0:3, :] # pandas index (start and end are inclusive)

# %%
world.iloc[:, 0:3]

# %%
world.loc[:, 'name_long':'pop'] # world[['name_long', 'geometry']]

# %%
world.drop([2, 3, 5])
world.drop(['name_long', 'continent'], axis=1)

# %%
world[['name_long', 'pop']].rename(columns={'pop': 'population'})

# %%
idx_small = world['area_km2'] < 10000  ## a logical 'Series'
small_countries = world[idx_small]

# small_countries = world[world['area_km2'] < 10000]

small_countries

# %%
idx_small = world['area_km2'] < 10000
idx_asia = world['continent'] == 'Asia'
world.loc[idx_small & idx_asia, ['name_long', 'continent', 'area_km2']]

# %%
world[world['continent'] == 'Asia']  \
    .loc[:, ['name_long', 'continent']]  \
    .iloc[0:5, :]

# %%
world[
        (world['continent'] == 'North America') | 
        (world['continent'] ==  'South America')
    ]  \
    .loc[:, ['name_long', 'continent']]

# %%
world[world['continent'].isin(['North America', 'South America'])]  \
    .loc[:, ['name_long', 'continent']]

# %%

world_agg1 = world.groupby('continent')[['pop']].sum().reset_index()
world_agg1

# %%
world_agg2 = world[['continent', 'pop', 'geometry']] \
    .dissolve(by='continent', aggfunc='sum') \
    .reset_index()
world_agg2

# %%
fig, ax = plt.subplots(figsize=(6, 3))
world_agg2.plot(column='pop', edgecolor='black', legend=True, ax=ax);

# %%
world_agg3 = world.dissolve(
    by='continent', 
    aggfunc={
        'name_long': 'count',
        'pop': 'sum',
        'area_km2': 'sum'
    }).rename(columns={'name_long': 'n'}).reset_index()
world_agg3

#%%
# Summed population
fig, ax = plt.subplots(figsize=(5, 2.5))
world_agg3.plot(column='pop', edgecolor='black', legend=True, ax=ax);
# Summed area
fig, ax = plt.subplots(figsize=(5, 2.5))
world_agg3.plot(column='area_km2', edgecolor='black', legend=True, ax=ax);
# Count of countries
fig, ax = plt.subplots(figsize=(5, 2.5))
world_agg3.plot(column='n', edgecolor='black', legend=True, ax=ax);

# %%

world_agg4 = world_agg3.drop(columns=['geometry'])
world_agg4['density'] = world_agg4['pop'] / world_agg4['area_km2']
world_agg4 = world_agg4.sort_values(by='n', ascending=False)
world_agg4 = world_agg4.head(3)
world_agg4

# %%
coffee_data = pd.read_csv(path + 'data/coffee_data.csv')
coffee_data

# %%
world_coffee = pd.merge(world, coffee_data, on='name_long', how='left')
world_coffee

# %%
base = world_coffee.plot(color='white', edgecolor='lightgrey')
coffee_map = world_coffee.plot(ax=base, column='coffee_production_2017');

# %%
pd.merge(world, coffee_data, on='name_long', how='inner')

#%%
world2 = world.copy()
world2['pop_dens'] = world2['pop'] / world2['area_km2']
world2

# %%
world2['con_reg'] = world['continent'] + ':' + world2['region_un']
world2 = world2.drop(['continent', 'region_un'], axis=1)
world2

#%%
world2[['continent', 'region_un']] = world2['con_reg'] \
    .str.split(':', expand=True)
world2

#%%
world2.rename(columns={'name_long': 'name'})

# %%
new_names = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'geom', 'i', 'j', 'k', 'l']
world2.columns = new_names
world2  

# %%
names = sorted(world2.columns, reverse=True)
world2 = world2[names]
world2

# %%
world2 = world2.drop('geom', axis=1)
world2 = pd.DataFrame(world2)
world2

# %%
elev = src_elev.read(1)
elev

# %%
elev[1, 2] = 0
elev

# %%
elev[0, 0:3] = 0
elev

# %%
np.mean(elev)

# %%
plt.hist(elev.flatten());