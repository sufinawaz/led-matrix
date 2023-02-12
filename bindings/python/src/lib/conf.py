import os

purpleAirHost = os.getenv('PURPLE_AIR_HOST')
weatherAppId = os.getenv('WEATHER_APP_ID')
mqttUsername = os.getenv('MQTT_USERNAME')
mqttPassword = os.getenv('MQTT_PASSWORD')
mqttTopic = os.getenv('MQTT_TOPIC')
mqttHost = os.getenv('MQTT_HOST')
mqttPort = os.getenv('MQTT_PORT')

path = '/home/pi/code/matrix/bindings/python/src'
fireplace = f'{path}/images/gifs/fireplace.gif'
purpleLogo = f'{path}/images/purple.jpg'
woodMistryLogo = f'{path}/images/wm.jpg'
mosqueLogo = f'{path}/images/mosque.jpg'

prayer_names = 'Fajr', 'Zuhr', 'Asr', 'Magh', 'Isha'
