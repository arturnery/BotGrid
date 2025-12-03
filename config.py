"""
Arquivo de Configuração - Grid Trading Bot
Ajuste os parâmetros abaixo para customizar o comportamento do bot
"""

# ============================================
# CONFIGURAÇÕES DO GRID TRADING
# ============================================

# Par de trading (símbolo do futuro perpétuo)
# Exemplos: "BTC_USDT", "ETH_USDT", "SOL_USDT"
# IMPORTANTE: Use underscore (_) não hífem (-)
SYMBOL = "BTC_USDT"

# Preço base do grid (ponto central)
# O bot criará ordens acima e abaixo deste preço
BASE_PRICE = 50000

# Intervalo de preço total (amplitude do grid)
# Exemplo: Se BASE_PRICE=50000 e PRICE_RANGE=2000
# As ordens serão criadas entre 49000 e 51000
PRICE_RANGE = 1000

# Número de níveis de grid (quantidade de ordens acima e abaixo do preço base)
# Exemplo: Se GRID_LEVELS=5, terá 5 ordens de compra e 5 de venda (total 10)
GRID_LEVELS = 5

# Tamanho de cada ordem (quantidade de ativos)
# Exemplo: 0.01 BTC por ordem
ORDER_SIZE = 0.01

# ============================================
# MODO DE OPERAÇÃO
# ============================================

# LONG: Apenas compra abaixo e vende acima (para mercados em alta)
# SHORT: Apenas venda acima e compra abaixo (para mercados em baixa)
# NEUTRAL: Compra e venda em ambos os lados (para mercados laterais)
MODE = "NEUTRAL"  # Opções: "LONG", "SHORT", "NEUTRAL"

# ============================================
# TIPO DE GRID
# ============================================

# GEOMETRIC: Diferença percentual fixa entre níveis (recomendado)
# ARITHMETIC: Diferença de preço fixa entre níveis
GRID_TYPE = "GEOMETRIC"  # Opções: "GEOMETRIC", "ARITHMETIC"

# Percentual de diferença entre níveis (para GEOMETRIC)
# Exemplo: 2 = 2% de diferença entre cada nível
GEOMETRIC_PERCENTAGE = 2

# Diferença de preço fixa entre níveis (para ARITHMETIC)
# Exemplo: 100 = $100 de diferença entre cada nível
ARITHMETIC_STEP = 100

# ============================================
# COMPORTAMENTO DO BOT
# ============================================

# Intervalo de atualização do bot (em segundos)
# O bot verificará o status das ordens a cada X segundos
UPDATE_INTERVAL = 30

# Cancelar todas as ordens antes de iniciar?
# True: Cancela todas as ordens existentes e começa do zero
# False: Continua com as ordens existentes
CANCEL_EXISTING_ORDERS = True

# Criar novas ordens automaticamente quando uma for preenchida?
# True: Cria novas ordens para manter o grid completo
# False: Apenas monitora as ordens existentes
AUTO_REORDER = True

# ============================================
# GERENCIAMENTO DE RISCO (OPCIONAL)
# ============================================

# Lucro alvo total (em USDT) - o bot parará quando atingir este lucro
# Deixe como None para desabilitar
TARGET_PROFIT = None  # Exemplo: 1000 (para parar ao ganhar $1000)

# Perda máxima permitida (em USDT) - o bot parará se perder mais que isto
# Deixe como None para desabilitar
MAX_LOSS = None  # Exemplo: 500 (para parar ao perder $500)

# ============================================
# LOGGING E DEBUG
# ============================================

# Nível de log: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = "INFO"

# Salvar logs em arquivo?
SAVE_LOGS = True

# Nome do arquivo de log
LOG_FILE = "grid_bot.log"

# Mostrar detalhes de cada ordem no console?
VERBOSE = True

# ============================================
# EXEMPLO DE CONFIGURAÇÕES PRÉ-DEFINIDAS
# ============================================

# Você pode criar diferentes configurações e trocar entre elas
# Descomente a que quiser usar

# --- Configuração Agressiva (muitos níveis, pequenas ordens) ---
# GRID_LEVELS = 20
# ORDER_SIZE = 0.001
# PRICE_RANGE = 5000
# GEOMETRIC_PERCENTAGE = 1

# --- Configuração Conservadora (poucos níveis, ordens maiores) ---
# GRID_LEVELS = 3
# ORDER_SIZE = 0.1
# PRICE_RANGE = 1000
# GEOMETRIC_PERCENTAGE = 5

# --- Configuração para ETH ---
# SYMBOL = "ETH_USDT"
# BASE_PRICE = 3000
# PRICE_RANGE = 300
# ORDER_SIZE = 0.1
# GRID_LEVELS = 5

# --- Configuração para SOL ---
# SYMBOL = "SOL_USDT"
# BASE_PRICE = 200
# PRICE_RANGE = 50
# ORDER_SIZE = 1
# GRID_LEVELS = 5
