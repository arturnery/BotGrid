"""
Cliente da API da Backpack Exchange
Implementa autenticação ED25519 e requisições assinadas
Documentação: https://docs.backpack.exchange/
"""

import requests
import time
import base64
import json
from typing import Dict, List, Optional, Any
import logging
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class BackpackAPI:
    """Cliente para interagir com a API da Backpack Exchange"""

    def __init__(self, public_key: str, private_key: str, api_url: str = "https://api.backpack.exchange"):
        """
        Inicializa o cliente da API

        Args:
            public_key: Chave pública da API (base64)
            private_key: Chave privada da API (base64)
            api_url: URL base da API
        """
        self.public_key = public_key
        self.private_key = private_key
        self.api_url = api_url
        self.session = requests.Session()
        
        # Validar e carregar as chaves
        self._load_keys()

    def _fix_base64_padding(self, data: str) -> str:
        """Corrige o padding do base64 se necessário"""
        padding = len(data) % 4
        if padding:
            data += '=' * (4 - padding)
        return data
    
    def _load_keys(self):
        """Carrega e valida as chaves ED25519"""
        try:
            from cryptography.hazmat.primitives.asymmetric import ed25519
            
            # Corrigir padding das chaves
            private_key_fixed = self._fix_base64_padding(self.private_key)
            public_key_fixed = self._fix_base64_padding(self.public_key)
            
            # Decodificar chave privada
            self.private_key_bytes = base64.b64decode(private_key_fixed)
            self.private_key_obj = ed25519.Ed25519PrivateKey.from_private_bytes(self.private_key_bytes)
            
            # Decodificar chave pública
            self.public_key_bytes = base64.b64decode(public_key_fixed)
            
            # Verificar que as chaves correspondem
            derived_public = self.private_key_obj.public_key().public_bytes_raw()
            if derived_public != self.public_key_bytes:
                logger.warning("⚠️  Aviso: As chaves pública e privada não correspondem!")
            
            logger.info("✓ Chaves ED25519 carregadas com sucesso")
            
        except Exception as e:
            logger.error(f"✗ Erro ao carregar chaves: {e}")
            raise

    def _generate_signature(self, instruction: str, params: Dict[str, Any]) -> tuple:
        """
        Gera a assinatura ED25519 para a requisição
        
        Segue a especificação da Backpack:
        https://docs.backpack.exchange/#signing-requests
        
        Args:
            instruction: Tipo de instrução (ex: orderExecute, orderCancel)
            params: Parâmetros da requisição
            
        Returns:
            Tupla (signature_b64, timestamp, window)
        """
        # 1. Timestamp em millisegundos
        timestamp = str(int(time.time() * 1000))
        window = "5000"
        
        # 2. Ordenar parâmetros alfabeticamente
        sorted_params = sorted(params.items())
        
        # 3. Construir query string dos parâmetros
        query_parts = [f"{k}={v}" for k, v in sorted_params]
        query_string = "&".join(query_parts)
        
        # 4. Construir string para assinar
        # Formato: instruction&param1=val1&param2=val2&timestamp=X&window=Y
        if query_string:
            sign_string = f"{instruction}&{query_string}&timestamp={timestamp}&window={window}"
        else:
            sign_string = f"{instruction}&timestamp={timestamp}&window={window}"
        
        logger.debug(f"String para assinar: {sign_string}")
        
        # 5. Assinar com a chave privada
        signature = self.private_key_obj.sign(sign_string.encode())
        signature_b64 = base64.b64encode(signature).decode()
        
        logger.debug(f"Assinatura gerada: {signature_b64[:50]}...")
        
        return signature_b64, timestamp, window

    def _make_request(
        self,
        method: str,
        endpoint: str,
        instruction: Optional[str] = None,
        params: Optional[Dict] = None,
        signed: bool = False,
    ) -> Any:
        """
        Faz uma requisição para a API
        
        Args:
            method: GET, POST, DELETE
            endpoint: Endpoint da API (ex: /api/v1/ticker)
            instruction: Tipo de instrução (para requisições assinadas)
            params: Parâmetros da requisição
            signed: Se a requisição deve ser assinada
            
        Returns:
            Resposta da API em JSON
        """
        if params is None:
            params = {}
        
        url = f"{self.api_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        # Preparar requisição assinada
        if signed and instruction:
            signature_b64, timestamp, window = self._generate_signature(instruction, params)
            
            headers["X-API-Key"] = self.public_key
            headers["X-Signature"] = signature_b64
            headers["X-Timestamp"] = timestamp
            headers["X-Window"] = window
            
            # Para requisições POST: parâmetros no corpo (JSON)
            # Para DELETE com orderCancelAll: parâmetros no corpo (JSON)
            # Para GET/DELETE simples: parâmetros na URL
            if method == "POST" or instruction == "orderCancelAll":
                request_body = params
                request_params = None
            else:
                # GET e DELETE simples: parâmetros na URL
                request_body = None
                request_params = params
        else:
            # Requisições não assinadas
            request_body = None
            request_params = params
        
        try:
            logger.debug(f"{method} {url}")
            if request_body:
                logger.debug(f"Body: {json.dumps(request_body)}")
            if request_params:
                logger.debug(f"Params: {request_params}")
            logger.debug(f"Headers: {headers}")
            
            if method == "GET":
                response = self.session.get(url, params=request_params, headers=headers, timeout=10)
            elif method == "POST":
                response = self.session.post(url, json=request_body, params=request_params, headers=headers, timeout=10)
            elif method == "DELETE":
                response = self.session.delete(url, params=request_params, headers=headers, timeout=10)
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            logger.debug(f"Status: {response.status_code}")
            logger.debug(f"Resposta: {response.text[:200]}")
            
            # Tentar fazer parse do JSON
            try:
                result = response.json()
                return result
            except:
                if response.status_code == 200:
                    return {"success": True}
                response.raise_for_status()
                return {}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            raise

    # ============================================================
    # ENDPOINTS PÚBLICOS (sem assinatura)
    # ============================================================

    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Obtém o ticker (preço atual) de um símbolo"""
        return self._make_request("GET", "/api/v1/ticker", params={"symbol": symbol})

    def get_tickers(self) -> List[Dict[str, Any]]:
        """Obtém todos os tickers"""
        return self._make_request("GET", "/api/v1/tickers")

    def get_order_book(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        """Obtém o order book de um símbolo"""
        return self._make_request("GET", "/api/v1/depth", params={"symbol": symbol, "limit": str(limit)})

    def health_check(self) -> bool:
        """Verifica se a API está disponível"""
        try:
            response = self.session.get(f"{self.api_url}/api/v1/tickers", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Erro ao verificar saúde da API: {e}")
            return False

    # ============================================================
    # ENDPOINTS AUTENTICADOS (com assinatura)
    # ============================================================

    def create_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
        client_order_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Cria uma nova ordem
        
        POST /api/v1/order - Parâmetros no CORPO (JSON)
        
        Args:
            symbol: Símbolo do par (ex: BTC_USDT)
            side: Bid (compra) ou Ask (venda)
            order_type: Limit ou Market
            quantity: Quantidade
            price: Preço (necessário para Limit)
            client_order_id: ID customizado da ordem
            
        Returns:
            Dados da ordem criada
        """
        # Converter side para o formato esperado pela Backpack
        backpack_side = "Bid" if side.upper() == "BUY" else "Ask"
        backpack_order_type = "Limit" if order_type.upper() == "LIMIT" else "Market"
        
        params = {
            "symbol": symbol,
            "side": backpack_side,
            "orderType": backpack_order_type,
            "quantity": str(quantity),
        }
        
        if price is not None:
            params["price"] = str(price)
        
        if client_order_id is not None:
            params["clientOrderId"] = client_order_id
        
        logger.info(f"Criando ordem: {side} {quantity} {symbol} @ {price}")
        return self._make_request(
            "POST", "/api/v1/order", instruction="orderExecute", params=params, signed=True
        )

    def cancel_order(self, order_id: str, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Cancela uma ordem
        
        DELETE /api/v1/order - Parâmetros na URL
        """
        params = {"orderId": order_id}
        if symbol:
            params["symbol"] = symbol
        
        logger.info(f"Cancelando ordem: {order_id}")
        return self._make_request(
            "DELETE", "/api/v1/order", instruction="orderCancel", params=params, signed=True
        )

    def cancel_all_orders(self, symbol: str) -> Dict[str, Any]:
        """
        Cancela todas as ordens de um simbolo
        
        DELETE /api/v1/orders - Parametros na URL
        """
        logger.info(f"Cancelando todas as ordens de {symbol}")
        try:
            return self._make_request(
                "DELETE",
                "/api/v1/orders",
                instruction="orderCancelAll",
                params={"symbol": symbol},
                signed=True,
            )
        except Exception as e:
            logger.warning(f"Nao foi possivel cancelar ordens: {e}")
            return {"success": True}

    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Obtém todas as ordens abertas
        
        GET /api/v1/orders - Parâmetros na URL
        """
        params = {}
        if symbol:
            params["symbol"] = symbol
        
        return self._make_request(
            "GET", "/api/v1/orders", instruction="orderQueryAll", params=params, signed=True
        )

    def get_order(self, order_id: str, symbol: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtém detalhes de uma ordem específica
        
        GET /api/v1/order - Parâmetros na URL
        """
        params = {"orderId": order_id}
        if symbol:
            params["symbol"] = symbol
        
        return self._make_request(
            "GET", "/api/v1/order", instruction="orderQuery", params=params, signed=True
        )

    def get_balances(self) -> List[Dict[str, Any]]:
        """
        Obtém os saldos da conta
        
        GET /api/v1/balances - Sem parâmetros
        """
        return self._make_request(
            "GET", "/api/v1/balances", instruction="balanceQuery", params={}, signed=True
        )

    def get_positions(self) -> List[Dict[str, Any]]:
        """
        Obtém as posições abertas
        
        GET /api/v1/positions - Sem parâmetros
        """
        return self._make_request(
            "GET", "/api/v1/positions", instruction="positionQuery", params={}, signed=True
        )

    def get_account_info(self) -> Dict[str, Any]:
        """
        Obtém informações da conta
        
        GET /api/v1/account - Sem parâmetros
        """
        return self._make_request(
            "GET", "/api/v1/account", instruction="accountQuery", params={}, signed=True
        )
