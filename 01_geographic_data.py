# %%
import pandas as pd
import shapely
import geopandas as gpd
from pathlib import Path

# %%
pd.set_option('display.max_rows', 8)

# %%
path = Path('C:/Users/ferna/Downloads/geocompx-geocompy-e3c5197/data/')
world = gpd.read_file(path / 'world.gpkg')

# %%
type(world) # geopandas.geodataframe.GeoDataFrame

# %%
world.shape # (177, 11)

# %%
world[['name_long', 'geometry']]