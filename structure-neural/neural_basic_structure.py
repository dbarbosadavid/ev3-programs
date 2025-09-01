#!/usr/bin/env python3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.tools import wait
from pybricks.robotics import DriveBase

ev3 = EV3Brick()
sensorUlt = UltrasonicSensor(Port.S4)

motorDir = Motor(Port.B)
motorEsq = Motor(Port.C)
robo = DriveBase(motorEsq, motorDir, wheel_diameter=55.5, axle_track=104)

#Parâmetros de uma rede neural
dist = 30 # Distancia que o robo deve manter do objeto
bias = -0.39651959669023307 # Valor definido depois de treinar a rede neural no Roberta Lab
pesoSensor = 9995105730045505 # Peso do valor de entrada do sensor
pesoDist = -9855879007070074 # Peso da distancia definida como 30

#Valor de saída (output)
velocidade = 0

#Valores de entrada (dist e valor do SensorUltrasonico)

def calcular_velocidade(distUlt):
    velocidade = bias + (dist * pesoDist) + (distUlt * pesoSensor)
    return velocidade

while True:
    distUlt = sensorUlt.distance() / 10
    robo.drive(calcular_velocidade(distUlt), 0)
    wait(10)
