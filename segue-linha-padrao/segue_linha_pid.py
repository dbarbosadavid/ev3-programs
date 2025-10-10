#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import ColorSensor, Motor
from pybricks.parameters import Port
from pybricks.tools import StopWatch, wait

# Inicializa dispositivos
ev3 = EV3Brick()
left_sensor = ColorSensor(Port.S1)
right_sensor = ColorSensor(Port.S2)
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
cronometro = StopWatch()

# Configurações iniciais
VELOCIDADE_BASE = 100

# Calibração manual (ajuste com seus valores reais)
REF_BRANCO = 60
REF_PRETO = 6
REF_MEDIA = (REF_BRANCO + REF_PRETO) / 2

# Constantes PID
Kp = 5
Ki = 0.025
Kd = 10

erro_acumulado = 0
erro_anterior = 0

ev3.speaker.beep()
cronometro.reset()

while True:
    # Leitura dos sensores
    left_value = left_sensor.reflection()
    right_value = right_sensor.reflection()

    # Cálculo do erro: diferença entre sensores
    erro = left_value - right_value  # Se positivo, desvia para a direita

    # PID
    erro_acumulado += erro
    derivada = erro - erro_anterior
    erro_anterior = erro

    correcao = Kp * erro + Ki * erro_acumulado + Kd * derivada

    # Cálculo das velocidades dos motores
    velocidade_esquerda = VELOCIDADE_BASE + correcao
    velocidade_direita = VELOCIDADE_BASE - correcao

    # Limita as velocidades
    velocidade_esquerda = max(min(velocidade_esquerda, 1000), -1000)
    velocidade_direita = max(min(velocidade_direita, 1000), -1000)

    # Aplica as velocidades
    left_motor.run(velocidade_esquerda)
    right_motor.run(velocidade_direita)

    # Condição de parada: ambos sensores no preto
    if left_value <= REF_PRETO and right_value <= REF_PRETO:
        break

    wait(10)

# Finalização
cronometro.pause()
left_motor.stop()
right_motor.stop()
ev3.speaker.beep()

ev3.screen.clear()
ev3.screen.print("Tempo total:")
ev3.screen.print(str(cronometro.time()))
