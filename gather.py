#!/usr/bin/python3

from Simulation import Simulation
# from Sensor import Sensor
# from Solenoid import Solenoid
from network import Model
from Experiences import Experiences
from Settings import Settings

import time
import numpy as np
import random
import math

sensor = solenoid = simulation = Simulation.init()
# sensor = Sensor()
# solenoid = Solenoid()
experiences = Experiences()

print('experiences ', len(experiences.get()))

target = Settings.getTargetC()
target_delta = Settings.getTargetDelta()
temperature, humidity, timestamp = sensor.gather()
experiences.add(temperature, humidity, solenoid.on, timestamp, target, target_delta)
experiences.add(temperature, humidity, solenoid.on, timestamp, target, target_delta)
experience = experiences.getLast()
state = experience.state0
action = 0

while True:
    
    simulation.step()

    experience = experiences.getLast()
    state = experience.state0
    if random.random() < 0.6:
        action = 0
    else:
        action = 1

    force = False
    if temperature < target - target_delta:
        action = 1
        force = True
    elif temperature > target + target_delta:
        action = 0
        force = True

    if action == 0:
        solenoid.switchOff()
    else:
        solenoid.switchOn()

    temperature, humidity, timestamp = sensor.gather()
    if not force:
        experiences.add(temperature, humidity, solenoid.isOn(), timestamp, target, target_delta)

    target = Settings.getTargetC()
    target_delta = Settings.getTargetDelta()

    print(temperature * 9 / 5 + 32, state, action, experience.value)
    