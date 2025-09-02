#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Button, Stop
from pybricks.tools import wait
import random

# ========== HARDWARE ==========
ev3 = EV3Brick()
motor_esquerda = Motor(Port.A)
motor_direita = Motor(Port.B)
color_esquerda = ColorSensor(Port.S1)
color_direita = ColorSensor(Port.S2)

velocidade = 200
treshold = 0.2  # faixa de tolerância do erro

# ========== Q-LEARNING ==========
ALPHA = 0.3
GAMMA = 0.9
EPSILON = 0.4   # chance de explorar
EPSILON_DECAY = 0.999
EPSILON_MIN = 0.05

# Estados
STATE_LEFT = 0
STATE_ALIGNED = 1
STATE_RIGHT = 2
STATE_LOST = 3
states = [STATE_LEFT, STATE_ALIGNED, STATE_RIGHT, STATE_LOST]

# Ações
A_LEFT = 0
A_STRAIGHT = 1
A_RIGHT = 2
actions = [A_LEFT, A_STRAIGHT, A_RIGHT]

# Q-table inicial
Q = [[0.0 for _ in actions] for __ in states]

# ========== FUNÇÕES ==========
def calcular_erro():
    ref_esquerda = color_esquerda.reflection()
    ref_direita = color_direita.reflection()
    return (ref_esquerda - ref_direita) / 30

def get_state(error):
    if error > treshold:
        return STATE_RIGHT
    elif error < -treshold:
        return STATE_LEFT
    elif abs(error) <= treshold:
        return STATE_ALIGNED
    else:
        return STATE_LOST

def reward(state):
    if state == STATE_ALIGNED:
        return 1.0
    elif state == STATE_LOST:
        return -2.0
    else:
        return 0.0

def executar_acao(action):
    if action == A_LEFT:
        motor_esquerda.run(-velocidade // 2)
        motor_direita.run(velocidade)
    elif action == A_RIGHT:
        motor_esquerda.run(velocidade)
        motor_direita.run(-velocidade // 2)
    elif action == A_STRAIGHT:
        motor_esquerda.run(velocidade)
        motor_direita.run(velocidade)
    wait(80)
    motor_esquerda.run(0)
    motor_direita.run(0)

def escolher_acao(state, epsilon):
    if random.random() < epsilon:
        return random.choice(actions)
    return max(actions, key=lambda a: Q[state][a])

def atualizar_q(s, a, r, s_next):
    melhor = max(Q[s_next])
    Q[s][a] = (1 - ALPHA) * Q[s][a] + ALPHA * (r + GAMMA * melhor)

def stop_all():
    motor_esquerda.stop(Stop.BRAKE)
    motor_direita.stop(Stop.BRAKE)

# ========== LOOP ==========
ev3.speaker.beep()
epsilon = EPSILON
s = get_state(calcular_erro())

try:
    while True:
        if Button.CENTER in ev3.buttons.pressed():
            break

        a = escolher_acao(s, epsilon)
        executar_acao(a)

        erro = calcular_erro()
        s_next = get_state(erro)
        r = reward(s_next)

        atualizar_q(s, a, r, s_next)

        s = s_next
        epsilon = max(EPSILON_MIN, epsilon * EPSILON_DECAY)

except Exception as e:
    ev3.screen.print("Erro:", str(e))
finally:
    stop_all()
    ev3.screen.print("Fim!")
