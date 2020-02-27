#!/usr/bin/env python3

import ms5837
import time

sensor = ms5837.MS5837_30BA()
sensor.init()
while True:
    sensor.read()
    print(sensor.depth() -0.45 )
    time.sleep(0.5)
