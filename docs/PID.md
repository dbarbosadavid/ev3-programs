# 📘 Controle PID — Teoria e Aplicação no LEGO EV3

O controle PID (Proporcional–Integral–Derivativo) é um algoritmo amplamente usado em sistemas de controle por sua precisão, estabilidade e velocidade. No contexto do LEGO EV3, ele permite que o robô siga linhas com muito mais eficiência que técnicas baseadas apenas em threshold.

---

# 🧠 1. Estrutura do PID

O algoritmo calcula uma **correção** com base no erro entre duas leituras de sensores.

## ● Erro  
erro = leitura_esquerda - leitura_direita

## ● Termos do PID  
- **P (Proporcional):** corrige imediatamente o erro atual  
- **I (Integral):** corrige erros residuais acumulados ao longo do tempo  
- **D (Derivativo):** evita oscilações, prevendo mudanças bruscas no erro  

correcao = (Kp * erro) + (Ki * soma_erro) + (Kd * derivada)

---

# ⚙️ 2. Benefícios no EV3

- Melhora a estabilidade  
- Permite maior velocidade  
- Reduz oscilações  
- Faz curvas suaves  
- Mantém o robô centrado sobre a linha

---

# 🔧 3. Ajuste das constantes (Tuning)

Valores comuns (podem variar por pista):

| Constante | Efeito |
|----------|--------|
| **Kp** alto demais → robô balança | baixo → robô reage lento |
| **Ki** alto demais → drift | baixo → erro residual permanece |
| **Kd** alto demais → robô vibra | baixo → robô oscila |

---

# 🏁 4. Aplicações

- Competições de velocidade  
- Seguidor de linha avançado  
- Rotas de precisão  
- Navegação autônoma  

Projetos associados: ../segue_linha_pid/