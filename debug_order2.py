"""
Script de debug para testar criação de ordem SEM clientOrderId
"""

import json
import logging
from backpack_api import BackpackAPI
import auth

# Configurar logging detalhado
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar cliente da API
api = BackpackAPI(
    public_key=auth.BACKPACK_PUBLIC_KEY,
    private_key=auth.BACKPACK_PRIVATE_KEY,
)

print("\n" + "="*70)
print("TESTE DE CRIAÇÃO DE ORDEM - SEM clientOrderId")
print("="*70)

# Testar criação de ordem SEM clientOrderId
print("\nCriando ordem SEM clientOrderId...")

try:
    response = api.create_order(
        symbol="BTC_USDT",
        side="BUY",
        order_type="LIMIT",
        quantity=0.001,
        price=40000,
        client_order_id=None  # SEM clientOrderId
    )
    
    print(f"\n✓ Resposta da API:")
    print(json.dumps(response, indent=2))
    
    if isinstance(response, dict) and response.get("orderId"):
        print(f"\n✅ SUCESSO! Ordem criada com ID: {response['orderId']}")
    else:
        print(f"\n⚠️  Resposta recebida mas sem orderId")
        
except Exception as e:
    print(f"\n✗ ERRO: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70 + "\n")
