# =============================================================================
# CONFIGURAÇÕES DO BOT DE GRID TRADING - BACKPACK EXCHANGE
# =============================================================================

# -----------------------------------------------------------------------------
# Par de Trading - FUTUROS PERPÉTUOS
# -----------------------------------------------------------------------------
SYMBOL = "BTC_USDC_PERP"  # Pares: SOL_USDC_PERP, BTC_USDC_PERP, ETH_USDC_PERP

# -----------------------------------------------------------------------------
# Configurações do Grid (AUTOMÁTICO baseado no preço de mercado)
# -----------------------------------------------------------------------------
# O bot busca o preço atual automaticamente e calcula o range
# Range: ±10% do preço atual (ex: se SOL = $141, grid de $127 a $155)

MODE = "LONG"  # LONG, SHORT ou NEUTRAL
PRICE_DECIMAL = 2  # Casas decimais do preço
NUMBER_OF_GRIDS = 20  # Número de níveis do grid
QUANTITY_PER_GRID = 0.0001  # Quantidade por nível

# Explicação dos Modos:
# NEUTRAL: 50% compra + 50% venda (mercado lateral)
# LONG: 70% compra + 30% venda (expectativa de alta)
# SHORT: 30% compra + 70% venda (expectativa de baixa)

# -----------------------------------------------------------------------------
# Configurações Avançadas
# -----------------------------------------------------------------------------
UPDATE_INTERVAL = 30  # Intervalo de verificação (segundos)
CANCEL_ON_EXIT = True  # Cancelar ordens ao sair
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
MAX_RETRIES = 3
RETRY_DELAY = 2

# =============================================================================
# EXEMPLOS PRÉ-CONFIGURADOS
# =============================================================================

# SOL Perpétuo (padrão)
"""
SYMBOL = "SOL_USDC_PERP"
NUMBER_OF_GRIDS = 100
QUANTITY_PER_GRID = 0.07
PRICE_DECIMAL = 2
"""

# BTC Perpétuo
"""
SYMBOL = "BTC_USDC_PERP"
NUMBER_OF_GRIDS = 100
QUANTITY_PER_GRID = 0.001
PRICE_DECIMAL = 2
"""

# ETH Perpétuo
"""
SYMBOL = "ETH_USDC_PERP"
NUMBER_OF_GRIDS = 100
QUANTITY_PER_GRID = 0.01
PRICE_DECIMAL = 2
"""

# =============================================================================
# NOTAS IMPORTANTES
# =============================================================================
# 
# - O bot calcula automaticamente o range como ±10% do preço de mercado
# - Capital necessário: ~$435 USDC para SOL com essas configurações
# - Reduza NUMBER_OF_GRIDS ou QUANTITY_PER_GRID se tiver pouco capital
# - Para testar: use NUMBER_OF_GRIDS = 10 e QUANTITY_PER_GRID = 0.01
#