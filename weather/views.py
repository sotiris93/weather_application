from django.shortcuts import redirect, render
import requests
from .models import City
from .forms import Cityform
from django.shortcuts import redirect
from datetime import datetime

def home(request):

    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={API KEY}&units=metric&lang=en'
    
    err_message=''
    message = ''
    message_notification = ''
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")


    if request.method =='POST':
        form = Cityform(request.POST)

        if form.is_valid():
            new_name= form.cleaned_data['name']
            existing = City.objects.filter(name=new_name).count()
            if existing ==0:
                r = requests.get(url.format(new_name)).json()
                if r['cod']==200:
                    form.save()
                else:
                    err_message = 'City does not exist'
            else:
                err_message='City already exists'
        if err_message:
            message = err_message
            message_notification = 'is-warning'
        else:
            message = 'City added successfully'
            message_notification = 'is-success'

    form = Cityform()
    Cities = City.objects.all()
    data= []

    
    for city in Cities:

        r= requests.get(url.format(city)).json()
            
        weather_info={
                'city': city,
                'temperature': r['main']['temp'],
                'feels_like': r['main']['feels_like'],
                'humidity': r['main']['humidity'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
                'wind_speed': r['wind']['speed'],
                'cloudiness': r['clouds']['all'],
                'visibility': r['visibility'],
                'country': r['sys']['country'],
                
                }
        data.append(weather_info)
    
    
    context = {'data': data,
                'form':form,
                 'message':message,
                  'message_notification':message_notification,
                  'date_time' : date_time,
                  }
    return render(request, 'weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
