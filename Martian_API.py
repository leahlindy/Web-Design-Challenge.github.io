#Dependancies
import matplotlib.pyplot as plt
import pandas as pd
import requests
from datetime import datetime
import seaborn as sns
sns.set(style="darkgrid")


# USE MARS INSIGHT PROJECT API TO CREATE DAILY WEATHER REPORT OF MARS 
# Documentation: https://api.nasa.gov/assets/insight/InSight%20Weather%20API%20Documentation.pdf

from api_key import nasa_key
nasa_key
base_url ='https://api.nasa.gov/insight_weather/?'
query_url = f'{base_url}api_key={nasa_key}&feedtype=json&ver=1.'

nasa_response = requests.get(query_url)
nasa_json=nasa_response.json()

sol_keys=nasa_json["sol_keys"]
print(f'A sol is a Martian day, the data has up to date information on the last {len(sol_keys)} Sols.')

#since only most recent 7 sol's are avaiable need to make the [sol] dynamic
#dynamic dates
sol_key=nasa_json["sol_keys"]
sol_list=[]
for sol in sol_key:
    sol_list.append(sol)

# Convert Martian date to earth date for all sol articles
date_list=[]
numerical_dates=[]

#format datas
for day in sol_list:
    utc_day=nasa_json[day]['First_UTC']
    utc=datetime.strptime(utc_day, '%Y-%m-%dT%H:%M:%SZ')
    date_formatted=utc.strftime("%d-%b-%Y")
    numeric_formatted = utc.strftime("%d-%m-%Y")
    date_list.append(date_formatted)
    numerical_dates.append(numeric_formatted)

# Metrics available for each Sol:
# Each sol has linear averages for Temperature (AT), horizontal wind speed (HWS) and atmostpheric pressure (PRE)
print(f'The Temperature of sol_1 is {nasa_json[sol_list[0]]["AT"]["av"]} F.')
print(f'The average horizontal windspeed of sol_1 is {nasa_json[sol_list[0]]["HWS"]["av"]} m/s.')
print(f'The average atmospheric pressure of sol_1 is {nasa_json[sol_list[0]]["PRE"]["av"]} Pa.')
# There is also a most common wind direction measure
print(f'wind direction: {nasa_json[sol_list[0]]["WD"]["most_common"]["compass_point"]}')


# iterate through each sol
try:
    for i in range(0,7):
        print(f'{date_list[i]}: \n AT: {nasa_json[sol_list[i]]["AT"]["av"]} F \n HWS: {nasa_json[sol_list[i]]["HWS"]["av"]} m/s \n PRE: {nasa_json[sol_list[i]]["PRE"]["av"]} Pa.')
except KeyError:
    pass

# Save result into variables for data frame
sol_variables = [sol_list[i] for i in range(0,7)]
date_variables = [date_list[i] for i in range(0,7)]
temp_variables = [nasa_json[sol_list[i]]["AT"]["av"] for i in range(0,7)]
HWS_variables = [nasa_json[sol_list[i]]["HWS"]["av"] for i in range(0,7)]
PRE_variables = [nasa_json[sol_list[i]]["PRE"]["av"] for i in range(0,7)]

mars_df=pd.DataFrame({'Sol':sol_variables,
                        'Date': date_variables,
                        'Average Temp':temp_variables,
                        'Horizontal Wind Speed':HWS_variables,
                         'Pressure':PRE_variables
                        })
#save table into html table format
mars_table= mars_df.to_html()

# Export the mars data into a .csv.
mars_df.to_csv('Resources/mars.csv', encoding='utf-8',index=False)

#use temperature to alter size of points
s= mars_df['Average Temp']

#plot each with matplot
fig = plt.figure()
ax = sns.scatterplot(x='Sol', y='Average Temp', size=s, sizes=(75, 200),data=mars_df)
ax.set_title('Avareage Temperature on Mars')
ax.set_xlabel('Sol (Martian Day)')
ax.set_ylabel('AT (F)')
fig.savefig('templates/Visualizations/AT.png')

fig = plt.figure()
ax = sns.scatterplot(x='Sol', y='Horizontal Wind Speed', size=s, sizes=(75, 200), legend=False,data=mars_df)
ax.set_title('Horizontal Wind Speed on Mars')
ax.set_xlabel('Sol (Martian Day)')
ax.set_ylabel('HWS (m/s)')
fig.savefig('templates/Visualizations/HWS.png')

fig = plt.figure()
ax = sns.scatterplot(x='Sol', y='Pressure', size=s, sizes=(75, 200), legend=False,data=mars_df)
ax.set_title('Atmospheric Pressure on Mars')
ax.set_xlabel('Sol (Martian Day)')
ax.set_ylabel('Pressure (Pa)')
fig.savefig('templates/Visualizations/Pressure.png')

mars_dropped=mars_df.drop(['Average Temp'], axis=1)

#a combined graph to show all metrics available on API
fig, ax1 = plt.subplots()
ax1.grid(b=None)

ax1.set_title('Weather on Mars')
ax1.set_ylabel('Horizontal Wind Speed')
ax1.bar(mars_dropped['Sol'], mars_dropped['Horizontal Wind Speed'], width=.4, color='green', label='HWS')
ax1.set_xlabel('Sol')
ax2=ax1.twinx()
ax2.bar(mars_dropped['Sol'], mars_dropped['Pressure'], align='edge',alpha=.5, width=.4, label='Pressure')
ax2.set_ylabel('Pressure')
ax2.grid(b=None)
ax3=ax1.twinx()
ax3.plot(mars_df['Sol'], mars_df['Average Temp'], c='black', label='Temp')
ax3.set_ylim(-62,-57)

fig.legend(loc='upper right')
fig.savefig('templates/Visualizations/combined.png')



