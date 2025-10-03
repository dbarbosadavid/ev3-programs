#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import ColorSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.tools import wait
import os

ev3 = EV3Brick()
left_color_sensor = ColorSensor(Port.S1)
right_color_sensor = ColorSensor(Port.S2)


def menu():
    ev3.screen.print("Mantenha o\nbotão para\npara recalibrar") 
    ev3.screen.print("Ou aguarde para\n carregar pesos")
    wait (3000)
    recalibrar = False
    if(ev3.buttons.pressed()):
        recalibrar = True
    ev3.screen.clear()

    if recalibrar:
        wait(1000)
        filename = "weights.json"

        try:
            os.remove(filename)
            print("Arquivo ", filename, " apagado com sucesso.")
        except OSError:
            print("Erro ao apagar o arquivo ", filename, ". Ele pode não existir.")

        ev3.screen.print("Aperte com o\nsensor esquerdo\nno branco")  
        while not ev3.buttons.pressed():
            branco = left_color_sensor.reflection()

        wait(1000)
        ev3.screen.clear()
        ev3.screen.print("Aperte com o\nsensor esquerdo\nno preto") 
        while not ev3.buttons.pressed():
            preto = left_color_sensor.reflection()
        ev3.screen.clear()
        ev3.screen.print(branco) 
        ev3.screen.print(preto) 