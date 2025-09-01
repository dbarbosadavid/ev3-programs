#!/usr/bin/env python3

from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, SpeedRPM, MoveTank
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sensor import INPUT_2
from ev3dev2.sound import Sound

# Inicializa os motores como base do tipo tanque
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

# Inicializa o sensor ultrassônico na porta S4
obstacle_sensor = UltrasonicSensor(INPUT_2)

# Inicializa o speaker
sound = Sound()

# Emite um beep para indicar que está pronto
sound.beep()

# Loop principal
while True:
    # Move para frente continuamente com 40% da velocidade
    tank_drive.on(SpeedRPM(60), SpeedRPM(60))
    
    # Espera até detectar um obstáculo a menos de 30 cm (300 mm)
    while obstacle_sensor.distance_centimeters <= 30:
        
        print(obstacle_sensor.distance_centimeters)

        sleep(0.01)  # Espera 10 milissegundos

        # Para os motores ao detectar obstáculo
        tank_drive.off()

        # Dá ré por cerca de 300 mm (ajustando a rotação)
        tank_drive.on_for_rotations(SpeedRPM(-60), SpeedRPM(-60), 2)

        # Gira para a direita 120 graus (ajuste o valor conforme necessário)
        tank_drive.on_for_degrees(SpeedRPM(60), SpeedRPM(-60), 300)


