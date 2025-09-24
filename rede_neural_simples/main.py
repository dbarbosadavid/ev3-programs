#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import ColorSensor, Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.tools import wait, StopWatch

from neural_network import NeuralNetwork
import os


# Para treinar a rede neural do zero
'''
filename = "weights.json"

try:
    os.remove(filename)
    print("Arquivo ", filename, " apagado com sucesso.")
except OSError:
    print("Erro ao apagar o arquivo ", filename, ". Ele pode não existir.")
'''

# Inicializando o EV3 Brick e os sensores
ev3 = EV3Brick()
left_color_sensor = ColorSensor(Port.S1)
right_color_sensor = ColorSensor(Port.S2)

left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

# Configuração da rede neural (2 entradas, 2 saídas)
input_size = 2
hidden_size = 2
output_size = 2
nn = NeuralNetwork(input_size, hidden_size, output_size)

cronometro = StopWatch()
velocidadeK = 250

training_data = [
        ([0, 1], [-1, 1]),
        ([0.1, 0.9], [-0.75, 1]),
        ([0.2, 0.8], [-0.5, 1]),
        ([0.3, 0.7], [-0.25, 1]),
        ([0.4, 0.6], [0, 1]),
        ([0.5, 0.5], [1, 1]),
        ([0.6, 0.4], [1, -0]),
        ([0.7, 0.3], [1, -0.25]),
        ([0.8, 0.2], [1, -0.5]),
        ([0.9, 0.1], [1, -0.75]),
        ([1, 0], [1, -1]),
        ([1, 1], [1, 1]),
    ]

carregado = nn.load_weights() 

if carregado: 
    print("Pesos carregados com sucesso.")
else:
    print("Treinando do zero.")
    for epoch in range(1000):  # Número de épocas (iterações)
        
        total_error = 0
        for inputs, expected_output in training_data:
            # Treinando a rede com os dados de entrada e saída desejada
            error = nn.train(inputs, expected_output)
            total_error += sum(error)
                
        if epoch % 10 == 0:
            print('Época ', epoch, ': Erro total ', total_error)
            print("treinando...")
            print(epoch)
    
nn.save_weights()

left_reflect = left_color_sensor.reflection()
right_reflect = right_color_sensor.reflection()






ev3.speaker.beep()
cronometro.reset()

while left_reflect > 6 or right_reflect > 6:
    # Coletando dados dos sensores (refletância vai de 0 a 100)
    print("L:", left_reflect, " R:", right_reflect)
    left_reflect = left_color_sensor.reflection()
    right_reflect = right_color_sensor.reflection()

    # Normalizando para [0, 1]
    left_input = left_reflect / 100
    right_input = right_reflect / 100

    # Passando para a rede neural
    outputs = nn.forward([left_input, right_input])
    
    # Convertendo a saída para velocidade dos motores
    left_speed = int(outputs[0]  * velocidadeK)
    right_speed = int(outputs[1]  * velocidadeK)

    # Aplicando a velocidade nos motores
    left_motor.run(left_speed)
    right_motor.run(right_speed)

cronometro.pause()
print("Tempo total: ", cronometro.time())
left_motor.stop()
right_motor.stop()
ev3.speaker.beep()
    
