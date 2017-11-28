#!/usr/bin/python3

import time
import numpy as np
import math

# from Sensor import Sensor
# from Solenoid import Solenoid
from Simulation import Simulation

from network import DQN
from Experiences import Experiences
from Settings import Settings


sensor = solenoid = Simulation()
# sensor = Sensor()
# solenoid = Solenoid()
experiences = Experiences()
dqn = DQN(4, 2)

target = Settings.getTargetC()
target_delta = Settings.getTargetDelta()
temperature, humidity, timestamp = sensor.gather()
experiences.add(temperature, humidity, solenoid.isOn(), timestamp, target, target_delta)
experience = experiences.getLast()
action = 0

while True:

    # experience = experiences.getLast()
    # state = experience.state0
    # actions = dqn.run([state])
    # action = np.argmax(actions)

    if temperature < target - target_delta:
        action = 1
    elif temperature > target + target_delta:
        action = 0

    if action == 0:
        solenoid.switchOff()
    else:
        solenoid.switchOn()

    temperature, humidity, timestamp = sensor.gather()
    experiences.add(temperature, humidity, solenoid.isOn(), timestamp, target, target_delta)
    print(temperature * 9 / 5 + 32, humidity, action, timestamp)

    target = Settings.getTargetC()
    target_delta = Settings.getTargetDelta()
    
    time.sleep(5)