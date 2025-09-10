#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Button, Stop
from pybricks.tools import wait
import random

# Criação dos objetos
ev3 = EV3Brick()

color_esquerda = ColorSensor(Port.S1)
color_direita = ColorSensor(Port.S2)

ref_esquerda = color_esquerda.reflection()
ref_direita = color_direita.reflection()

motor_esquerda = Motor(Port.A)
motor_direita = Motor(Port.B)

velocidade = 200
black = 8
white = 69
treshold = 0.1

def virar_direita(error):
    motor_esquerda.run(velocidade * error)
    motor_direita.run(-(velocidade * error) / 2)

def virar_esquerda(error):
    motor_esquerda.run(-(velocidade * -error) / 2)
    motor_direita.run(velocidade * -error)

def seguir_em_frente():
    motor_esquerda.run(velocidade)
    motor_direita.run(velocidade)


actions = ["forward", "left", "right"]
Q = {}
alpha, gamma, epsilon = 0.5, 0.8, 0.5  # hiperparâmetros

def get_state():
    l = 1 if color_esquerda.reflection() < 45 else 0
    r = 1 if color_direita.reflection() < 45 else 0
    erro = color_esquerda.reflection() - color_direita.reflection()
    return erro, l, r

def choose_action(state):
    if random.random() < epsilon or state not in Q:
        return random.choice(actions)
    return max(Q[state], key=Q[state].get)

def perform_action(action):
    if action == "forward":
        seguir_em_frente()
    elif action == "left":
        virar_esquerda(1)  # força de curva simplificada
    elif action == "right":
        virar_direita(1)
    wait(200)

def reward(state):
    erro, l, r = state
    if 0 <= abs(erro) <= 5 and (l == 1 or r == 1):   # dois sensores no preto
        return 5
    elif 6 <= abs(erro) <= 10:
        return 1
    else:
        return -5

# Loop principal
while True:
    state = get_state()
    action = choose_action(state)
    perform_action(action)
    new_state = get_state()
    r = reward(new_state)

    if state not in Q:
        Q[state] = {a: 0 for a in actions}
    if new_state not in Q:
        Q[new_state] = {a: 0 for a in actions}

    old_value = Q[state][action]
    next_max = max(Q[new_state].values())
    Q[state][action] = old_value + alpha * (r + gamma * next_max - old_value)

    ev3.screen.clear()
    ev3.screen.print("S:", state, "A:", action, "R:", r)
