from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie

# Create your views here.
def name(request):
    return HttpResponse("mandakini")

@ensure_csrf_cookie
def cal(request):
    x = request.POST.get('n1')
    y = request.POST.get('n2')
    d={}
    try:
        t=int(x)+int(y)
        r=f"Addition of {x} & {y} = {t}"
        d={'total':r}
    except:
        pass


    return render(request,'test.html',d)

def bio(request):
    return render(request, 'biodata.html')


def timestampfilter(timestamp):
    from datetime import datetime,timezone
    #convert the timestamp to a utc datetime object
    dt_object_utc = datetime.fromtimestamp(timestamp)

    #separate the date and time
    just_date = dt_object_utc.date()
    just_time = dt_object_utc.time()

    return just_date,just_time

def get_compass_direction(degrees):
    # Ensure the angle is within the 0-359.99 range
    degrees %= 360
    
    # 16 points mean each sector covers 22.5 degrees (360 / 16)
    directions = [
        "North", "North-Northeast", "Northeast", "East-Northeast",
        "East", "East-Southeast", "Southeast", "South-Southeast",
        "South", "South-Southwest", "Southwest", "West-Southwest",
        "West", "West-Northwest", "Northwest", "North-Northwest"
    ]
    
    # Calculate index by dividing by 22.5 and rounding to the nearest integer
    # Using modulo 16 ensures that angles near 360 (like 355) wrap back to 0 (North)
    index = int((degrees / 22.5) + 0.5) % 16
    
    return directions[index]



def weatherdata(request):
    import requests as rq

    api_key='2784f132116e985f08a7aed238633c09'
    city_name= request.GET.get("city")
    print(city_name)                       #input('Enter city name :')
    try:
        url='https://api.openweathermap.org/data/2.5/weather?q='+city_name+'&appid='+api_key
        data=rq.get(url).json()
        

        w=data['weather']
        w1 = w[0]
        des =w1['description']
        icon =w1['icon']
        

        m = data['main']
        temp = round(m['temp']-273,2)
        temp_max=round(m['temp_max'] -273,2)
        temp_min = round(m['temp_min']-273,2)
        feels_like = round(m['feels_like']-273,2)
        pres = m['pressure']
        hum = m['humidity']
        

        wd=data['wind']
        spd = wd['speed']
        deg=wd['deg']
        direction = get_compass_direction(deg)
        print(direction)

        cl = data['clouds']
        cloud = cl['all']

        dt=data['dt']
        date,time = timestampfilter(dt)
        print(date,time)

        sys = data['sys']
        country = sys['country']
        sunrise = sys['sunrise']
        sunset = sys['sunset']
        sunrise_t,x = timestampfilter(sunrise)
        sunset_t ,y= timestampfilter(sunset)

        image_url = f"https://openweathermap.org/img/wn/{icon}@4x.png"
        print(image_url)

        
        
        data={"city":city_name.upper,
              "temp":temp,
              'temp_max': temp_max,
              'temp_min':temp_min,
              'feels_like': feels_like,
              'des': des,
              'speed':spd,
              'humidity':hum,
              'pressure':pres,
              'cloud':cloud,
              'direction':direction,
              'sunrise':sunrise_t,
              'sunset':sunset_t,
              'date':date,
              'time':time,
              'iconurl':image_url,

              #dynamic sun cycle timestamps
              'sunrise_ts':int(sunrise),
              'sunset_ts':int(sunset),
              'current_ts':int(dt),
              }
        
    except Exception as e:
        print('error: ',e)    
        return render(request,'weather.html')
    return render(request,'weather.html',data)