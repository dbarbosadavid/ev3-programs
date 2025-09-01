#!/usr/bin/env python3

from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import SpeedRPM, MoveTank
from ev3dev2.sound import Sound

# Inicializa motores nas portas A e B
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

# Inicializa o speaker do EV3
sound = Sound()

# Anda para frente (equivalente a 300mm = 0.3m)
tank_drive.on_for_rotations(SpeedRPM(60), SpeedRPM(60), 2)
sound.beep()

# Anda para trás
tank_drive.on_for_rotations(SpeedRPM(-60), SpeedRPM(-60), 2)
sound.beep()

# Gira 360 graus no sentido horário (direita)
tank_drive.on_for_degrees(SpeedRPM(60), SpeedRPM(-60), 700)  # ajuste o valor se necessário
sound.beep()

# Gira 360 graus no sentido anti-horário (esquerda)
tank_drive.on_for_degrees(SpeedRPM(-60), SpeedRPM(60), 700)
sound.beep()
