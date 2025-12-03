# 🤖 Bot de Grid Trading para Backpack Exchange

Bot automatizado de grid trading para a Backpack Exchange, desenvolvido em Python. Permite executar estratégias de grid trading com configuração simples e fácil.

## ✨ Funcionalidades

- ✅ **Grid Trading Automático**: Cria ordens em múltiplos níveis de preço
- 📊 **Três Modos**: LONG (alta), SHORT (baixa), NEUTRAL (lateral)
- 📈 **Dois Tipos de Grid**: Geométrico (recomendado) e Aritmético
- 🔄 **Loop Contínuo**: Monitora e atualiza ordens automaticamente
- 📝 **Logs Detalhados**: Acompanhe tudo que o bot está fazendo
- ⚙️ **Configuração Simples**: Tudo em arquivos Python fáceis de editar

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Conta na Backpack Exchange com chaves de API

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/arturnery/BotGrid.git
cd BotGrid
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure suas credenciais

Abra o arquivo `auth.py` e adicione suas credenciais da Backpack:

```python
BACKPACK_PUBLIC_KEY = "sua_chave_publica_aqui"
BACKPACK_PRIVATE_KEY = "sua_chave_privada_aqui"
```

**Como obter as chaves:**
1. Acesse [https://backpack.exchange](https://backpack.exchange)
2. Vá para Configurações → API
3. Clique em "Criar Nova Chave de API"
4. Copie a chave pública e privada

⚠️ **IMPORTANTE**: Nunca compartilhe suas chaves privadas!

### 4. Configure os parâmetros

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

## ▶️ Como Usar

### Iniciar o bot

```bash
python bot.py
```

### Parar o bot

Pressione `Ctrl+C` no terminal

## 📊 Exemplos de Configuração

### Bitcoin (BTC)

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

### Ethereum (ETH)

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

### Solana (SOL)

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

### NEUTRAL (Neutro)
- Preço sobe: ↑ vende, lucra
- Preço desce: ↓ compra, lucra
- Preço lateral: ↔ compra e vende, lucra

**Melhor para**: Mercados laterais com alta volatilidade

### LONG (Comprado)
- Preço sobe: ↑ vende, lucra
- Preço desce: ↓ compra, lucra (menos ordens)

**Melhor para**: Tendências de alta

### SHORT (Vendido)
- Preço sobe: ↑ vende, lucra (menos ordens)
- Preço desce: ↓ compra, lucra

**Melhor para**: Tendências de baixa

## 📐 Tipos de Grid

### GEOMETRIC (Geométrico) - Recomendado

Usa percentual fixo entre níveis. Melhor para diferentes volatilidades.

**Exemplo com 2% de diferença:**
- Nível 1: 50000 * 0.98 = 49000 (compra)
- Nível 2: 50000 * 0.96 = 48000 (compra)
- Nível 3: 50000 * 1.02 = 51000 (venda)
- Nível 4: 50000 * 1.04 = 52000 (venda)

### ARITHMETIC (Aritmético)

Usa diferença de preço fixa entre níveis. Mais simples.

**Exemplo com $100 de diferença:**
- Nível 1: 50000 - 100 = 49900 (compra)
- Nível 2: 50000 - 200 = 49800 (compra)
- Nível 3: 50000 + 100 = 50100 (venda)
- Nível 4: 50000 + 200 = 50200 (venda)

## 📁 Estrutura do Projeto

```
BotGrid/
├── bot.py              # Script principal do bot
├── auth.py             # Autenticação com a API
├── config.py           # Configurações do bot
├── grid.py             # Lógica da estratégia de grid
├── orders.py           # Gerenciamento de ordens
├── requirements.txt    # Dependências Python
├── grid_bot.log       # Arquivo de logs (gerado automaticamente)
└── README.md          # Este arquivo
```

## 📝 Logs

Os logs são salvos em `grid_bot.log` e também exibidos no console.

Você pode ajustar o nível de log em `config.py`:

```python
LOG_LEVEL = "INFO"  # Opções: DEBUG, INFO, WARNING, ERROR
```

## 🔐 Segurança

- ⚠️ Nunca compartilhe suas chaves privadas com ninguém
- 🚫 Não faça commit do arquivo `auth.py` em repositórios públicos
- 🧪 Use testnet para testar antes de usar fundos reais
- 💰 Comece pequeno com valores baixos

### Usar Testnet

Para testar sem risco, use a testnet:

1. Acesse [https://testnet.backpack.exchange](https://testnet.backpack.exchange)
2. Crie uma conta de teste
3. Gere chaves de API para testnet
4. Em `auth.py`, mude:

```python
BACKPACK_API_URL = "https://api.testnet.backpack.exchange"
```

## ❓ Problemas Comuns

### "Configure suas chaves de API"

**Solução**: Abra `auth.py` e adicione suas credenciais

### "Insufficient balance"

**Solução**: Você não tem saldo suficiente. Deposite mais fundos ou reduza o tamanho das ordens.

### "Invalid symbol"

**Solução**: Verifique se o símbolo está correto (ex: BTC_USDT, ETH_USDT). Use underscore (_) não hífen (-)

### "Order placement failed"

**Solução**:
- Verifique se as credenciais estão corretas
- Verifique se tem saldo disponível
- Verifique os logs para mais detalhes

## 📚 Recursos

Para mais informações sobre a API da Backpack:
- [Documentação oficial da API](https://docs.backpack.exchange/)

## ⚠️ Disclaimer

Este bot é fornecido "como está" sem garantias. O trading de criptomoedas envolve risco significativo de perda. Sempre:

- Faça sua própria pesquisa (DYOR)
- Teste em testnet primeiro
- Comece com valores pequenos
- Nunca invista mais do que pode perder

## 📄 Licença

Este projeto é open source e está disponível para uso livre.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

---

**Desenvolvido para traders que querem automatizar suas estratégias de grid trading** 🚀