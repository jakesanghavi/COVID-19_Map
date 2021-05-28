import cartopy.crs as crs
import cartopy.feature as cf
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import cartopy.feature as cfeature
from matplotlib.colors import LinearSegmentedColormap, DivergingNorm
import os
import matplotlib.animation as anim

plt.rcParams["font.family"] = "serif"

logos = os.listdir(os.getcwd() + '/csse_covid_19_time_series')

wd_data = pd.read_csv(os.getcwd() + '/csse_covid_19_time_series/' + str(logos[5]))
wc_data = pd.read_csv(os.getcwd() + '/csse_covid_19_time_series/' + str(logos[3]))
usd_data = pd.read_csv(os.getcwd() + '/csse_covid_19_time_series/' + str(logos[6]))
usc_data = pd.read_csv(os.getcwd() + '/csse_covid_19_time_series/' + str(logos[4]))
wc_data = wc_data.loc[wc_data['Country/Region'] != 'US']
wd_data = wd_data.loc[wd_data['Country/Region'] != 'US']
usc_data = usc_data.drop(columns=['UID', 'iso2', 'iso3', 'code3', 'code3', 'FIPS', 'Admin2', 'Combined_Key'])
usd_data = usd_data.drop(columns=['UID', "iso2", "iso3", "code3", "code3", "FIPS", "Admin2", "Combined_Key"])
wc_data.rename(columns = {'Province/State':'Province_State', 'Country/Region':'Country_Region', 'Long':'Long_'}, inplace = True)
wd_data.rename(columns = {'Province/State':'Province_State', 'Country/Region':'Country_Region', 'Long':'Long_'}, inplace = True)

final_c = usc_data
final_d = usd_data

long_list = np.arange(-179.5, 180, 1)
lat_list = np.arange(-89.5, 90, 1)
proj = crs.PlateCarree(central_longitude=0)

cmap = plt.get_cmap('YlOrRd')

# Norm for ratio of deaths
norm = DivergingNorm(vcenter=0.055)

fig = plt.figure()

i = 1

time = final_c.columns.tolist()
time.remove("Province_State")
time.remove("Country_Region")
time.remove("Long_")
time.remove("Lat")


def update(i):
        plt.clf()
        ax = plt.axes(projection=proj)

        ax.set_title('US COVID-19 Progression (Author: Jake Sanghavi)\n' + str(time[i]), fontsize=10)
        ax.add_feature(cf.COASTLINE, alpha=0.7)
        ax.add_feature(cfeature.LAND, facecolor='0.25')
        ax.add_feature(cfeature.BORDERS, zorder=10, alpha=0.7)
        ax.set_extent([-125, -66.5, 24, 50], crs.PlateCarree())
        states_provinces = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='50m',
            facecolor='none')
        ax.add_feature(states_provinces, edgecolor='black')
        ax.add_feature(cfeature.OCEAN, color='navy', alpha=0.5)
        ax.add_feature(cfeature.LAKES, color='mediumblue', alpha=0.2)
        ax.scatter(x=final_c['Long_'],
                   y=final_c['Lat'],
                   s=final_c[str(time[i])].astype(float)/1000,
                   c=final_d[str(time[i])].astype(float)/final_c[str(time[i])].astype(float),
                   cmap=cmap, norm=norm)
        i += 1


ani = anim.FuncAnimation(fig, update, frames=len(time), interval=200)

writerg = anim.FFMpegWriter(fps=10)
ani.save("us_covid_gif.mp4", writer=writerg)
