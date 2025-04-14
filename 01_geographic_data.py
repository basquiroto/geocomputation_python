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

# %%
world[world['name_long'] == 'Brazil'].plot()

# %%
world.explore()

# %%
world.geometry.crs

# %%
world2 = world.copy()

# %%
world2.geometry = world.envelope
world2.plot()

# %%
world.geometry.type.value_counts()

# %%
world['bbox'] = world.envelope
world = world.set_geometry('bbox')

world.explore()

# %%
#world = world.set_geometry('geometry')
world.geometry.iloc[1]

# %%
world[world['name_long'] == 'Brazil'].geometry.iloc[0]

# %%
ponto = shapely.Point([5,2])
ponto

# %%
pnt_wkt = shapely.from_wkt('POINT(5 2)')
pnt_wkt

# %%
linha = shapely.LineString([(1,5), (4,4), (4,1), (2,3), (5,5)])
linha

# %%
poligono = shapely.Polygon(
    [(1,5), (2,2), (4,1), (4,4), (1,5)],
    [[(2,4), (3,4), (2,3), (2,3)],
     [(3,3), (3,2), (2,3), (3,3)]]  ## Hole(s)
)
poligono

# %%
multipoligono = shapely.MultiPolygon([
    [[(1,5), (2,2), (4,1), (4,4), (1,5)], [[(2,4), (3,4), (3,3), (2,3), (2,4)]]],  ## Polygon 1 
    [[(0,2), (1,2), (1,3), (0,3), (0,2)], []]   ## Polygon 2, etc.
])
multipoligono

# %%
multipoligono.buffer(0.2).difference(multipoligono)

# %%
list(poligono.exterior.coords)

# %%
lnd_point = shapely.Point(0.1, 51.5)

lnd_geom = gpd.GeoSeries([lnd_point], crs=4326)
lnd_geom

# %%
lnd_data = {
  'name': ['London'],
  'temperature': [25],
  'date': ['2023-06-21'],
  'geometry': lnd_geom
}

lnd_layer = gpd.GeoDataFrame(lnd_data)
lnd_layer

# %%
lnd_point = shapely.Point(0.1, 51.5)
paris_point = shapely.Point(2.3, 48.9)
towns_geom = gpd.GeoSeries([lnd_point, paris_point], crs=4326)
towns_data = {
  'name': ['London', 'Paris'],
  'temperature': [25, 27],
  'date': ['2013-06-21', '2013-06-21'],
  'geometry': towns_geom
}
towns_layer = gpd.GeoDataFrame(towns_data)
towns_layer

# %%
towns_layer.explore(color='red', marker_kwds={'radius': 10})

# %%
towns_table = pd.DataFrame({
  'name': ['London', 'Paris'],
  'temperature': [25, 27],
  'date': ['2017-06-21', '2017-06-21'],
  'x': [0.1, 2.3],
  'y': [51.5, 48.9]
})
towns_geom = gpd.points_from_xy(towns_table['x'], towns_table['y'])
towns_layer = gpd.GeoDataFrame(towns_table, geometry=towns_geom, crs=4326)

# %%
# linha.length
poligono.area

# %%
gpd.GeoSeries([linha, poligono]).area

# %%
world[world['name_long']=='Slovenia'].to_crs(32633).area

# %%
import numpy as np
import rasterio
import rasterio.plot

#%% 
src = rasterio.open('C:/Users/ferna/OneDrive/Área de Trabalho/qgis_visada/ARQUIVOS/RST/s29_w050_1arc_v3.tif')
src

# %%
rasterio.plot.show(src)

# %%
src.meta


# %%
src.read(1)

# %%
elev = np.arange(1, 37, dtype=np.uint8).reshape(6, 6)
elev

# %%
v = [
  1, 0, 1, 2, 2, 2, 
  0, 2, 0, 0, 2, 1, 
  0, 2, 2, 0, 0, 2, 
  0, 0, 1, 1, 1, 1, 
  1, 1, 1, 2, 1, 1, 
  2, 1, 2, 2, 0, 2
]
grain = np.array(v, dtype=np.uint8).reshape(6, 6)
grain

# %%
new_transform = rasterio.transform.from_origin(
    west=-1.5, 
    north=1.5, 
    xsize=0.5, 
    ysize=0.5
)
new_transform

# %%
rasterio.plot.show(elev);

# %%
rasterio.plot.show(elev, transform=new_transform);

# %%
rasterio.plot.show(grain, transform=new_transform);

# %%
new_dataset = rasterio.open(
    'C:/Users/ferna/OneDrive/Área de Trabalho/elev.tif', 'w', 
    driver='GTiff',
    height=elev.shape[0],
    width=elev.shape[1],
    count=1,
    dtype=elev.dtype,
    crs=4326,
    transform=new_transform
)
new_dataset.write(elev, 1)
new_dataset.close()

# %% 
import pyproj
epsg_codes = pyproj.get_codes('EPSG', 'CRS')  ## Supported EPSG codes
epsg_codes[:5]  ## Print first five supported EPSG codes

# %%
pyproj.CRS.from_epsg(4326)

# %%
zion = gpd.read_file('C:/Users/ferna/Downloads/geocompx-geocompy-e3c5197/data/zion.gpkg')
zion.crs

# %%
# WGS84
zion.to_crs(4326).plot(edgecolor='black', color='lightgrey').grid()
# NAD83 / UTM zone 12N
zion.plot(edgecolor='black', color='lightgrey').grid();