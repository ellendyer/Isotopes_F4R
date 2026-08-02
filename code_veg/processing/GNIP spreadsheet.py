import pandas as pd
import datetime as dt
from matplotlib import pyplot as plt
#define the file location and name
location = "/Users/ellendyer/Documents/GitHub/Isotopes_F4R/code_veg/processing/" 
GNIP_sheet1= location + "GNIP_H2.xlsx"

#load data - Note:  We cannot open the file if it is open elsewhere, like in excel
GNIP_df1 = pd.read_excel(GNIP_sheet1)

#tansform the date column into a datetime 
GNIP_df1['Sample Date'] = pd.to_datetime(GNIP_df1['Sample Date'])

#this is a work around - .dt does not work...dunno why.  Version too old? 1.5.1
GNIP_df1['year'] = GNIP_df1['Sample Date'].apply(lambda x:x.year)
print(GNIP_df1['year'])

#Finding all the sites name.  Transforming into a set to remove duplicate
sites=GNIP_df1['Sample Site Name']
sites = set(sites)

for site in sites:
    site_df = GNIP_df1.loc[GNIP_df1['Sample Site Name']==site]
    df_1990 = site_df.loc[site_df['year']>=1990]
    plt.scatter(df_1990['Sample Date'],df_1990['Measurand Amount'],label =site)

plt.legend()
plt.show()

GNIP_subset = GNIP_df1.loc[(GNIP_df1.Latitude>-5)&(GNIP_df1.Latitude<5)&(GNIP_df1.Longitude>15)&(GNIP_df1.Longitude<31)]
print(GNIP_subset['Measurand Amount'].mean())
print(GNIP_subset['Measurand Amount'].max())
