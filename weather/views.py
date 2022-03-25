import datetime
import itertools
import os
import pytz
import requests
from dateutil import tz
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CityForm
from pytz import timezone

def index(request):
    """Return the current and forecasted weather for a US zipcode."""

    def utc_to_local_time(date_time):
        """Convert utc to local time.

        A local time to convert to can be set in the to_zone variable.
        """
        from_zone = tz.tzutc()
        to_zone = tz.gettz('America/Los_Angeles')
        utc = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        utc_replace = utc.replace(tzinfo = from_zone)
        local_timezone = utc_replace.astimezone(to_zone)
        return str(local_timezone)

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid() == False:
            messages.error(request, 'Zip code must be 5 numbers long')
    else:
        form = CityForm()

    API_KEY = os.environ.get('API_KEY')
    
    url = 'http://api.openweathermap.org/data/2.5/weather?zip={},us&units=imperial&appid='+API_KEY
    form_zipcode = form['zipcode'].value()
    r = requests.get(url.format(form_zipcode)).json()
    # Clear the contents of the form after post request and return new form.
    form = CityForm()

    weather_data_current = {}

    if form_zipcode != None and len(form_zipcode) == 5:
        try:
            weather_data_current = {
            'city' : r['name'],
            'temperature' : round(r['main']['temp']),
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon']
            }
        except KeyError:
            messages.error(request, 'Please enter a valid zip code')

    weather_data_forecast = []

    if weather_data_current != {}:
        url_two = 'https://api.openweathermap.org/data/2.5/forecast?zip={}&units=imperial&appid='+API_KEY
        r_two = requests.get(url_two.format(form_zipcode)).json()

        index_count = 0
        data_forecast = []

        while index_count < len(r_two['list']):
            forecast_fields = {
            'date':utc_to_local_time(r_two['list'][index_count]['dt_txt'])[0:10],
            'temp_max':r_two['list'][index_count]['main']['temp_max'],
            'temp_min':r_two['list'][index_count]['main']['temp_min'],
            'icon':r_two['list'][index_count]['weather'][0]['icon'],
            'date_time':utc_to_local_time(r_two['list'][index_count]['dt_txt'])[11:19]}
            index_count += 1
            data_forecast.append(forecast_fields)

        def get_temp(temp):
            return temp['date']

        today_date = datetime.datetime.now(pytz.timezone('US/Pacific'))
        time_delta = datetime.timedelta(days=4)

        delta = today_date + time_delta

        grouping = itertools.groupby(data_forecast, get_temp)

        for key, group in grouping:
            if key > str(today_date) and key <= str(delta):
                groups = list(group)
                forecast_data = {}
                forecast_data['date'] = key
                forecast_data['temp_min'] = round(min(day['temp_min'] for day in groups))
                forecast_data['temp_max'] = round(max(day['temp_max'] for day in groups))
                forecast_data['icon'] = [day['icon'] for day in groups if day['date_time'] == '11:00:00'][0]
                forecast_data['day_name'] = datetime.datetime.strptime(key, '%Y-%m-%d').strftime('%A')
                weather_data_forecast.append(forecast_data)

    context = {
    'form': form, 'weather_data_current': weather_data_current, 'weather_data_forecast':weather_data_forecast}

    return render(request, 'index.html', context)

if __name__ == '__main__':
    index(request)
