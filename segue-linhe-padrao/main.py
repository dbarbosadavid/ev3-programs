#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor, TouchSensor, ColorSensor,
    InfraredSensor, UltrasonicSensor, GyroSensor
)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Este programa requer LEGO EV3 MicroPython v2.0 ou superior.

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

# Função para calcular erro com base nos sensores
def calcular_erro():
    ref_esquerda = color_esquerda.reflection()
    ref_direita = color_direita.reflection()
    error = (ref_esquerda - ref_direita) / 30
    print("L: ", ref_esquerda)
    print("R: ", ref_direita)
    print("erro: ", error)
    return error

# Ações baseadas no erro
def virar_direita(error):
    motor_esquerda.run(velocidade * error)
    motor_direita.run(-(velocidade * error) / 2)

def virar_esquerda(error):
    motor_esquerda.run(-(velocidade * -error) / 2)
    motor_direita.run(velocidade * -error)

def seguir_em_frente():
    motor_esquerda.run(velocidade)
    motor_direita.run(velocidade)

# Início do programa
ev3.speaker.beep()

while True:
    error = calcular_erro()
    
    while error > treshold:
        virar_direita(error)
        error = calcular_erro()

    while error < -treshold:
        virar_esquerda(error)
        error = calcular_erro()

    while -treshold <= error <= treshold:
        seguir_em_frente()
        error = calcular_erro()
