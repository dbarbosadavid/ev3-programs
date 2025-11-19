# 🤖 Seguidor de Linha de Alto Desempenho com Controle PID

## 📄 Visão Geral do Projeto

Este repositório contém um programa **MicroPython (Pybricks)** para o **LEGO Mindstorms EV3** que implementa um **Seguidor de Linha (Line Follower)** utilizando o robusto algoritmo de controle **PID (Proporcional-Integral-Derivativo)**.

O controle PID é essencial para robôs de competição, pois permite correções de curso mais suaves, precisas e rápidas do que os métodos baseados em simples limiares (thresholds) ou lógica booleana.

---

## 🧠 Lógica de Controle: Algoritmo PID

O controle PID calcula a **correção** que deve ser aplicada aos motores com base em três fatores que analisam o **erro** atual do robô. 

### 1. Cálculo do Erro

O erro é a diferença direta entre as leituras de refletância dos dois sensores.
> **Erro** = Reflexão Esquerda - Reflexão Direita

* Se o **Erro** for positivo, o robô está desviando para a **direita** (Sensor Esquerdo está mais claro).
* Se o **Erro** for negativo, o robô está desviando para a **esquerda** (Sensor Direito está mais claro).

### 2. Componentes da Correção

A **Correção** final aplicada aos motores é a soma ponderada dos três termos.

> **Correção** = (Kp * Erro) + (Ki * Erro Acumulado) + (Kd * Derivada)

| Termo | Variável | Função no Controle |
| :--- | :--- | :--- |
| **Proporcional (P)** | `Kp * erro` | Responde ao **erro atual**. Garante a correção imediata. |
| **Integral (I)** | `Ki * erro_acumulado` | Responde ao **erro histórico**. Elimina o erro de estado estacionário (offset). |
| **Derivativo (D)** | `Kd * derivada` | Responde à **taxa de mudança do erro**. Amortece oscilações e estabiliza o robô. |

---

## ⚙️ Configurações e Calibração

O desempenho do robô depende diretamente de ajustes precisos.

### 🎯 Constantes PID (Tuning)

As constantes PID são cruciais e devem ser ajustadas (`tuning`) para cada robô e pista.

| Constante | Valor Padrão | Descrição |
| :--- | :---: | :--- |
| `Kp` | `5` | **Ganho Principal.** Ajusta a força da reação imediata ao desvio. |
| `Ki` | `0.025` | **Ganho Integral.** Ajusta a influência do erro histórico. |
| `Kd` | `10` | **Ganho Derivativo.** Ajusta o amortecimento das oscilações. |

### 🎨 Calibração de Cores

A precisão do `erro` depende dos valores de referência.

* `REF_BRANCO = 60`
* `REF_PRETO = 6`

> **Importante:** Os valores de `REF_BRANCO` e `REF_PRETO` devem ser ajustados manualmente no código para corresponderem às leituras reais da sua pista.

---

## 🛠️ Componentes de Hardware

O robô requer a seguinte configuração de portas:

| Componente | Variável no Código | Porta |
| :--- | :--- | :--- |
| **EV3 Brick** | `ev3` | - |
| **Motor Esquerdo** | `left_motor` | `Port.A` |
| **Motor Direito** | `right_motor` | `Port.B` |
| **Sensor de Cor Esquerdo** | `left_sensor` | `Port.S1` |
| **Sensor de Cor Direito** | `right_sensor` | `Port.S2` |

---

## 🏁 Fluxo de Execução

1.  **Início:** O programa toca um *beep* e zera o `StopWatch`.
2.  **Cálculo:** Dentro do loop principal, a `correcao` PID é calculada a cada iteração (`wait(10)`).
3.  **Movimento:** As velocidades dos motores são calculadas como `VELOCIDADE_BASE ± correcao`.
    * O código também inclui uma etapa de **limitação** (`max(min(...))`) para garantir que as velocidades permaneçam dentro dos limites seguros (entre -1000 e 1000).
4.  **Parada:** O loop é encerrado quando a condição de parada é satisfeita: **ambos** os sensores leem um valor igual ou inferior a `REF_PRETO`.
5.  **Finalização:** Os motores são parados, um *beep* é emitido e o tempo total de execução é exibido na tela do EV3.