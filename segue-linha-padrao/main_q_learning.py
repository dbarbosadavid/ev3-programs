#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port
from pybricks.tools import wait
import random
import json

# Inicializa EV3 e dispositivos
ev3 = EV3Brick()

motor_esquerda = Motor(Port.A)
motor_direita = Motor(Port.B)

color_esquerda = ColorSensor(Port.S1)
color_direita = ColorSensor(Port.S2)

# Hiperparâmetros
n_states = 3
alpha = 0.2       # taxa de aprendizado
gamma = 0.9       # fator de desconto
epsilon = 0.2     # taxa de exploração
vel = 200         # velocidade do robô

# Estados e ações
actions = ['LEFT', 'RIGHT', 'FORWARD']
Q = {}

# Função para discretizar os valores de reflexão
def get_state():
    def classify(ref):
        if ref < 10:
            return 'B'  # Preto
        elif ref > 60:
            return 'W'  # Branco
        else:
            return 'G'  # Cinza (borda da linha)

    l = classify(color_esquerda.reflection())
    r = classify(color_direita.reflection())
    return (l, r)

# Escolher ação baseada em política epsilon-greedy
def choose_action(state):
    if state not in Q:
        Q[state] = {a: 0 for a in actions}
    if random.random() < epsilon:
        return random.choice(actions)
    return max(Q[state], key=Q[state].get)

# Executa ação no robô
def execute_action(action):
    if action == 'LEFT':
        motor_esquerda.run(-vel//2)
        motor_direita.run(vel)
    elif action == 'RIGHT':
        motor_esquerda.run(vel)
        motor_direita.run(-vel//2)
    elif action == 'FORWARD':
        motor_esquerda.run(vel)
        motor_direita.run(vel)
    wait(200)
    motor_esquerda.stop()
    motor_direita.stop()

# Calcula recompensa com base no estado
def get_reward(state):
    if state == ('G', 'G'):
        return 1
    elif 'G' in state:
        return 0
    else:
        return -1

# Loop de treinamento
ev3.speaker.beep()

for episode in range(1000):
    state = get_state()
    action = choose_action(state)
    execute_action(action)
    next_state = get_state()
    reward = get_reward(next_state)

    if next_state not in Q:
        Q[next_state] = {a: 0 for a in actions}

    old_value = Q[state][action]
    next_max = max(Q[next_state].values())

    Q[state][action] = old_value + alpha * (reward + gamma * next_max - old_value)

    # Pequeno descanso entre passos
    wait(50)
