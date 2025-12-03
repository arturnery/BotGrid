# 🚀 Guia Rápido - Grid Trading Bot

## 5 Passos para Começar

### 1️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2️⃣ Adicionar Credenciais (auth.py)

Abra `auth.py` e substitua:

```python
BACKPACK_PUBLIC_KEY = "sua_chave_publica_aqui"
BACKPACK_PRIVATE_KEY = "sua_chave_privada_aqui"
```

### 3️⃣ Configurar Parâmetros (config.py)

Edite os valores principais em `config.py`:

```python
SYMBOL = "BTC-PERP"           # Qual par tradear
BASE_PRICE = 50000            # Preço central
PRICE_RANGE = 2000            # Amplitude do grid
GRID_LEVELS = 5               # Número de níveis
ORDER_SIZE = 0.01             # Tamanho de cada ordem
MODE = "NEUTRAL"              # LONG, SHORT ou NEUTRAL
```

### 4️⃣ Executar o Bot

```bash
python bot.py
```

### 5️⃣ Monitorar e Parar

- O bot mostrará logs no console
- Pressione `Ctrl+C` para parar

## 📊 Exemplos Rápidos

### Bitcoin Agressivo (muitas ordens pequenas)

```python
SYMBOL = "BTC_USDT"
BASE_PRICE = 50000
PRICE_RANGE = 5000
GRID_LEVELS = 20
ORDER_SIZE = 0.001
MODE = "NEUTRAL"
```

### Bitcoin Conservador (poucas ordens grandes)

```python
SYMBOL = "BTC_USDT"
BASE_PRICE = 50000
PRICE_RANGE = 1000
GRID_LEVELS = 3
ORDER_SIZE = 0.1
MODE = "NEUTRAL"
```

### Ethereum Neutro

```python
SYMBOL = "ETH_USDT"
BASE_PRICE = 3000
PRICE_RANGE = 300
GRID_LEVELS = 5
ORDER_SIZE = 0.1
MODE = "NEUTRAL"
```

## 🎯 Modos Explicados

| Modo | Quando Usar | Compra | Venda |
|------|-----------|--------|-------|
| **NEUTRAL** | Mercado lateral | Abaixo | Acima |
| **LONG** | Mercado em alta | Abaixo | Acima |
| **SHORT** | Mercado em baixa | Abaixo | Acima |

## 🔄 Como Funciona

1. **Bot inicia** → Calcula os níveis de grid
2. **Cria ordens** → Coloca todas as ordens nos níveis
3. **Monitora** → Verifica o status a cada 30s
4. **Atualiza** → Se uma ordem preencher, cria uma nova
5. **Lucra** → Cada vez que compra baixo e vende alto

## 📈 Exemplo Visual

```
Preço sobe de 50000 para 51000:
- Ordem de venda em 51000 preenche ✅ (lucra)
- Cria nova ordem de venda em 51000

Preço cai de 50000 para 49000:
- Ordem de compra em 49000 preenche ✅ (lucra)
- Cria nova ordem de compra em 49000

Resultado: Lucra em ambas as direções! 💰
```

## ⚠️ Importante

- **Testnet primeiro**: Use testnet.backpack.exchange para testar
- **Comece pequeno**: Use ORDER_SIZE baixo inicialmente
- **Monitore**: Acompanhe os logs para entender o que está acontecendo
- **Segurança**: Nunca compartilhe suas chaves privadas

## 🆘 Problemas Comuns

**"Erro: Chave não configurada"**
→ Abra auth.py e adicione suas credenciais

**"Erro: Insufficient balance"**
→ Você não tem saldo. Deposite mais ou reduza ORDER_SIZE

**"Nenhuma ordem criada"**
→ Verifique se SYMBOL está correto (ex: BTC-PERP)

## 📚 Próximos Passos

1. Teste na testnet primeiro
2. Comece com valores pequenos
3. Monitore por algumas horas
4. Ajuste os parâmetros conforme necessário
5. Aumente gradualmente os valores

---

**Boa sorte! 🚀**
