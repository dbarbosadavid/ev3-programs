#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# Inicialização dos dispositivos
ev3 = EV3Brick()
motor_esquerdo = Motor(Port.A)
motor_direito = Motor(Port.B)
sensor_esquerdo = ColorSensor(Port.S1)
sensor_direito = ColorSensor(Port.S2)

cronometro = StopWatch()
velocidadeK = 4.5

# Variáveis da rede neural (extraídas do RobertaLab (Java) pós treinamento)
def nnStep(s1, s2):
    
    b_h1n1 = 19.72935268419554
    w_S1_h1n1 = -1.7607380874352934
    w_S2_h1n1 = 5.995171844047934

    b_h1n2 = 8.676026580646239
    w_S1_h1n2 = 10.851863028454568
    w_S2_h1n2 = -9.035157156822432

    b_Mot_L = -0.14717705511547738
    w_h1n1_Mot_L = -2.977681482033278
    w_h1n2_Mot_L = 10.26622261443128

    b_Mot_R = -0.017501467781120172
    w_h1n1_Mot_R = 5.578208807517729
    w_h1n2_Mot_R = -9.253346396722998

    h1n1 = b_h1n1 + s1 * w_S1_h1n1 + s2 * w_S2_h1n1
    h1n2 = b_h1n2 + s1 * w_S1_h1n2 + s2 * w_S2_h1n2

    mot_l = b_Mot_L + h1n1 * w_h1n1_Mot_L + h1n2 * w_h1n2_Mot_L
    mot_r = b_Mot_R + h1n1 * w_h1n1_Mot_R + h1n2 * w_h1n2_Mot_R

    return mot_l, mot_r

# Função para seguir a linha
cronometro.reset()

def segue_linha():
    while not (sensor_esquerdo.reflection() < 10 and sensor_direito.reflection() < 10):
        s1 = sensor_esquerdo.reflection() / 100
        s2 = sensor_direito.reflection() / 100
        mot_l, mot_r = nnStep(s1, s2)
        
        motor_esquerdo.run(mot_l * velocidadeK)
        motor_direito.run(mot_r * velocidadeK)

    print("Tempo Total:", cronometro.time())


# Loop principal

segue_linha()
motor_esquerdo.stop()
motor_direito.stop()
ev3.speaker.beep()

