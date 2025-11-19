# 🤖 Seguidor de Linha Inteligente (RNA Onboard)

## 📄 Visão Geral do Projeto

Este projeto demonstra a implementação de um **Seguidor de Linha (Line Follower)** avançado para a plataforma **LEGO Mindstorms EV3**, utilizando uma **Rede Neural Artificial (RNA)** para o controle do robô.

A característica central deste projeto é que tanto o **modelo da Rede Neural** quanto o **treinamento (Backpropagation)** e a **persistência dos pesos** são executados diretamente no bloco EV3, utilizando o ambiente **Pybricks MicroPython**.

### 💡 Funcionalidades Principais

* **Treinamento Onboard:** A RNA é treinada no próprio EV3 utilizando dados gerados a partir da calibração de cores.
* **Persistência de Pesos:** Os pesos treinados são salvos em um arquivo `.json` (`weights.json`) e recarregados em execuções futuras, eliminando a necessidade de retreinamento constante.
* **Controle Suave:** A RNA mapeia continuamente as leituras dos sensores de cor para a velocidade ideal dos motores, resultando em um rastreamento de linha suave e adaptável.

---

## 🧠 Arquitetura da Rede Neural (RNA)

O controle do robô é feito por uma RNA *Feedforward* de duas camadas (Input, Hidden, Output).

| Camada | Tamanho | Função de Ativação |
| :--- | :---: | :--- |
| **Input (Entrada)** | **2** | - |
| **Hidden (Oculta)** | **2** | $\tanh(x)$ |
| **Output (Saída)** | **2** | $\tanh(x)$ |

### Mapeamento Input/Output

| Entrada (Input) | Saída Desejada (Output) |
| :--- | :--- |
| Reflexão do Sensor Esquerdo (Normalizada $[0, 1]$) | Velocidade do Motor Esquerdo (Normalizada $[-1, 1]$) |
| Reflexão do Sensor Direito (Normalizada $[0, 1]$) | Velocidade do Motor Direito (Normalizada $[-1, 1]$) |

---

## ⚙️ Módulos e Componentes

Este projeto é composto por quatro arquivos Python principais e requer a seguinte configuração de hardware:

### 📁 Estrutura de Arquivos

| Arquivo | Descrição |
| :--- | :--- |
| `main.py` | **Módulo Principal.** Executa o menu, gerencia o fluxo de treinamento/carregamento de pesos e executa o loop de rastreamento de linha. |
| `neural_network.py` | **Classe da RNA.** Contém a arquitetura, as funções de `forward` (inferência), `train` (backpropagation) e métodos para `save_weights`/`load_weights`. |
| `menu.py` | **Módulo de Calibração.** Permite calibrar os valores de preto e branco e oferece a opção de apagar os pesos salvos para forçar um novo treinamento. |
| `training_data.py` | **Geração de Dados.** Contém as funções para gerar e carregar o `training_data.json` a partir dos valores de calibração. |

### 🛠️ Configuração de Hardware

| Componente | Variável no Código | Porta |
| :--- | :--- | :--- |
| **Motor Esquerdo** | `left_motor` | `Port.A` |
| **Motor Direito** | `right_motor` | `Port.B` |
| **Sensor de Cor Esquerdo** | `left_color_sensor` | `Port.S1` |
| **Sensor de Cor Direito** | `right_color_sensor` | `Port.S2` |
| **Sensor Ultrassônico** | `ultrassonic_sensor` | `Port.S3` |

---

## 🚀 Fluxo de Trabalho e Treinamento

O robô opera seguindo o seguinte ciclo:

### 1. Inicialização e Calibração

1.  O `main.py` inicia e chama o `menu()`.
2.  O usuário pode optar por **recalibrar** as cores (preto e branco) e apagar os pesos antigos.
3.  Se os pesos forem apagados, o `training_data.py` gera um novo conjunto de **dados de treinamento supervisionado** com base nas novas calibrações.

### 2. Carregamento ou Treinamento

1.  A função `nn.load_weights()` tenta carregar os pesos do arquivo `weights.json`.
2.  **Se Carregado:** O robô entra diretamente no loop de rastreamento.
3.  **Se Não Carregado (ou Recalibrado):**
    * O código entra no loop de treinamento por `EPOCAS` (padrão: `1000`).
    * O método `nn.train()` utiliza o algoritmo **Backpropagation** para ajustar os pesos da rede, minimizando o erro entre a saída da rede e a saída desejada.
    * Os erros e o progresso são exibidos na tela e no console do EV3.

### 3. Execução (Rastreamento de Linha)

Após o treinamento (ou carregamento dos pesos), o robô inicia o rastreamento:

1.  Os valores de refletância dos sensores de cor são lidos continuamente e **normalizados** para o intervalo $[0, 1]$.
2.  Os dados normalizados são passados para a rede via `nn.forward()`.
3.  A saída da rede (valores $[-1, 1]$) é escalonada pela `VELOCIDADE` máxima (padrão: `230`) para obter as velocidades finais dos motores.
4.  O loop de rastreamento para quando *ambos* os sensores detectam uma reflexão baixa (menor que `6`), indicando o fim da pista.

---

## ⚙️ Variáveis Chave em `main.py`

| Variável | Valor Padrão | Descrição |
| :--- | :---: | :--- |
| `VELOCIDADE` | `230` | Velocidade máxima permitida para os motores durante o rastreamento. |
| `EPOCAS` | `1000` | Número de repetições completas do conjunto de dados durante o treinamento da RNA. |
| `input_size` | `2` | Número de entradas da RNA (sensores de cor). |
| `output_size` | `2` | Número de saídas da RNA (motores). |