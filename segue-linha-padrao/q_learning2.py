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

velocidade = 100
black = 8
white = 69
treshold = 0.1

def virar_direita():
    motor_esquerda.run(velocidade // 2)
    motor_direita.run(velocidade)

def virar_esquerda():
    motor_esquerda.run(velocidade)
    motor_direita.run(velocidade // 2)

def seguir_em_frente():
    motor_esquerda.run(velocidade)
    motor_direita.run(velocidade)


actions = ["forward", "left", "right"]
Q = {}
alpha, gamma, epsilon = 0.5, 0.8, 1  # hiperparâmetros

def get_state():
    l = color_esquerda.reflection()
    r = color_direita.reflection()
    
    if l < 50 and r < 50:   # ambos no preto
        return "both_black"
    elif l < 30:            # só esquerda no preto
        return "left_black"
    elif r < 30:            # só direita no preto
        return "right_black"
    else:                   # ambos no branco
        return "lost"

def choose_action(state):
    if random.random() < epsilon or state not in Q:
        return random.choice(actions)
    return max(Q[state], key=Q[state].get)

def perform_action(action):
    if state == "right_black":
        # gira procurando a linha
        motor_esquerda.run(100)
        motor_direita.run(10)
        wait(1000)
        motor_esquerda.stop()
        motor_direita.stop()
        return
    elif state == "left_black":
        motor_esquerda.run(10)
        motor_direita.run(100)
        wait(1000)
        motor_esquerda.stop()
        motor_direita.stop()
        return
    elif state == "lost":
        motor_esquerda.run(100)
        motor_direita.run(-100)
        wait(400)
        motor_esquerda.stop()
        motor_direita.stop()
    if action == "forward":
        seguir_em_frente()
    elif action == "left":
        virar_esquerda()  # força de curva simplificada
    elif action == "right":
        virar_direita()
    
    wait(100)
    motor_esquerda.stop()
    motor_direita.stop()

def reward(state):
    if state == "both_black":
        return 20   # perfeito
    elif state in ["left_black", "right_black"]:
        return 5   # está corrigindo
    else:
        return -20  # saiu da linha

    

# Loop principal
while True:
    
    epsilon = max(0.1, epsilon * 0.996)
    print(epsilon)
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
