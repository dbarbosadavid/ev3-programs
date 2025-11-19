# 🤖 Seguidor de Linha Clássico por Limiares (Threshold-Based)

## 📄 Visão Geral do Projeto

Este repositório contém um programa **MicroPython (Pybricks)** para o **LEGO Mindstorms EV3** que implementa um **Seguidor de Linha** utilizando lógica de **limiares (thresholds)** para correção.

O código calcula o erro como a diferença entre as leituras dos dois sensores de cor. Com base na magnitude desse erro, o robô alterna entre três estados: **Seguir em Frente**, **Virar à Direita** ou **Virar à Esquerda**.

---

## 🧠 Lógica de Controle: Baseada em Erro

O núcleo do controle é a função `calcular_erro()`, que determina a posição do robô em relação à linha.

### 📐 Cálculo do Erro

O erro é definido pela diferença normalizada entre as leituras dos sensores de cor:

> **Erro** = (Reflexão Esquerda - Reflexão Direita) / 30

Este valor de **Erro** é usado para determinar a ação:

| Faixa de Erro | Estado (Ação Principal) | Condição |
| :--- | :--- | :--- |
| **Erro > treshold** | **Virar à Direita** (`virar_direita`) | O robô está muito à esquerda da linha (Sensor Direito está mais no preto). |
| **Erro < -treshold** | **Virar à Esquerda** (`virar_esquerda`) | O robô está muito à direita da linha (Sensor Esquerdo está mais no preto). |
| **-treshold $\le$ Erro $\le$ treshold** | **Seguir em Frente** (`seguir_em_frente`) | O robô está razoavelmente centralizado na linha. |

### 🧭 Correção de Movimento

As funções `virar_direita` e `virar_esquerda` aplicam diferentes níveis de correção à velocidade (`velocidade = 220`) dos motores para trazer o robô de volta ao centro da linha de forma agressiva.

---

## 🛠️ Componentes de Hardware

O robô requer a seguinte configuração de portas:

| Componente | Variável no Código | Porta |
| :--- | :--- | :--- |
| **EV3 Brick** | `ev3` | - |
| **Motor Esquerdo** | `motor_esquerda` | `Port.A` |
| **Motor Direito** | `motor_direita` | `Port.B` |
| **Sensor de Cor Esquerdo** | `color_esquerda` | `Port.S1` |
| **Sensor de Cor Direito** | `color_direita` | `Port.S2` |

---

## 🚀 Como Utilizar

### Pré-requisitos

1.  O bloco EV3 deve estar rodando o firmware **Pybricks MicroPython**.
2.  O robô deve ser montado com dois sensores de cor frontais, posicionados para rastrear a linha.
3.  O valor de `treshold` (padrão `0.2`) e o divisor na função `calcular_erro()` (padrão `30`) podem precisar de ajustes finos dependendo da luz ambiente e das características da linha.

### Início e Parada

* **Início:** O programa toca um *beep* e zera o cronômetro (`StopWatch`).
* **Loop:** O robô segue a linha indefinidamente até a condição de parada.
* **Condição de Parada:** O robô para quando **ambos** os sensores de cor detectam uma leitura de reflexão muito baixa (abaixo de **12**), indicando o final da pista ou uma área totalmente escura.
* **Término:** Os motores são parados, o robô emite outro *beep* e o tempo total de execução é impresso.
