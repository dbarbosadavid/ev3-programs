#!/usr/bin/env pybricks-micropython

import json
import random
import math

class NeuralNetwork:

    def save_weights(self, filename="weights.json"):
        data = {
            "weights_input_hidden": self.weights_input_hidden,
            "weights_hidden_output": self.weights_hidden_output,
            "bias_hidden": self.bias_hidden,
            "bias_output": self.bias_output
        }
        with open(filename, "w") as f:
            json.dump(data, f)

    def load_weights(self, filename="weights.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.weights_input_hidden = data["weights_input_hidden"]
            self.weights_hidden_output = data["weights_hidden_output"]
            self.bias_hidden = data["bias_hidden"]
            self.bias_output = data["bias_output"]
            return True
        except (OSError, ValueError):
            print("Erro ao carregar os pesos. Treinando do zero.")
            return False

    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        self.weights_input_hidden = [[random.uniform(-1, 1) for _ in range(hidden_size)] for _ in range(input_size)]
        self.weights_hidden_output = [[random.uniform(-1, 1) for _ in range(output_size)] for _ in range(hidden_size)]

        self.bias_hidden = [random.uniform(-1, 1) for _ in range(hidden_size)]
        self.bias_output = [random.uniform(-1, 1) for _ in range(output_size)]

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def tanh(self, x):
        return math.tanh(x)

    def tanh_derivative(self, x):
        return 1 - x**2


    def forward(self, inputs):
        # Camada oculta
        self.hidden = [0] * self.hidden_size
        for j in range(self.hidden_size):
            total = self.bias_hidden[j]
            for i in range(self.input_size):
                total += inputs[i] * self.weights_input_hidden[i][j]
            self.hidden[j] = self.tanh(total)

        # Camada de saída
        self.output = [0] * self.output_size
        for k in range(self.output_size):
            total = self.bias_output[k]
            for j in range(self.hidden_size):
                total += self.hidden[j] * self.weights_hidden_output[j][k]
            self.output[k] = self.tanh(total)

        return self.output

    def train(self, inputs, expected_output, learning_rate=0.1):
        # Propagação para frente
        output = self.forward(inputs)

        # Cálculo do erro na saída
        output_errors = [expected_output[k] - output[k] for k in range(self.output_size)]

        # Gradientes da saída
        output_gradients = [output_errors[k] * self.tanh_derivative(output[k]) for k in range(self.output_size)]

        # Atualizar pesos da camada oculta → saída
        for j in range(self.hidden_size):
            for k in range(self.output_size):
                self.weights_hidden_output[j][k] += learning_rate * output_gradients[k] * self.hidden[j]
        
        # Atualizar vieses da saída
        for k in range(self.output_size):
            self.bias_output[k] += learning_rate * output_gradients[k]

        # Erro da camada oculta
        hidden_errors = [0] * self.hidden_size
        for j in range(self.hidden_size):
            for k in range(self.output_size):
                hidden_errors[j] += output_gradients[k] * self.weights_hidden_output[j][k]

        # Gradientes da camada oculta
        hidden_gradients = [hidden_errors[j] * self.tanh_derivative(self.hidden[j]) for j in range(self.hidden_size)]

        # Atualizar pesos da entrada → camada oculta
        for i in range(self.input_size):
            for j in range(self.hidden_size):
                self.weights_input_hidden[i][j] += learning_rate * hidden_gradients[j] * inputs[i]

        # Atualizar vieses da camada oculta
        for j in range(self.hidden_size):
            self.bias_hidden[j] += learning_rate * hidden_gradients[j]

        return output_errors





