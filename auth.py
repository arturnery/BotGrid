"""
Arquivo de Autenticação - Backpack Exchange
Coloque suas credenciais aqui para acessar a API da Backpack
"""

# ============================================
# SUAS CREDENCIAIS DA BACKPACK
# ============================================

# Sua chave pública da API (Public Key)
# Obtenha em: https://backpack.exchange -> Configurações -> API
BACKPACK_PUBLIC_KEY = ""

# Sua chave privada da API (Private Key)
# ⚠️ NUNCA compartilhe esta chave com ninguém!
# Obtenha em: https://backpack.exchange -> Configurações -> API
BACKPACK_PRIVATE_KEY = ""

# URL da API da Backpack
BACKPACK_API_URL = "https://api.backpack.exchange"

# ============================================
# CONFIGURAÇÕES OPCIONAIS
# ============================================

# Timeout para requisições (em segundos)
REQUEST_TIMEOUT = 10

# Intervalo entre requisições (em segundos) - para não sobrecarregar a API
REQUEST_DELAY = 1

# Modo de teste (True = testnet, False = mainnet)
# Mude para True se quiser testar com a testnet
TESTNET_MODE = False

# Se usar testnet, descomente a linha abaixo e comente a de cima
# BACKPACK_API_URL = "https://api.testnet.backpack.exchange"
