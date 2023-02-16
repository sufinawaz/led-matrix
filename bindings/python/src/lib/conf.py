import os

purpleAirHost = os.getenv('PURPLE_AIR_HOST')
weatherAppId = os.getenv('WEATHER_APP_ID')
mqttUsername = os.getenv('MQTT_USERNAME')
mqttPassword = os.getenv('MQTT_PASSWORD')
mqttTopic = os.getenv('MQTT_TOPIC')
mqttHost = os.getenv('MQTT_HOST')
mqttPort = os.getenv('MQTT_PORT')

path = '/home/pi/code/matrix/bindings/python/src'
gif = {'fireplace': f'{path}/images/gifs/fireplace.gif',
       'matrix': f'{path}/images/gifs/matrix.gif',
       'nebula': f'{path}/images/gifs/nebula.gif',
       'hyperloop': f'{path}/images/gifs/hyperloop.gif',
       'spacetravel': f'{path}/images/gifs/spacetravel.gif',
       'retro': f'{path}/images/gifs/retro.gif'}
purpleLogo = f'{path}/images/purple.jpg'
woodMistryLogo = f'{path}/images/wm.jpg'
mosqueLogo = f'{path}/images/mosque.jpg'
#mosqueLogo = f'{path}/images/islamic.png'

prayer_names = 'Fajr', 'Zuhr', 'Asr', 'Magh', 'Isha'
