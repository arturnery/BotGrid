# 📚 Guia Completo - Grid Trading Bot

## Índice
1. [O que é Grid Trading?](#o-que-é-grid-trading)
2. [Configuração Básica](#configuração-básica)
3. [Parâmetros do Bot](#parâmetros-do-bot)
4. [Estratégias Explicadas](#estratégias-explicadas)
5. [Exemplos Práticos](#exemplos-práticos)
6. [Dicas e Boas Práticas](#dicas-e-boas-práticas)

---

## O que é Grid Trading?

**Grid Trading** é uma estratégia de trading que coloca múltiplas ordens de compra e venda em diferentes níveis de preço, formando uma "grade" (grid).

### Exemplo Visual:

```
Preço
  |
  | ← SELL (Venda) 55204
  | ← SELL (Venda) 54121
  | ← SELL (Venda) 53060
  | ← SELL (Venda) 52020
  | ← SELL (Venda) 51000
  |
  | ← Preço Base: 50000 (ponto central)
  |
  | ← BUY (Compra) 49000
  | ← BUY (Compra) 48020
  | ← BUY (Compra) 47059
  | ← BUY (Compra) 46118
  | ← BUY (Compra) 45196
  |
```

### Como Funciona:

1. **Quando o preço sobe:**
   - As ordens de VENDA (acima) são executadas
   - Você vende alto e lucra

2. **Quando o preço cai:**
   - As ordens de COMPRA (abaixo) são executadas
   - Você compra baixo

3. **O bot monitora continuamente:**
   - Se uma ordem é preenchida, o bot cria uma nova no lugar
   - Isso permite capturar lucro em cada oscilação de preço

---

## Configuração Básica

Abra o arquivo `config.py` e você verá:

```python
# ============================================
# CONFIGURAÇÕES DO GRID TRADING
# ============================================

SYMBOL = "BTC_USDT"           # Par de trading
BASE_PRICE = 50000            # Preço central
PRICE_RANGE = 1000            # Intervalo total
GRID_LEVELS = 5               # Número de níveis
ORDER_SIZE = 0.01             # Tamanho de cada ordem
MODE = "NEUTRAL"              # Modo de operação
GRID_TYPE = "GEOMETRIC"       # Tipo de grid
GEOMETRIC_PERCENTAGE = 2      # Percentual para grid geométrico
```

---

## Parâmetros do Bot

### 1. **SYMBOL** (Par de Trading)
**O que é:** O ativo que você quer fazer trading

**Exemplos:**
- `BTC_USDT` - Bitcoin em USDT
- `ETH_USDT` - Ethereum em USDT
- `SOL_USDT` - Solana em USDT

**Como escolher:**
- Use pares com **alto volume** (mais liquidez)
- Use pares que você entende (não escolha aleatoriamente)

---

### 2. **BASE_PRICE** (Preço Base)
**O que é:** O ponto central do seu grid

**Exemplo:**
```
BASE_PRICE = 50000

Grid será criado em torno de 50000:
- Compras abaixo de 50000
- Vendas acima de 50000
```

**Como escolher:**
- Use o **preço atual** do ativo
- Ou um preço que você acha que o ativo vai oscilar

---

### 3. **PRICE_RANGE** (Intervalo de Preço)
**O que é:** A amplitude total do grid (quanto acima e abaixo do preço base)

**Exemplo:**
```
BASE_PRICE = 50000
PRICE_RANGE = 1000

Preço mínimo: 50000 - 500 = 49500
Preço máximo: 50000 + 500 = 50500
```

**Como escolher:**
- **Mercado calmo:** Use 1-2% do preço base
- **Mercado volátil:** Use 3-5% do preço base
- **Muito volátil:** Use 5-10% do preço base

**Exemplo para BTC em 50000:**
```
1% = 500
2% = 1000
3% = 1500
5% = 2500
```

---

### 4. **GRID_LEVELS** (Número de Níveis)
**O que é:** Quantas ordens de compra e quantas de venda você quer

**Exemplo:**
```
GRID_LEVELS = 5

Resultado:
- 5 ordens de COMPRA (abaixo do preço base)
- 5 ordens de VENDA (acima do preço base)
- Total: 10 ordens
```

**Como escolher:**
- **Mais níveis = mais ordens = mais frequência de trades**
- **Menos níveis = menos ordens = menos frequência de trades**

**Recomendações:**
```
Conservador (poucos trades):    GRID_LEVELS = 3
Normal (trades regulares):      GRID_LEVELS = 5-10
Agressivo (muitos trades):      GRID_LEVELS = 15-20
```

---

### 5. **ORDER_SIZE** (Tamanho de Cada Ordem)
**O que é:** Quanto de cada ativo você quer comprar/vender em cada nível

**Exemplo:**
```
ORDER_SIZE = 0.01
GRID_LEVELS = 5

Cada ordem compra/vende 0.01 BTC
Total de BTC envolvido: 0.01 × 5 = 0.05 BTC
```

**Como escolher:**
- Depende do seu **saldo disponível**
- Depende da sua **tolerância ao risco**

**Cálculo do investimento aproximado:**
```
Investimento ≈ ORDER_SIZE × GRID_LEVELS × BASE_PRICE

Exemplo:
0.01 × 5 × 50000 = 2500 USDT
```

---

### 6. **MODE** (Modo de Operação)
**O que é:** Como o bot vai distribuir as ordens

#### **NEUTRAL (Recomendado)**
```
Compra abaixo do preço base
Venda acima do preço base

Ideal para: Mercados laterais (oscilando)
Risco: Médio
Lucro: Constante em oscilações
```

**Exemplo:**
```
BASE_PRICE = 50000

COMPRA em: 49000, 48020, 47059, 46118, 45196
VENDA em:  51000, 52020, 53060, 54121, 55204
```

#### **LONG**
```
Todas as ordens de COMPRA abaixo do preço base
Todas as ordens de VENDA acima do preço base

Ideal para: Mercados em alta (uptrend)
Risco: Baixo (você está comprando)
Lucro: Quando o preço sobe
```

**Exemplo:**
```
BASE_PRICE = 50000

Todas as 10 ordens são de COMPRA entre 45000-50000
Quando preenchidas, vende acima de 50000
```

#### **SHORT**
```
Todas as ordens de VENDA acima do preço base
Todas as ordens de COMPRA abaixo do preço base

Ideal para: Mercados em baixa (downtrend)
Risco: Baixo (você está vendendo primeiro)
Lucro: Quando o preço cai
```

**Exemplo:**
```
BASE_PRICE = 50000

Todas as 10 ordens são de VENDA entre 50000-55000
Quando preenchidas, compra abaixo de 50000
```

---

### 7. **GRID_TYPE** (Tipo de Grid)

#### **GEOMETRIC (Recomendado)**
```
Espaçamento em PERCENTUAL

Cada nível está X% acima/abaixo do anterior

Vantagem: Adapta-se melhor a grandes movimentos
Desvantagem: Mais complexo de entender
```

**Exemplo com GEOMETRIC_PERCENTAGE = 2%:**
```
Nível 1: 50000
Nível 2: 50000 × 1.02 = 51000
Nível 3: 51000 × 1.02 = 52020
Nível 4: 52020 × 1.02 = 53060
...
```

#### **ARITHMETIC**
```
Espaçamento em VALOR FIXO

Cada nível está X unidades acima/abaixo do anterior

Vantagem: Mais simples de entender
Desvantagem: Não se adapta bem a grandes movimentos
```

**Exemplo:**
```
Intervalo: 1000 / 5 = 200 por nível

Nível 1: 50000
Nível 2: 50200
Nível 3: 50400
Nível 4: 50600
...
```

---

## Estratégias Explicadas

### **Estratégia 1: Grid Neutro em Mercado Lateral**

**Quando usar:** Quando o preço está oscilando entre dois valores

**Configuração:**
```python
SYMBOL = "BTC_USDT"
BASE_PRICE = 50000          # Preço atual
PRICE_RANGE = 2000          # ±2% (mercado calmo)
GRID_LEVELS = 10            # Muitos níveis para capturar oscilações
ORDER_SIZE = 0.01
MODE = "NEUTRAL"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 1    # Pequenas diferenças entre níveis
```

**Como funciona:**
1. Cria 10 ordens de compra abaixo de 50000
2. Cria 10 ordens de venda acima de 50000
3. Quando o preço sobe, vende (lucra)
4. Quando o preço cai, compra (lucra)
5. Repete continuamente

**Lucro esperado:** Pequeno lucro em cada oscilação × muitas oscilações

---

### **Estratégia 2: Grid Long em Mercado em Alta**

**Quando usar:** Quando você acha que o preço vai subir

**Configuração:**
```python
SYMBOL = "BTC_USDT"
BASE_PRICE = 50000          # Preço atual ou esperado
PRICE_RANGE = 3000          # ±3% (expectativa de queda antes de subir)
GRID_LEVELS = 5             # Menos níveis
ORDER_SIZE = 0.02           # Maior tamanho (mais confiante)
MODE = "LONG"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 2
```

**Como funciona:**
1. Cria 5 ordens de compra abaixo de 50000 (esperando queda)
2. Se o preço cair, compra barato
3. Quando o preço sobe, vende com lucro
4. Repete

**Lucro esperado:** Maior lucro por trade, menos frequência

---

### **Estratégia 3: Grid Short em Mercado em Baixa**

**Quando usar:** Quando você acha que o preço vai cair

**Configuração:**
```python
SYMBOL = "BTC_USDT"
BASE_PRICE = 50000
PRICE_RANGE = 3000          # ±3% (expectativa de subida antes de cair)
GRID_LEVELS = 5
ORDER_SIZE = 0.02
MODE = "SHORT"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 2
```

**Como funciona:**
1. Cria 5 ordens de venda acima de 50000
2. Se o preço subir, vende caro
3. Quando o preço cai, compra com lucro
4. Repete

**Lucro esperado:** Lucro em mercado em queda

---

### **Estratégia 4: Grid Agressivo (Muitos Trades)**

**Quando usar:** Quando quer capturar muitas pequenas oscilações

**Configuração:**
```python
SYMBOL = "BTC_USDT"
BASE_PRICE = 50000
PRICE_RANGE = 5000          # ±5% (maior amplitude)
GRID_LEVELS = 20            # MUITOS níveis
ORDER_SIZE = 0.005          # Pequeno tamanho (risco distribuído)
MODE = "NEUTRAL"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 1    # Pequenas diferenças
```

**Resultado:**
- 20 ordens de compra
- 20 ordens de venda
- Total: 40 ordens
- Muitos pequenos lucros

**Lucro esperado:** Muitos trades pequenos = lucro consistente

---

### **Estratégia 5: Grid Conservador (Poucos Trades)**

**Quando usar:** Quando quer risco baixo e lucros maiores

**Configuração:**
```python
SYMBOL = "BTC_USDT"
BASE_PRICE = 50000
PRICE_RANGE = 1000          # ±1% (mercado muito calmo)
GRID_LEVELS = 3             # Poucos níveis
ORDER_SIZE = 0.05           # Maior tamanho
MODE = "NEUTRAL"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 3    # Maiores diferenças
```

**Resultado:**
- 3 ordens de compra
- 3 ordens de venda
- Total: 6 ordens
- Poucos trades, mas maiores

**Lucro esperado:** Lucros maiores, menos frequência

---

## Exemplos Práticos

### **Exemplo 1: Bitcoin Oscilando entre 49000-51000**

```python
SYMBOL = "BTC_USDT"
BASE_PRICE = 50000          # Meio do intervalo
PRICE_RANGE = 2000          # Cobre 49000-51000
GRID_LEVELS = 5
ORDER_SIZE = 0.01
MODE = "NEUTRAL"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 2
```

**Resultado:**
```
COMPRA em: 49000, 48020, 47059, 46118, 45196
VENDA em:  51000, 52020, 53060, 54121, 55204
```

Quando o preço oscila entre 49000-51000:
- Vende em 51000, 52020 (lucra)
- Compra em 49000, 48020 (lucra)
- Repete continuamente

---

### **Exemplo 2: Ethereum em Tendência de Alta**

```python
SYMBOL = "ETH_USDT"
BASE_PRICE = 3000           # Preço atual
PRICE_RANGE = 300           # ±5%
GRID_LEVELS = 8
ORDER_SIZE = 0.1
MODE = "LONG"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 2
```

**Estratégia:**
- Espera o preço cair para 2850-2900
- Compra em múltiplos níveis
- Quando sobe, vende com lucro
- Favorece a tendência de alta

---

### **Exemplo 3: Solana em Mercado Muito Volátil**

```python
SYMBOL = "SOL_USDT"
BASE_PRICE = 200
PRICE_RANGE = 40            # ±10% (muito volátil)
GRID_LEVELS = 15            # Muitos níveis
ORDER_SIZE = 1
MODE = "NEUTRAL"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 1.5  # Pequenas diferenças
```

**Estratégia:**
- Cria muitos níveis para capturar volatilidade
- Lucra em cada oscilação
- Distribuir risco em muitas ordens pequenas

---

## Dicas e Boas Práticas

### **1. Escolha o Símbolo Certo**
```
✓ BTC_USDT - Alto volume, previsível
✓ ETH_USDT - Bom volume, segue BTC
✓ SOL_USDT - Médio volume, mais volátil
✗ Altcoins pequenas - Baixo volume, imprevisível
```

### **2. Ajuste o PRICE_RANGE**
```
Se o preço está oscilando muito:
  → Aumente PRICE_RANGE

Se o preço está estável:
  → Diminua PRICE_RANGE

Regra: PRICE_RANGE deve cobrir 80% das oscilações esperadas
```

### **3. Escolha GRID_LEVELS com Cuidado**
```
Mais níveis = Mais ordens = Mais capital necessário

Cálculo:
Capital necessário ≈ ORDER_SIZE × GRID_LEVELS × BASE_PRICE

Exemplo:
0.01 × 10 × 50000 = 5000 USDT
```

### **4. Monitore o Bot**
```
Verifique regularmente:
- Quantas ordens foram preenchidas?
- Qual é o lucro acumulado?
- O preço está fora do PRICE_RANGE?

Se o preço sair do range:
  → Aumente PRICE_RANGE
  → Ou mude o BASE_PRICE
```

### **5. Não Seja Ganancioso**
```
✓ Ganho pequeno e consistente é melhor
✓ 0.5% ao dia = 15% ao mês
✗ Tentar ganhar 10% ao dia = perder tudo

Fórmula simples:
Lucro por trade × Número de trades = Lucro total
```

### **6. Teste Antes de Usar Dinheiro Real**
```
1. Configure o bot com valores pequenos
2. Rode por 1-2 dias
3. Analise os resultados
4. Ajuste se necessário
5. Depois aumente os valores
```

### **7. Gerencie o Risco**
```
Nunca coloque todo seu dinheiro em uma estratégia

Exemplo:
Total: 10000 USDT
  → Grid Trading: 3000 USDT
  → Reserva: 7000 USDT

Assim você não perde tudo se algo der errado
```

---

## Resumo Rápido

| Parâmetro | Conservador | Normal | Agressivo |
|-----------|------------|--------|-----------|
| GRID_LEVELS | 3-5 | 5-10 | 15-20 |
| PRICE_RANGE | 1% | 2-3% | 5-10% |
| ORDER_SIZE | Grande | Médio | Pequeno |
| MODE | NEUTRAL | NEUTRAL | NEUTRAL |
| GRID_TYPE | GEOMETRIC | GEOMETRIC | GEOMETRIC |
| Frequência | Poucos trades | Trades regulares | Muitos trades |
| Risco | Baixo | Médio | Alto |
| Lucro | Pequeno mas seguro | Médio | Grande mas arriscado |

---

## Próximos Passos

1. **Escolha uma estratégia** baseada em seu estilo
2. **Configure o bot** com os parâmetros
3. **Teste com valores pequenos** por 1-2 dias
4. **Analise os resultados**
5. **Ajuste conforme necessário**
6. **Aumente gradualmente** conforme ganha confiança

Boa sorte! 🚀
