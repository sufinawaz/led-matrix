#!/usr/bin/env python
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import paho.mqtt.client as mqttClient
from samplebase import SampleBase
from queue import Queue
from time import sleep, perf_counter, strftime, localtime
import threading
from PIL import Image, ImageSequence, GifImagePlugin
from lib.utils import get_date_time, color_intensity, get_purple_data, get_openweather_data, get_next_prayer_time, \
    get_prayer_times
import os
import lib.conf as conf

import logging
from systemd.journal import JournaldLogHandler

logger = logging.getLogger(__name__)
journald_handler = JournaldLogHandler()
journald_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(journald_handler)
logger.setLevel(logging.DEBUG)

print(f"2loaded conf {conf.mqttPort}  {conf.path}")

mqttHost = os.getenv('MQTT_HOST')
mqttPort = os.getenv('MQTT_PORT')

print(f"3loaded conf {mqttPort}  {mqttHost}")

client = mqttClient.Client()
fontSmall = graphics.Font()
font = graphics.Font()
Connected = False
new_line = '\n'
q = Queue()

fontSmall.LoadFont("/home/pi/code/matrix/fonts/4x6.bdf")
font.LoadFont("/home/pi/code/matrix/fonts/7x13.bdf")


def render_purple_data(self, canvas, aqi, pm1, pm25):
    c1 = color_intensity(aqi)
    c2 = color_intensity(pm1, 100)
    c3 = color_intensity(pm25, 100)
    graphics.DrawText(canvas, font, 5, 12, graphics.Color(c1[0], c1[1], c1[2]), str(aqi))
    graphics.DrawText(canvas, fontSmall, 5, 21, graphics.Color(255, 255, 255), "PM1")
    graphics.DrawText(canvas, fontSmall, 20, 21, graphics.Color(c2[0], c2[1], c2[2]), str(pm1))
    graphics.DrawText(canvas, fontSmall, 5, 31, graphics.Color(255, 255, 255), "PM2.5")
    graphics.DrawText(canvas, fontSmall, 28, 31, graphics.Color(c3[0], c3[1], c3[2]), str(pm25))
    return self.matrix.SwapOnVSync(canvas)


def on_message(client, userdata, msg):
    message = msg if isinstance(msg, str) else str(msg.payload.decode("utf-8"))
    val = None if isinstance(msg, str) else msg.payload
    print(f"onMessage received: {message}, value {val}")
    q.put(message)
    run_text = RunText()
    if not run_text.process():
        run_text.print_help()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        logger.info('Connected to broker')
        global Connected
        Connected = True
    else:
        print("Connection failed")
        logger.info('Connection failed')


class RunText(SampleBase):
    image = None

    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def run(self):
        message = q.get()
        if not message:
            return
        canvas = self.matrix.CreateFrameCanvas()
        if message == 'AQI':
            thread1 = threading.Thread(target=display_purple, args=(self, canvas))
            thread1.start()
        elif message == 'clock':
            thread1 = threading.Thread(target=display_clock_weather, args=(self, canvas))
            thread1.start()
        elif message == 'fireplace':
            thread1 = threading.Thread(target=display_fireplace, args=(self, canvas))
            thread1.start()
        elif message == 'random':
            display_hmarquee(self, canvas, message)
        elif message == 'prayer':
            thread1 = threading.Thread(target=display_prayer_times, args=(self, canvas))
            thread1.start()
        else:
            display_hmarquee(self, canvas, message)


def display_purple(self, canvas):
    aqi, pm1, pm25 = get_purple_data()
    canvas.Clear()
    self.image = Image.open(f'{conf.path}/images/purple.jpg').convert('RGB')
    self.image.thumbnail((24, 24), Image.ANTIALIAS)
    canvas.SetImage(self.image, 40, 2, False)
    canvas = render_purple_data(self, canvas, aqi, pm1, pm25)
    start_time = perf_counter()
    while True:
        now = perf_counter()
        if (now - start_time) > 15:
            canvas.Clear()
            start_time = now
            canvas.SetImage(self.image, 40, 2, False)
            aqi, pm1, pm25 = get_purple_data()
            canvas = render_purple_data(self, canvas, aqi, pm1, pm25)
        if not q.empty():
            return


def display_prayer_times(self, canvas):
    times = get_prayer_times()
    next_prayer_time, prayer = get_next_prayer_time(times)
    canvas.Clear()
    # self.image = Image.open(f'{path}/images/purple.jpg').convert('RGB')
    # self.image.thumbnail((24, 24), Image.ANTIALIAS)
    print('get_next_prayer_time', next_prayer_time)
    while True:
        canvas.Clear()
        # canvas.SetImage(self.image, 40, 2, False)
        graphics.DrawText(canvas, font, 5, 12, graphics.Color(255, 255, 255), str(next_prayer_time))
        # graphics.DrawText(canvas, fontSmall, 5, 21, graphics.Color(255, 255, 255), str(isha))
        canvas = self.matrix.SwapOnVSync(canvas)
        if not q.empty():
            return


def display_clock_weather(self, canvas):
    day, dt, mo, clk = get_date_time()
    times = get_prayer_times()
    next_prayer_time, prayer = get_next_prayer_time(times)
    # preload calendar and date while weather data loads
    graphics.DrawText(canvas, fontSmall, 3, 6, graphics.Color(173, 255, 47), day)
    graphics.DrawText(canvas, fontSmall, 20, 6, graphics.Color(173, 255, 47), dt)
    graphics.DrawText(canvas, fontSmall, 30, 6, graphics.Color(255, 255, 0), mo)
    # date
    graphics.DrawText(canvas, font, 3, 18, graphics.Color(255, 255, 255), clk)
    canvas = self.matrix.SwapOnVSync(canvas)
    # (slow) fetch weather data
    current, lowest, highest, icon = get_openweather_data()
    if icon:
        self.image = Image.open(icon).convert('RGB')
        self.image.thumbnail((24, 24), Image.ANTIALIAS)
    start_time = perf_counter()
    while True:
        now = perf_counter()
        if (now - start_time) > 600:
            next_prayer_time, prayer = get_next_prayer_time(times)
            c, l, h, i = get_openweather_data()
            if c and l and h and i:
                current, lowest, highest, icon = c, l, h, i
                self.image = Image.open(icon).convert('RGB')
                self.image.thumbnail((24, 24), Image.ANTIALIAS)
        canvas.Clear()
        day, dt, mo, clk = get_date_time()
        # weather icon
        if self.image:
            canvas.SetImage(self.image, 44, -4, False)
        # calendar
        graphics.DrawText(canvas, fontSmall, 3, 6, graphics.Color(173, 255, 47), day)
        graphics.DrawText(canvas, fontSmall, 20, 6, graphics.Color(173, 255, 47), dt)
        graphics.DrawText(canvas, fontSmall, 30, 6, graphics.Color(255, 255, 0), mo)
        # clock
        graphics.DrawText(canvas, font, 3, 18, graphics.Color(255, 255, 255), clk)
        # weather
        if current and highest and lowest:
            graphics.DrawText(canvas, font, 42, 30, graphics.Color(135, 206, 235), current)
            graphics.DrawText(canvas, fontSmall, 28, 25, graphics.Color(255, 114, 118), highest)
            graphics.DrawText(canvas, fontSmall, 28, 31, graphics.Color(173, 216, 230), lowest)
        # prayer
        graphics.DrawText(canvas, fontSmall, 5, 25, graphics.Color(150, 150, 150), str(prayer))
        graphics.DrawText(canvas, fontSmall, 5, 31, graphics.Color(30, 144, 255), str(next_prayer_time))
        canvas = self.matrix.SwapOnVSync(canvas)
        if not q.empty():
            return


def display_fireplace(self, canvas):
    self.image = Image.open(conf.fireplace)
    while True:
        for frame in range(self.image.n_frames):
            canvas.Clear()
            self.image.seek(frame)
            canvas.SetImage(self.image.convert('RGB'), 0, 0, False)
            canvas = self.matrix.SwapOnVSync(canvas)
            sleep(0.1)
            if not q.empty():
                canvas.Clear()
                return


def display_hmarquee(self, canvas, message):
    pos = canvas.width
    while True:
        canvas.Clear()
        len = graphics.DrawText(canvas, font, pos, 20, graphics.Color(255, 255, 255), message)
        pos -= 1
        if pos + len < 0:
            break
        sleep(0.02)
        canvas = self.matrix.SwapOnVSync(canvas)


client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=conf.mqttUsername, password=conf.mqttPassword)
client.connect(conf.mqttHost, port=int(conf.mqttPort))
client.loop_start()

if __name__ == "__main__":
    try:
        while not Connected:
            sleep(0.1)
        client.subscribe(conf.mqttTopic)
        on_message(None, None, 'clock')
        # on_message(None, None, {'payload': 'clock'})
        while True:
            sleep(1)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()
