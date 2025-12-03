"""
Script de debug para testar criação de uma única ordem
"""

import json
import logging
from backpack_api import BackpackAPI
import auth

# Configurar logging detalhado
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Criar cliente da API
api = BackpackAPI(
    public_key=auth.BACKPACK_PUBLIC_KEY,
    private_key=auth.BACKPACK_PRIVATE_KEY,
)

print("\n" + "="*70)
print("TESTE DE CRIAÇÃO DE ORDEM - DEBUG")
print("="*70)

# 1. Testar conexão
print("\n1️⃣  Testando conexão com a API...")
try:
    ticker = api.get_ticker("BTC_USDT")
    print(f"✓ Conexão OK")
    print(f"  Resposta: {json.dumps(ticker, indent=2)}")
except Exception as e:
    print(f"✗ Erro na conexão: {e}")
    exit(1)

# 2. Criar uma ordem de teste
print("\n2️⃣  Criando uma ordem de teste...")
print("  Parâmetros:")
print("  - Symbol: BTC_USDT")
print("  - Side: Bid (compra)")
print("  - Type: Limit")
print("  - Quantity: 0.001")
print("  - Price: 40000")

try:
    response = api.create_order(
        symbol="BTC_USDT",
        side="BUY",
        order_type="LIMIT",
        quantity=0.001,
        price=40000,
        client_order_id="debug_test_order"
    )
    
    print(f"\n✓ Resposta da API recebida:")
    print(f"  Tipo: {type(response)}")
    print(f"  Conteúdo: {json.dumps(response, indent=2)}")
    
    # Verificar se tem orderId
    if isinstance(response, dict):
        order_id = response.get("orderId")
        if order_id:
            print(f"\n✅ SUCESSO! Ordem criada com ID: {order_id}")
        else:
            print(f"\n⚠️  AVISO: Resposta recebida mas sem orderId")
            print(f"  Chaves na resposta: {list(response.keys())}")
    else:
        print(f"\n⚠️  AVISO: Resposta não é um dicionário")
        
except Exception as e:
    print(f"\n✗ ERRO ao criar ordem: {e}")
    import traceback
    traceback.print_exc()

# 3. Verificar ordens abertas
print("\n3️⃣  Verificando ordens abertas...")
try:
    orders = api.get_open_orders("BTC_USDT")
    print(f"✓ Ordens recebidas:")
    print(f"  Tipo: {type(orders)}")
    print(f"  Conteúdo: {json.dumps(orders, indent=2)}")
    
    if isinstance(orders, list):
        print(f"\n  Total de ordens: {len(orders)}")
        for order in orders:
            print(f"    - ID: {order.get('orderId')}, Status: {order.get('status')}")
    
except Exception as e:
    print(f"\n✗ ERRO ao obter ordens: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("FIM DO TESTE")
print("="*70 + "\n")
