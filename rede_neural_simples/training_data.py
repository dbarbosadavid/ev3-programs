import json

def gerar_dados(branco, preto):
    branco = branco/100
    preto = preto/100
    media = (preto + branco) / 2
    aumento = (media - preto) / 5

    sensor_esquerdo = []
    sensor_direito = []
    motor_esquerdo = []
    motor_direito = []

    for i in range(11):
        sensor_esquerdo.append(preto + aumento * i)
        sensor_direito.append(branco - aumento * i)
        if i <= 4:
            motor_esquerdo.append(-1/(i+1)**2)
            motor_direito.append(1)
        if i == 5:
                motor_esquerdo.append(1)
                motor_direito.append(1)
        if i >= 6:
                motor_esquerdo.append(1)
                motor_direito.append(-1/(11-i)**2)

    sensor_direito.append(branco)
    sensor_esquerdo.append(branco)
    motor_direito.append(1)
    motor_esquerdo.append(1)

    data = {
        "sensor_esquerdo": sensor_esquerdo,
        "sensor_direito": sensor_direito,
        "motor_esquerdo": motor_esquerdo,
        "motor_direito": motor_direito,
    }

    with open('training_data.json', "w") as f:
            json.dump(data, f)
        
def carregar_dados(filename="training_data.json"):
    with open(filename, "r") as f:
        data = json.load(f)

    training_data = []
    for i in range(len(data["sensor_esquerdo"])):
        input_data = (data["sensor_esquerdo"][i], data["sensor_direito"][i])
        output_data = (data["motor_esquerdo"][i], data["motor_direito"][i])
        print('inputs/outputs', input_data, output_data)
        training_data.append((input_data, output_data))
            
    print("Dados carregados com sucesso.")
    return training_data
    