# 🧠 Redes Neurais no LEGO EV3

Este documento explica como redes neurais podem ser utilizadas em robôs LEGO EV3, seja implementando-as manualmente ou carregando modelos gerados externamente.

---

# 🧩 1. Conceito Geral

Uma rede neural é composta por camadas que recebem entradas, multiplicam pelos pesos e aplicam uma função de ativação.

No EV3 trabalhamos com **forward pass** simples:

saida = ativacao( soma( entrada * peso ) + bias )


Devido às limitações do hardware, usamos redes pequenas:

- 2 a 3 neurônios de entrada  
- 3 a 5 neurônios ocultos  
- 1 a 2 neurônios de saída  

---

# 🛠️ 2. Formas de Implementação no EV3

## ✔️ 1. Rede Neural Interna  
Implementada manualmente em Python (Pybricks), sem bibliotecas externas.  
Ideal para pequenos modelos e testes rápidos.

Projeto:  
../rede_neural_interna_ev3/

## ✔️ 2. Rede gerada no Open Roberta Lab  
Treinada visualmente e exportada para ONNX.  
Pesos são carregados externamente e utilizados no EV3.

Projeto:  
../open_roberta_lab_weigths/

---

# 📌 3. Aplicações

- Seguir linha com IA  
- Classificação de padrões  
- Navegação autônoma leve  
- Tomada de decisão baseada em sensores  

---

# 🔍 4. Limitações

- Hardware limitado  
- Processamento lento com redes grandes  
- Necessidade de quantização simples  