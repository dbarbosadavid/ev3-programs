#!/usr/bin/env python3
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveSteering
from ev3dev2.sensor import INPUT_1, INPUT_2

BLACK = 5
WHITE = 47
THRESHOLD = (BLACK + WHITE) / 2

sensor = ColorSensor(INPUT_1)
sensor2 = ColorSensor(INPUT_2)
steer_pair = MoveSteering(OUTPUT_A, OUTPUT_B)

while True:

    print("Media", THRESHOLD)

    reflexEsq = sensor.reflected_light_intensity
    reflexDir = sensor2.reflected_light_intensity

    print("Reflexo Esquerda", reflexEsq)
    print("Reflexo Direita", reflexDir)

    erroEsq = reflexEsq - THRESHOLD
    erroDir = reflexDir - THRESHOLD

    print("Erro Esquerdo:", erroEsq)
    print("Erro Direito:", erroDir)

