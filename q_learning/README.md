# 🤖 Seguidor de Linha (Q-Learning) com EV3

## 📄 Visão Geral do Projeto

Este projeto demonstra a aplicação de **Aprendizado por Reforço (Reinforcement Learning - RL)**, especificamente o algoritmo **Q-Learning**, para treinar um robô **LEGO Mindstorms EV3** a seguir uma linha.

Diferente dos métodos de controle convencionais (como PID), o robô aprende as melhores ações (virar à esquerda, direita, ou seguir em frente) através de **tentativa e erro**, otimizando sua performance com base em recompensas.

---

## 🧠 Conceito Principal: Q-Learning

O Q-Learning é o coração deste código. Ele usa a matriz **Q** (implementada como um dicionário em Python) para armazenar o "valor de qualidade" de cada ação em um determinado estado. 

| Termo | Variável no Código | Descrição |
| :--- | :--- | :--- |
| **Q-Table** | `Q` | Dicionário que mapeia **estados** para **ações** e seus respectivos valores de qualidade. |
| **Estados** | `get_state()` | As quatro condições do ambiente: `both_black`, `left_black`, `right_black`, e `lost`. |
| **Ações** | `actions` | Movimentos que o robô pode realizar: `"forward"`, `"left"`, `"right"`. |
| **Recompensa** | `reward(state)` | Função que atribui um valor (positivo ou negativo) com base no novo estado atingido após uma ação. |
| **Exploração** | `epsilon` | Define a chance de o robô escolher uma ação aleatória (exploração). |
| **Fórmula de Atualização** | A equação que ajusta os valores de `Q` com base na recompensa (`r`), taxa de aprendizado (`alpha`) e fator de desconto (`gamma`). |

---

## ⚙️ Configuração e Hiperparâmetros

Os hiperparâmetros determinam a velocidade e a qualidade do aprendizado do robô.

| Parâmetro | Variável no Código | Valor Padrão | Função |
| :--- | :--- | :--- | :--- |
| **Taxa de Aprendizado** | `alpha` | `0.5` | Quão rapidamente a nova informação se sobrepõe à informação antiga. |
| **Fator de Desconto** | `gamma` | `0.8` | Importância das recompensas futuras (longo prazo). |
| **Taxa de Exploração** | `epsilon` | `1.0` | Probabilidade inicial de o robô *explorar* (escolhe uma ação aleatória). **Decai ao longo do tempo.** |
| **Velocidade Base** | `velocidade` | `100` | Velocidade base dos motores (em graus por segundo). |

---

## 💡 Funcionamento do Algoritmo

O robô opera em um loop contínuo de aprendizado e execução:

1.  **Observa o Estado (`get_state`):** O robô lê os sensores de cor e determina em qual dos 4 estados discretos ele se encontra.
2.  **Escolhe a Ação (`choose_action`):** Utiliza a política **epsilon-greedy**:
    * No início, o alto `epsilon` força a **exploração** (ações aleatórias).
    * Com o decaimento do `epsilon`, o robô passa a priorizar a **explotação** (a ação com o maior Q-valor conhecido).
3.  **Executa e Recompensa:** O robô executa a ação, observa o novo estado e recebe a recompensa correspondente:
    * **Positivo (+20):** Se estiver bem centralizado (`both_black`).
    * **Negativo (-20):** Se estiver perdido (`lost`).
4.  **Atualiza a Tabela Q:** A fórmula de Q-Learning ajusta o Q-valor da ação que acabou de ser executada, consolidando o aprendizado.

---

## 🛠️ Componentes de Hardware

O robô requer a seguinte configuração de portas:

| Componente | Variável no Código | Porta |
| :--- | :--- | :--- |
| **EV3 Brick** | `ev3` | - |
| **Motor Esquerdo** | `motor_esquerda` | `Port.A` |
| **Motor Direito** | `motor_direita` | `Port.B` |
| **Sensor de Cor** | `color_esquerda` | `Port.S1` |
| **Sensor de Cor** | `color_direita` | `Port.S2` |
