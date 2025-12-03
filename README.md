# Grid Trading Bot - Versão Simples

Um bot de grid trading simples e prático para rodar localmente na sua máquina. Perfeito para automatizar suas estratégias de trading em futuros perpétuos na **Backpack Exchange**.

## 🚀 Características

- **Grid Trading Automático**: Cria ordens em múltiplos níveis de preço
- **Três Modos**: LONG (alta), SHORT (baixa), NEUTRAL (lateral)
- **Dois Tipos de Grid**: Geométrico (recomendado) e Aritmético
- **Loop Contínuo**: Monitora e atualiza ordens automaticamente
- **Logs Detalhados**: Acompanhe tudo que o bot está fazendo
- **Configuração Simples**: Tudo em arquivos Python fáceis de editar

## 📋 Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)
- Conta na Backpack Exchange com chaves de API

## 🔧 Instalação

### 1. Clonar ou baixar o projeto

```bash
cd grid_bot_simple
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Configurar Autenticação (`auth.py`)

Abra o arquivo `auth.py` e adicione suas credenciais da Backpack:

```python
BACKPACK_PUBLIC_KEY = "sua_chave_publica_aqui"
BACKPACK_PRIVATE_KEY = "sua_chave_privada_aqui"
```

**Como obter as chaves:**
1. Acesse https://backpack.exchange
2. Vá para Configurações → API
3. Clique em "Criar Nova Chave de API"
4. Copie a chave pública e privada

### 2. Configurar Parâmetros do Bot (`config.py`)

Abra o arquivo `config.py` e ajuste os parâmetros:

```python
# Par de trading
SYMBOL = "BTC_USDT"

# Preço base (ponto central do grid)
BASE_PRICE = 50000

# Intervalo de preço total
PRICE_RANGE = 1000

# Número de níveis (5 = 5 compras + 5 vendas)
GRID_LEVELS = 5

# Tamanho de cada ordem
ORDER_SIZE = 0.01

# Modo: LONG, SHORT ou NEUTRAL
MODE = "NEUTRAL"

# Tipo de grid: GEOMETRIC ou ARITHMETIC
GRID_TYPE = "GEOMETRIC"

# Intervalo de atualização (segundos)
UPDATE_INTERVAL = 30
```

## 🏃 Executando o Bot

### Iniciar o bot

```bash
python bot.py
```

### Parar o bot

Pressione `Ctrl+C` no terminal

## 📊 Exemplo de Configuração

### Para Bitcoin (BTC_USDT)

```python
SYMBOL = "BTC_USDT"
BASE_PRICE = 50000
PRICE_RANGE = 1000
GRID_LEVELS = 5
ORDER_SIZE = 0.01
MODE = "NEUTRAL"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 2
```

### Para Ethereum (ETH_USDT)

```python
SYMBOL = "ETH_USDT"
BASE_PRICE = 3000
PRICE_RANGE = 300
GRID_LEVELS = 5
ORDER_SIZE = 0.1
MODE = "NEUTRAL"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 2
```

### Para Solana (SOL_USDT)

```python
SYMBOL = "SOL_USDT"
BASE_PRICE = 200
PRICE_RANGE = 50
GRID_LEVELS = 5
ORDER_SIZE = 1
MODE = "NEUTRAL"
GRID_TYPE = "GEOMETRIC"
GEOMETRIC_PERCENTAGE = 2
```

## 🎯 Modos de Operação

### NEUTRAL (Recomendado para mercados laterais)

```
Preço sobe:     ↑ vende, lucra
Preço desce:    ↓ compra, lucra
Preço lateral:  ↔ compra e vende, lucra
```

### LONG (Para mercados em alta)

```
Preço sobe:     ↑ vende, lucra
Preço desce:    ↓ compra, lucra (menos ordens)
```

### SHORT (Para mercados em baixa)

```
Preço sobe:     ↑ vende, lucra (menos ordens)
Preço desce:    ↓ compra, lucra
```

## 📈 Tipos de Grid

### GEOMETRIC (Recomendado)

Usa percentual fixo entre níveis. Melhor para diferentes volatilidades.

```
Exemplo com 2% de diferença:
Nível 1: 50000 * 0.98 = 49000 (compra)
Nível 2: 50000 * 0.96 = 48000 (compra)
Nível 3: 50000 * 1.02 = 51000 (venda)
Nível 4: 50000 * 1.04 = 52000 (venda)
```

### ARITHMETIC

Usa diferença de preço fixa entre níveis. Mais simples.

```
Exemplo com $100 de diferença:
Nível 1: 50000 - 100 = 49900 (compra)
Nível 2: 50000 - 200 = 49800 (compra)
Nível 3: 50000 + 100 = 50100 (venda)
Nível 4: 50000 + 200 = 50200 (venda)
```

## 📝 Logs

Os logs são salvos em `grid_bot.log` e também exibidos no console.

Você pode ajustar o nível de log em `config.py`:

```python
LOG_LEVEL = "INFO"  # Opções: DEBUG, INFO, WARNING, ERROR
```

## ⚠️ Segurança

- **Nunca compartilhe suas chaves privadas** com ninguém
- **Não faça commit** do arquivo `auth.py` em repositórios públicos
- **Use testnet** para testar antes de usar fundos reais
- **Comece pequeno** com valores baixos

## 🧪 Testnet

Para testar sem risco, use a testnet:

1. Acesse https://testnet.backpack.exchange
2. Crie uma conta de teste
3. Gere chaves de API para testnet
4. Em `auth.py`, mude:

```python
BACKPACK_API_URL = "https://api.testnet.backpack.exchange"
```

## 🐛 Troubleshooting

### Erro: "Chave pública não foi configurada"

**Solução**: Abra `auth.py` e adicione suas credenciais

### Erro: "Insufficient balance"

**Solução**: Você não tem saldo suficiente. Deposite mais fundos ou reduza o tamanho das ordens.

### Erro### Invalid symbol

**Solução**: Verifique se o símbolo está correto (ex: BTC_USDT, ETH_USDT). Use underscore (_) não hífem (-)

### Bot não cria ordens

**Solução**:
1. Verifique se as credenciais estão corretas
2. Verifique se tem saldo disponível
3. Verifique os logs para mais detalhes

## 📞 Suporte

Para mais informações sobre a API da Backpack:
- https://docs.backpack.exchange
- https://support.backpack.exchange

## ⚖️ Disclaimer

Este bot é fornecido "como está" sem garantias. O trading de criptomoedas envolve risco significativo. Sempre teste em testnet antes de usar com fundos reais.

---

**Desenvolvido para traders que querem automatizar suas estratégias de grid trading** 🚀
