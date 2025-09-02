#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Button, Stop
from pybricks.tools import wait
import random, time

# ====== HARDWARE ======
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
cs_left = ColorSensor(Port.S1)
cs_right = ColorSensor(Port.S2)

# ====== AJUSTES ======
BASE_SPEED = 250
DELTA = 150
STEP_MS = 80

ALPHA = 0.3
GAMMA = 0.9
EPS_START = 0.5
EPS_MIN = 0.05
EPS_DECAY = 0.999

# Estados
STATE_BOTH = 0
STATE_LEFT = 1
STATE_RIGHT = 2
STATE_NONE = 3
states = [STATE_BOTH, STATE_LEFT, STATE_RIGHT, STATE_NONE]

# Ações
A_LEFT, A_STRAIGHT, A_RIGHT = 0, 1, 2
actions = [A_LEFT, A_STRAIGHT, A_RIGHT]

Q = [[0.0 for _ in actions] for __ in states]

# ====== CALIBRAÇÃO ======
def calibrate(sensor, name):
    ev3.screen.clear()
    ev3.screen.print("{name} BRANCO: center")
    while Button.CENTER not in ev3.buttons.pressed():
        wait(20)
    white = sensor.reflection()
    ev3.speaker.beep()

    ev3.screen.clear()
    ev3.screen.print("{name} PRETO: center")
    while Button.CENTER not in ev3.buttons.pressed():
        wait(20)
    black = sensor.reflection()
    ev3.speaker.beep()
    return (white + black) / 2

th_left = calibrate(cs_left, "Esq")
th_right = calibrate(cs_right, "Dir")

tol = 8  # tolerância

# ====== FUNÇÕES ======
def get_state():
    l = cs_left.reflection()
    r = cs_right.reflection()
    left_on = abs(l - th_left) <= tol
    right_on = abs(r - th_right) <= tol
    if left_on and right_on:
        return STATE_BOTH
    elif left_on and not right_on:
        return STATE_LEFT
    elif right_on and not left_on:
        return STATE_RIGHT
    else:
        return STATE_NONE

def reward(state):
    if state == STATE_BOTH:
        return 1.0
    elif state == STATE_NONE:
        return -2.0
    else:
        return 0.0

def step(action):
    if action == A_LEFT:
        l, r = BASE_SPEED - DELTA, BASE_SPEED + DELTA
    elif action == A_RIGHT:
        l, r = BASE_SPEED + DELTA, BASE_SPEED - DELTA
    else:  # STRAIGHT
        l, r = BASE_SPEED, BASE_SPEED
    left_motor.run(l)
    right_motor.run(r)
    wait(STEP_MS)
    left_motor.hold()
    right_motor.hold()

def choose_action(s, eps):
    if random.random() < eps:
        return random.choice(actions)
    return max(actions, key=lambda a: Q[s][a])

def update_q(s, a, r, s_next):
    best_next = max(Q[s_next])
    Q[s][a] = (1 - ALPHA) * Q[s][a] + ALPHA * (r + GAMMA * best_next)

def stop_all():
    left_motor.stop(Stop.BRAKE)
    right_motor.stop(Stop.BRAKE)

# ====== LOOP ======
ev3.screen.clear()
ev3.screen.print("Q-learning 2 sensores")
eps = EPS_START
s = get_state()

try:
    while True:
        if Button.CENTER in ev3.buttons.pressed():
            break
        a = choose_action(s, eps)
        step(a)
        s_next = get_state()
        r = reward(s_next)
        update_q(s, a, r, s_next)
        s = s_next
        eps = max(EPS_MIN, eps * EPS_DECAY)
except Exception as e:
    ev3.screen.print("Erro:", str(e))
finally:
    stop_all()
    ev3.screen.print("Fim!")
