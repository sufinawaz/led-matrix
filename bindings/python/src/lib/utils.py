from datetime import datetime, timedelta
import requests
import lib.conf as conf


def get_date_time(h24format=False, add_minutes=0):
    tm = datetime.now() + timedelta(minutes=add_minutes)
    return tm.strftime('%a'), \
           tm.strftime('%d'), \
           tm.strftime('%b'), \
           tm.strftime('%H:%M') if h24format else tm.strftime('%I:%M%p')[:-1].lower()


def color_intensity(value, highest=100, reverse=True):
    if value <= (highest / 2):
        r = 255
        g = int(255 * value / (highest / 2))
        b = 0
    else:
        r = int(255 * (highest - value) / (highest / 2))
        g = 255
        b = 0
    if reverse:
        r, g = g, r
    return [r, g, b]


def get_openweather_data():
    print('fetching openweathermap data')
    try:
        r = requests.get(
            f'https://openweathermap.org/data/2.5/weather?id=4791160&appid={conf.weatherAppId}&units=imperial',
            headers={'Accept': 'application/json'})
        j = r.json()
        current = f"{round(j['main']['temp'])}°"
        lowest = str(round(j['main']['temp_min']))
        highest = str(round(j['main']['temp_max']))
        icon = f"{conf.path}/images/weather-icons/{j['weather'][0]['icon']}.jpg"
        return current, lowest, highest, icon
    except:
        return None, None, None, None


def get_purple_data():
    print('fetching purple data')
    r = requests.get(f'http://{conf.purpleAirHost}/json?live=true',
                     headers={'Accept': 'application/json'})
    j = r.json()
    cha = j['pm2.5_aqi']
    chb = j['pm2.5_aqi_b']
    aqi = round(float(((cha + chb) / 2)), 1)
    pm1 = round(float((j['pm1_0_cf_1'] + j['pm1_0_cf_1_b']) / 2), 1)
    pm25 = round(float((j['pm2_5_cf_1'] + j['pm2_5_cf_1_b']) / 2), 1)
    return aqi, pm1, pm25


def get_prayer_times():
    print('fetching prayer times')
    r = requests.get('http://api.aladhan.com/v1/timings?latitude=38.903481&longitude=-77.262817&method=1&school=1',
                     headers={'Accept': 'application/json'})
    j = r.json()
    timings = j['data']['timings']
    fajr, dhuhr, asr, maghrib, isha = timings['Fajr'], timings['Dhuhr'], timings['Asr'], timings['Maghrib'], timings[
        'Isha']
    return fajr, dhuhr, asr, maghrib, isha


def get_next_prayer_time(times):
    day, dt, mo, clk = get_date_time(True, 10)
    for i in range(5):
        if times[i] > clk:
            return times[i], conf.prayer_names[i]
    return times[0], conf.prayer_names[0]
