#!/usr/bin/python3

from network import DQN
from Simulation import Simulation
from Experiences import Experiences

import numpy as np
import random
import math

dqn = DQN(2, 2)

experiences = Experiences()
simulation = Simulation()

print('experiences ', len(experiences.get()))

iteration = 0
temperature, humidity, timestamp, value = simulation.step()
temperature_list = [temperature] * 2
state0 = list(temperature_list)

for iteration in range(270):

    actions = dqn.run([state0])
    if random.random() < 0.1:
        action = np.random.choice(2, 1)[0]
    else:
        action = np.argmax(actions)

    if action == 0:
        simulation.switchOff()
    else:
        simulation.switchOn()

    temperature, humidity, timestamp, value = simulation.step()

    del temperature_list[0]
    temperature_list.append(temperature)

    state1 = list(temperature_list)
    experiences.add(state0, state1, action, value)
    state0 = state1

    loss = dqn.train(experiences)
    print(state0, action, 'actions', actions, 'value', value, 'loss', loss)

    dqn.save()