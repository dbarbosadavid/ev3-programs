# 🤖 EV3 Line Follower (Seguidor de Linha) com Rede Neural

## 📄 Visão Geral do Projeto

Este repositório contém o código **MicroPython (Pybricks)** para um seguidor de linha altamente eficiente e adaptável, desenvolvido para a plataforma **LEGO Mindstorms EV3**.

O diferencial deste projeto é a utilização de um sistema de controle baseado em uma **Rede Neural (NN)**, cujos pesos e *bias* foram pré-treinados pela plataforma do Open Roberta Lab utilizando a tabela de treinamento do arquivo: *data_table_training.csv*. Essa abordagem permite um comportamento de rastreamento mais robusto e otimizado em comparação com os métodos de controle tradicionais.

---

## 🧠 Sistema de Controle: Rede Neural (`nnStep`)

O coração do projeto é a função `nnStep(s1, s2)`, que simula uma rede neural. O código efetua o mapeamento dos valores de reflexão dos sensores para os comandos de velocidade dos motores, utilizando os pesos **pré-calculados** da NN.

### 📐 Estrutura da Rede

A Rede Neural é uma arquitetura *Feedforward* simples que opera da seguinte forma:

1.  **Entrada (Input):**
    * `s1`: Valor de Reflexão do Sensor Esquerdo (normalizado: `0` a `1`).
    * `s2`: Valor de Reflexão do Sensor Direito (normalizado: `0` a `1`).

2.  **Camada Oculta (Hidden Layer):**
    * Dois neurônios ocultos (`h1n1` e `h1n2`).

3.  **Saída (Output):**
    * `mot_l`: Valor de potência para o Motor Esquerdo.
    * `mot_r`: Valor de potência para o Motor Direito.

---

## 🛠️ Componentes de Hardware

Para executar este código, o robô deve ser montado com a seguinte configuração de portas:

| Componente | Variável no Código | Porta |
| :--- | :--- | :--- |
| **EV3 Brick** | `ev3` | - |
| **Motor Esquerdo** | `motor_esquerdo` | `Port.A` |
| **Motor Direito** | `motor_direito` | `Port.B` |
| **Sensor de Cor** | `sensor_esquerdo` | `Port.S1` |
| **Sensor de Cor** | `sensor_direito` | `Port.S2` |


---

## 🚀 Como Utilizar

### Pré-requisitos

1.  **Firmware Pybricks:** O bloco EV3 deve estar rodando o firmware **Pybricks MicroPython**.
2.  **Setup do Robô:** O robô deve estar montado com os sensores e motores nas portas especificadas acima.

### Instruções de Execução

1.  Copie o código completo para o seu ambiente de desenvolvimento Pybricks (VSCode com a extensão EV3 MicroPython).
2.  Transfira o arquivo para o bloco EV3 via USB.
3.  Posicione o robô na linha e inicie o programa.

**Comportamento do Robô:**

* O robô se move seguindo a linha, utilizando a NN para calcular a potência dos motores a cada passo.
* O rastreamento é interrompido quando **ambos** os sensores detectam uma reflexão abaixo de **10** (a condição de parada).
* Ao parar, o tempo total de execução (`cronometro.time()`) é exibido e o EV3 emite um `beep()` de confirmação.

---

## 📚 Estrutura do Código

O script é dividido em três seções principais:

| Seção | Objetivo |
| :--- | :--- |
| **Inicialização** | Importa as bibliotecas Pybricks, mapeia os motores/sensores e define a constante de ganho de velocidade (`velocidadeK`). |
| **`nnStep(s1, s2)`** | Função que contém todos os pesos e *bias* da NN, responsável pelo cálculo dos valores de saída dos motores. |
| **`segue_linha()`** | Contém o loop principal que lê os sensores, normaliza os dados, chama a NN e aplica a potência calculada aos motores. |