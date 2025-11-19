# 🎮 Q-Learning aplicado ao LEGO EV3

O Q-Learning é um algoritmo de **Aprendizado por Reforço** que treina um agente a partir de tentativa e erro. No EV3, ele pode aprender como reagir às leituras dos sensores para tomar decisões de movimento.

---

# 🧠 1. Conceito

O robô mantém uma tabela Q:

Q[estado][ação]



Ela é atualizada com base em recompensas:

Q(s,a) = Q(s,a) + α * ( recompensa + γ * max(Q(s’,*)) – Q(s,a) )

Onde:  
- **α** = taxa de aprendizado  
- **γ** = desconto futuro  
- **recompensa** = feedback (bom ou ruim)  

---

# 🚗 2. Aplicação no EV3

O robô pode aprender ações como:

- virar direita  
- virar esquerda  
- acelerar  
- desacelerar  

Estados podem ser definidos pelas leituras dos sensores.

---

# 🔬 3. Explorando vs Explorando (ε-greedy)

se random < ε:
escolher ação aleatória
senao:
escolher ação com maior Q

---

# 📌 4. Projeto Relacionado
../q_learning/

---

# 🏁 5. Uso Prático
Embora demore para treinar, permite:

- comportamentos emergentes  
- adaptação a pistas diferentes  
- navegação inteligente  
