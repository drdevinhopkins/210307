# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from datetime import date


# %%
old_weather = pd.read_csv('CYULweather.csv')
# old_weather.tail()


# %%
last_timestamp = pd.to_datetime(old_weather.tail(1).valid).tolist()[0]
# print(last_timestamp)


# %%
old_year = str(last_timestamp.date().year)
old_month = str(last_timestamp.date().month)
old_day = str(last_timestamp.date().day)
# print(old_year, old_month, old_day)

today = date.today()
today_year = str(today.year)
today_month = str(today.month)
today_day = str(today.day+1)
# print(today_year, today_month, today_day)


# %%
new_weather = pd.read_csv('https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?station=CYUL&data=all&year1='+old_year+'&month1='+old_month+'&day1='+old_day+'&year2=' +
                          today_year+'&month2='+today_month+'&day2='+today_day+'&tz=America%2FNew_York&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&direct=no&report_type=1&report_type=2')
# new_weather.tail()


# %%
concat_weather = pd.concat([old_weather, new_weather], ignore_index=True).drop_duplicates(
    subset='valid', keep='last')
# concat_weather.tail(50)


# %%
concat_weather.to_csv('CYULweather.csv', index=False)


# %%
