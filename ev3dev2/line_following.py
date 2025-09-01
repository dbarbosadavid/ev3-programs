#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B
from ev3dev2.motor import MoveSteering
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_2
from time import sleep

# === CONFIGURAÇÕES GERAIS ===
BLACK = 5
WHITE = 40
THRESHOLD = (BLACK + WHITE) / 2
DRIVE_SPEED = 20  # Velocidade base

# Constantes do controlador PID
KP = 1.2  # Proporcional
KI = 0.02 # Integral
KD = 0.8  # Derivativo

def inicializar_componentes():
    steer_pair = MoveSteering(OUTPUT_A, OUTPUT_B)
    sensor = ColorSensor(INPUT_2)
    return steer_pair, sensor

def calcula_pid(erro, erro_anterior, soma_erros):

    derivada = erro - erro_anterior # Define o valor derivativo
    
    turn = (KP * erro) + (KI * soma_erros) + (KD * derivada) # Calcula a curva com PID  
    turn = max(min(turn, 100), -100)  # Limita curva

    return turn


def seguir_linha(steer_pair, sensor):
    erro_anterior = 0
    soma_erros = 0

    while True:
        reflexao = sensor.reflected_light_intensity
        erro = reflexao - THRESHOLD 

        soma_erros += erro
        soma_erros = max(min(soma_erros, 100), -100) # Limita os valores gerados

        turn = calcula_pid(erro, erro_anterior, soma_erros)
        steer_pair.on(steering=turn, speed=DRIVE_SPEED)

        erro_anterior = erro
        sleep(0.01)

if __name__ == "__main__":
    steer_pair, sensor = inicializar_componentes()
    seguir_linha(steer_pair, sensor)