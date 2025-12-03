import time
import base64
import requests
from typing import Dict, Optional
import logging
from cryptography.hazmat.primitives.asymmetric import ed25519

logger = logging.getLogger(__name__)

# IMPORTANTE: Adicione suas credenciais aqui
BACKPACK_PUBLIC_KEY = "t/GREKzC4kAIiyMJb0Ul4/ekWKjLj7W1/oGpeZ+0LTU="
BACKPACK_PRIVATE_KEY = "gzGF1iro55IsDavLVNzogylSHSXAnM6woU8uC7V0wC8="

# URL da API (mude para testnet se necessário)
BACKPACK_API_URL = "https://api.backpack.exchange"
# Para testnet use: BACKPACK_API_URL = "https://api.testnet.backpack.exchange"

# Mapeamento de endpoints para instruções
ENDPOINT_INSTRUCTIONS = {
    '/api/v1/capital': 'balanceQuery',
    '/api/v1/order': 'orderExecute',
    '/api/v1/orders': 'orderQueryAll',
    '/api/v1/order/cancel': 'orderCancel',
    '/api/v1/fills': 'fillHistoryQueryAll',
    '/wapi/v1/capital/deposit/address': 'depositAddressQuery',
}


class BackpackAuth:
    def __init__(self):
        self.public_key = BACKPACK_PUBLIC_KEY
        self.private_key_b64 = BACKPACK_PRIVATE_KEY
        self.api_url = BACKPACK_API_URL
        
        if self.public_key == "sua_chave_publica_aqui":
            raise ValueError("Configure suas chaves de API no arquivo auth.py!")
        
        # Carrega a chave privada ED25519
        try:
            private_key_bytes = base64.b64decode(self.private_key_b64)
            self.private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
            logger.info("✅ Chave privada ED25519 carregada com sucesso")
        except Exception as e:
            logger.error(f"❌ Erro ao carregar chave privada: {e}")
            raise ValueError("Chave privada inválida. Verifique se copiou corretamente da Backpack.")
    
    def _get_instruction(self, endpoint: str, method: str) -> str:
        """Obtém a instrução correta para o endpoint"""
        if method == 'DELETE':
            return 'orderCancel'
        return ENDPOINT_INSTRUCTIONS.get(endpoint, 'balanceQuery')
    
    def _build_signature_string(self, instruction: str, params: Optional[Dict], 
                               timestamp: int, window: int) -> str:
        """Constrói a string de assinatura conforme documentação Backpack"""
        sign_str = f"instruction={instruction}"
        
        if params:
            # Ordena os parâmetros alfabeticamente
            sorted_params_list = []
            for key, value in sorted(params.items()):
                # Booleanos devem ser lowercase
                if isinstance(value, bool):
                    value = str(value).lower()
                sorted_params_list.append(f"{key}={value}")
            
            sorted_params = "&".join(sorted_params_list)
            if sorted_params:
                sign_str += "&" + sorted_params
        
        sign_str += f"&timestamp={timestamp}&window={window}"
        return sign_str
    
    def _generate_signature(self, sign_str: str) -> str:
        """Gera assinatura ED25519"""
        logger.debug(f"String para assinar: {sign_str}")
        
        # Assina com ED25519
        signature_bytes = self.private_key.sign(sign_str.encode('utf-8'))
        
        # Retorna em base64
        encoded_signature = base64.b64encode(signature_bytes).decode('utf-8')
        return encoded_signature
    
    def _get_headers(self, timestamp: int, window: int, signature: str) -> Dict[str, str]:
        """Retorna headers para requisição autenticada"""
        return {
            'X-API-Key': self.public_key,
            'X-Signature': signature,
            'X-Timestamp': str(timestamp),
            'X-Window': str(window),
            'Content-Type': 'application/json; charset=utf-8'
        }
    
    def make_request(self, method: str, endpoint: str, 
                     params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict:
        """Faz uma requisição autenticada à API"""
        timestamp = int(time.time() * 1000)  # Milissegundos
        window = 5000  # 5 segundos
        
        # Obtém a instrução correta
        instruction = self._get_instruction(endpoint, method)
        
        # Prepara parâmetros para a assinatura
        request_params = params if method.upper() == 'GET' else data
        
        # Constrói a string de assinatura
        sign_str = self._build_signature_string(instruction, request_params, timestamp, window)
        
        # Gera assinatura
        signature = self._generate_signature(sign_str)
        
        # Monta headers
        headers = self._get_headers(timestamp, window, signature)
        
        # URL completa
        url = f"{self.api_url}{endpoint}"
        
        logger.debug(f"Request: {method} {url}")
        logger.debug(f"Instruction: {instruction}")
        
        # Faz requisição
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, json=data, timeout=10)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            # Log da resposta
            logger.debug(f"Status: {response.status_code}")
            logger.debug(f"Response: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Resposta: {e.response.text}")
            raise
    
    def test_connection(self) -> bool:
        """Testa a conexão com a API"""
        try:
            # Tenta obter informações da conta
            logger.info("Testando conexão com a API...")
            result = self.make_request('GET', '/api/v1/capital')
            logger.info("✅ Conexão com API estabelecida com sucesso!")
            logger.info(f"Saldo disponível: {result}")
            return True
        except Exception as e:
            logger.error(f"❌ Falha ao conectar: {e}")
            return False
    
    def get_account_balance(self) -> Dict:
        """Obtém saldo da conta"""
        return self.make_request('GET', '/api/v1/capital')
    
    def get_ticker(self, symbol: str) -> Dict:
        """Obtém preço atual do par"""
        # Ticker é endpoint público, não precisa de autenticação
        url = f"{self.api_url}/api/v1/ticker"
        try:
            response = requests.get(url, params={'symbol': symbol}, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao obter ticker: {e}")
            raise