"""
Script para testar e validar a geração de assinatura ED25519 para a Backpack API
"""

import base64
import time
from cryptography.hazmat.primitives.asymmetric import ed25519

# Suas credenciais (substitua pelas suas)
PUBLIC_KEY_B64 = "sua_chave_publica_aqui"
PRIVATE_KEY_B64 = "sua_chave_privada_aqui"

def test_signature_generation():
    """Testa a geração de assinatura"""
    
    print("=" * 70)
    print("TESTE DE GERAÇÃO DE ASSINATURA ED25519 - BACKPACK API")
    print("=" * 70)
    
    # 1. Decodificar as chaves
    print("\n1️⃣  Decodificando chaves...")
    try:
        private_key_bytes = base64.b64decode(PRIVATE_KEY_B64)
        public_key_bytes = base64.b64decode(PUBLIC_KEY_B64)
        
        print(f"   ✓ Chave privada decodificada: {len(private_key_bytes)} bytes")
        print(f"   ✓ Chave pública decodificada: {len(public_key_bytes)} bytes")
    except Exception as e:
        print(f"   ✗ Erro ao decodificar chaves: {e}")
        return
    
    # 2. Criar objeto de chave privada
    print("\n2️⃣  Criando objeto de chave privada...")
    try:
        private_key_obj = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
        print("   ✓ Chave privada carregada com sucesso")
    except Exception as e:
        print(f"   ✗ Erro ao carregar chave privada: {e}")
        return
    
    # 3. Verificar que a chave pública corresponde
    print("\n3️⃣  Verificando correspondência de chaves...")
    try:
        derived_public_key = private_key_obj.public_key().public_bytes_raw()
        if derived_public_key == public_key_bytes:
            print("   ✓ Chaves correspondem corretamente")
        else:
            print("   ✗ AVISO: Chaves NÃO correspondem!")
            print(f"     Esperado: {base64.b64encode(public_key_bytes).decode()}")
            print(f"     Obtido:   {base64.b64encode(derived_public_key).decode()}")
    except Exception as e:
        print(f"   ✗ Erro ao verificar chaves: {e}")
    
    # 4. Testar assinatura com um exemplo simples
    print("\n4️⃣  Testando assinatura com exemplo simples...")
    
    # Exemplo da documentação: cancelar ordem
    params = {
        "orderId": "28",
        "symbol": "BTC_USDT"
    }
    instruction = "orderCancel"
    timestamp = "1614550000000"
    window = "5000"
    
    # Construir string de assinatura
    sorted_params = sorted(params.items())
    query_string = "&".join([f"{k}={v}" for k, v in sorted_params])
    
    # String para assinar: instruction&param1=val1&param2=val2&timestamp=X&window=Y
    sign_string = f"{instruction}&{query_string}&timestamp={timestamp}&window={window}"
    
    print(f"   Instrução: {instruction}")
    print(f"   Parâmetros: {params}")
    print(f"   Timestamp: {timestamp}")
    print(f"   Window: {window}")
    print(f"\n   String para assinar:")
    print(f"   {sign_string}")
    
    # Assinar
    try:
        signature = private_key_obj.sign(sign_string.encode())
        signature_b64 = base64.b64encode(signature).decode()
        
        print(f"\n   ✓ Assinatura gerada com sucesso")
        print(f"   Assinatura (base64): {signature_b64}")
        print(f"   Tamanho da assinatura: {len(signature)} bytes")
    except Exception as e:
        print(f"   ✗ Erro ao gerar assinatura: {e}")
        return
    
    # 5. Testar com um exemplo de criação de ordem
    print("\n5️⃣  Testando assinatura para criação de ordem...")
    
    order_params = {
        "symbol": "BTC_USDT",
        "side": "Bid",
        "orderType": "Limit",
        "quantity": "0.01",
        "price": "45196.03984"
    }
    instruction = "orderExecute"
    timestamp = str(int(time.time() * 1000))
    window = "5000"
    
    # Construir string de assinatura
    sorted_params = sorted(order_params.items())
    query_string = "&".join([f"{k}={v}" for k, v in sorted_params])
    
    # String para assinar
    sign_string = f"{instruction}&{query_string}&timestamp={timestamp}&window={window}"
    
    print(f"   Instrução: {instruction}")
    print(f"   Parâmetros: {order_params}")
    print(f"   Timestamp: {timestamp}")
    print(f"   Window: {window}")
    print(f"\n   String para assinar:")
    print(f"   {sign_string}")
    
    # Assinar
    try:
        signature = private_key_obj.sign(sign_string.encode())
        signature_b64 = base64.b64encode(signature).decode()
        
        print(f"\n   ✓ Assinatura gerada com sucesso")
        print(f"   Assinatura (base64): {signature_b64}")
    except Exception as e:
        print(f"   ✗ Erro ao gerar assinatura: {e}")
        return
    
    print("\n" + "=" * 70)
    print("✅ TESTE CONCLUÍDO COM SUCESSO")
    print("=" * 70)
    print("\nHeaders para enviar na requisição:")
    print(f"X-API-Key: {PUBLIC_KEY_B64}")
    print(f"X-Signature: {signature_b64}")
    print(f"X-Timestamp: {timestamp}")
    print(f"X-Window: {window}")


if __name__ == "__main__":
    test_signature_generation()
