#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Color, Direction, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# Inicialização dos dispositivos
ev3 = EV3Brick()
motor_esquerdo = Motor(Port.A)
motor_direito = Motor(Port.B)
sensor_esquerdo = ColorSensor(Port.S1)
sensor_direito = ColorSensor(Port.S2)

# Base de movimentação
base = DriveBase(motor_esquerdo, motor_direito, wheel_diameter=56, axle_track=180)

# Variáveis da rede neural (extraídas do Java)
def nnStep(s1, s2):
    
    b_h1n1 = 19.84630082349111
    w_S1_h1n1 = -3.962532338601946
    w_S2_h1n1 = 4.198819054419457

    b_h1n2 = 9.066311929396003
    w_S1_h1n2 = 9.325798006397793
    w_S2_h1n2 = -8.932275349286144

    b_Mot_L = 0.000015314416910538847
    w_h1n1_Mot_L = -2.964962492028893
    w_h1n2_Mot_L = 9.622595984656261

    b_Mot_R = 0.00004682608918152318
    w_h1n1_Mot_R = 5.449530731650953
    w_h1n2_Mot_R = -8.511408048301586

    h1n1 = b_h1n1 + s1 * w_S1_h1n1 + s2 * w_S2_h1n1
    h1n2 = b_h1n2 + s1 * w_S1_h1n2 + s2 * w_S2_h1n2

    mot_l = b_Mot_L + h1n1 * w_h1n1_Mot_L + h1n2 * w_h1n2_Mot_L
    mot_r = b_Mot_R + h1n1 * w_h1n1_Mot_R + h1n2 * w_h1n2_Mot_R

    return mot_l, mot_r

# Função para seguir a linha
def segue_linha():
    while not (sensor_esquerdo.reflection() < 10 and sensor_direito.reflection() < 10):
        s1 = sensor_esquerdo.reflection() / 100
        s2 = sensor_direito.reflection() / 100
        mot_l, mot_r = nnStep(s1, s2)
        
        # Ajustar a velocidade dos motores
        motor_esquerdo.run(mot_l * 4)  # multiplica por 100 para converter em duty cycle (aproximadamente)
        motor_direito.run(mot_r * 4)

    # Parar os motores quando condição de parada for atingida
    motor_esquerdo.Stop()
    motor_direito.Stop()

# Função para detectar verde e tomar decisão
def ver_verde():
    cor_s2 = sensor_esquerdo.color()
    cor_s3 = sensor_direito.color()

    if cor_s2 == Color.GREEN and cor_s3 == Color.GREEN:
        base.turn(180)
    elif cor_s2 == Color.GREEN and cor_s3 != Color.GREEN:
        base.drive_time(50, 50, 600)  # curva para a direita
    elif cor_s2 != Color.GREEN and cor_s3 == Color.GREEN:
        base.drive_time(50, -50, 600)  # curva para a esquerda
    else:
        base.straight(10)  # anda um pouco para frente

# Loop principal
while True:
    segue_linha()
    ver_verde()

