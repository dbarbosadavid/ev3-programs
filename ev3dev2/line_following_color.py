#!/usr/bin/env python3
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveSteering
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

# === CONFIGURAÇÕES GERAIS ===
BLACK = 5  #5
WHITE = 60 #45
THRESHOLD = (BLACK + WHITE) / 2
DRIVE_SPEED = 10  # Velocidade base
COR_VERDE = 3  # Código da cor verde (ColorSensor.COLOR_GREEN)

# Constantes do controlador PID
KP = 5.0   # 5
KI = 0.0   # 0.02
KD = 0.0   # 0.3

def inicializar_componentes():
    steer_pair = MoveSteering(OUTPUT_A, OUTPUT_B)
    sensorEsq = ColorSensor(INPUT_1)
    sensorDir = ColorSensor(INPUT_2)
    return steer_pair, sensorEsq, sensorDir

def calcula_pid(erro, erro_anterior, soma_erros):
    derivada = erro - erro_anterior
    turn = (KP * erro) + (KI * soma_erros) + (KD * derivada)
    turn = max(min(turn, 100), -100)  # Limita curva
    print("Curva:", turn)
    return turn

def seguir_linha(steer_pair, sensorEsq, sensorDir):
    erro_anterior = 0
    soma_erros = 0

    while True:

        # Detecta a cor nos sensores
        cor_esquerda = sensorEsq.color
        cor_direita = sensorDir.color

        # Verifica se há verde em um dos lados
        if cor_esquerda == COR_VERDE:
            print("Verde esquerda: virando esquerda")
            steer_pair.on_for_seconds(steering=-80, speed=DRIVE_SPEED, seconds=0.7)
            continue

        if cor_direita == COR_VERDE:
            print("Verde direita: virando direita")
            steer_pair.on_for_seconds(steering=80, speed=DRIVE_SPEED, seconds=0.7)
            continue

        # Leitura da intensidade da luz refletida
        reflexo_esquerdo = sensorEsq.reflected_light_intensity
        reflexo_direito = sensorDir.reflected_light_intensity

        erroEsq = reflexo_esquerdo - THRESHOLD 
        erroDir = reflexo_direito - THRESHOLD

        # Em curvas muito estreitas ele perde a linha e vê branco, virando pra direita quando deveria virar para esquerda
        if erroEsq > 0 and erroEsq < erroDir: 
            erro = erroEsq * (-1)
        else:
            erro = erroEsq

        # PID
        soma_erros += erro
        soma_erros = max(min(soma_erros, 100), -100)
        turn = calcula_pid(erro, erro_anterior, soma_erros)
        steer_pair.on(steering=turn, speed=DRIVE_SPEED)
        erro_anterior = erro

        sleep(0.5)

if __name__ == "__main__":
    steer_pair, sensorEsq, sensorDir = inicializar_componentes()
    seguir_linha(steer_pair, sensorEsq, sensorDir)
