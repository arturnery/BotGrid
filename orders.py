import logging
import time
from typing import List, Dict, Optional
from config import MAX_RETRIES, RETRY_DELAY

logger = logging.getLogger(__name__)


class OrderManager:
    def __init__(self, auth):
        """
        Inicializa o gerenciador de ordens
        
        Args:
            auth: Instância de BackpackAuth para fazer requisições
        """
        self.auth = auth
    
    def place_limit_order(self, symbol: str, side: str, price: float, 
                         quantity: float) -> Optional[Dict]:
        """
        Coloca uma ordem limit
        
        Args:
            symbol: Par de trading (ex: BTC_USDT)
            side: 'Bid' para compra, 'Ask' para venda
            price: Preço da ordem
            quantity: Quantidade
            
        Returns:
            Resposta da API ou None se falhar
        """
        for attempt in range(MAX_RETRIES):
            try:
                data = {
                    'orderType': 'Limit',
                    'side': side,
                    'symbol': symbol,
                    'price': str(price),
                    'quantity': str(quantity),
                    'timeInForce': 'GTC'  # Good Till Cancel
                }
                
                result = self.auth.make_request('POST', '/api/v1/order', data=data)
                
                side_name = "COMPRA" if side == "Bid" else "VENDA"
                logger.info(f"✓ Ordem de {side_name} colocada: {quantity} @ ${price}")
                
                return result
                
            except Exception as e:
                logger.warning(f"Tentativa {attempt + 1}/{MAX_RETRIES} falhou: {e}")
                
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"Falha ao colocar ordem após {MAX_RETRIES} tentativas")
                    return None
    
    def cancel_order(self, symbol: str, order_id: str) -> bool:
        """
        Cancela uma ordem específica
        
        Args:
            symbol: Par de trading
            order_id: ID da ordem
            
        Returns:
            True se cancelada com sucesso
        """
        try:
            data = {
                'symbol': symbol,
                'orderId': order_id
            }
            
            self.auth.make_request('DELETE', '/api/v1/order', data=data)
            logger.info(f"Ordem {order_id} cancelada")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao cancelar ordem {order_id}: {e}")
            return False
    
    def cancel_all_orders(self, symbol: str) -> int:
        """
        Cancela todas as ordens abertas de um símbolo
        
        Args:
            symbol: Par de trading
            
        Returns:
            Número de ordens canceladas
        """
        try:
            # Obtém todas as ordens abertas
            open_orders = self.get_open_orders(symbol)
            
            if not open_orders:
                logger.info("Nenhuma ordem aberta para cancelar")
                return 0
            
            cancelled = 0
            for order in open_orders:
                if self.cancel_order(symbol, order['id']):
                    cancelled += 1
                time.sleep(0.2)  # Evita rate limit
            
            logger.info(f"Total de {cancelled} ordens canceladas")
            return cancelled
            
        except Exception as e:
            logger.error(f"Erro ao cancelar todas as ordens: {e}")
            return 0
    
    def get_open_orders(self, symbol: str) -> List[Dict]:
        """
        Obtém todas as ordens abertas
        
        Args:
            symbol: Par de trading
            
        Returns:
            Lista de ordens abertas
        """
        try:
            params = {'symbol': symbol}
            result = self.auth.make_request('GET', '/api/v1/orders', params=params)
            
            # Filtra apenas ordens abertas (não executadas)
            open_orders = [
                order for order in result 
                if order.get('status') in ['New', 'PartiallyFilled']
            ]
            
            return open_orders
            
        except Exception as e:
            logger.error(f"Erro ao obter ordens abertas: {e}")
            return []
    
    def get_order_status(self, symbol: str, order_id: str) -> Optional[Dict]:
        """
        Obtém status de uma ordem específica
        
        Args:
            symbol: Par de trading
            order_id: ID da ordem
            
        Returns:
            Informações da ordem ou None
        """
        try:
            params = {
                'symbol': symbol,
                'orderId': order_id
            }
            
            result = self.auth.make_request('GET', '/api/v1/order', params=params)
            return result
            
        except Exception as e:
            logger.error(f"Erro ao obter status da ordem {order_id}: {e}")
            return None
    
    def get_order_history(self, symbol: str, limit: int = 100) -> List[Dict]:
        """
        Obtém histórico de ordens
        
        Args:
            symbol: Par de trading
            limit: Número máximo de ordens para retornar
            
        Returns:
            Lista de ordens do histórico
        """
        try:
            params = {
                'symbol': symbol,
                'limit': limit
            }
            
            result = self.auth.make_request('GET', '/api/v1/orderHistory', params=params)
            return result
            
        except Exception as e:
            logger.error(f"Erro ao obter histórico de ordens: {e}")
            return []
    
    def get_fills(self, symbol: str, limit: int = 100) -> List[Dict]:
        """
        Obtém execuções (fills) de ordens
        
        Args:
            symbol: Par de trading
            limit: Número máximo de fills para retornar
            
        Returns:
            Lista de execuções
        """
        try:
            params = {
                'symbol': symbol,
                'limit': limit
            }
            
            result = self.auth.make_request('GET', '/api/v1/fills', params=params)
            return result
            
        except Exception as e:
            logger.error(f"Erro ao obter fills: {e}")
            return []
    
    def calculate_total_orders_value(self, orders: List[Dict]) -> Dict:
        """
        Calcula valor total das ordens
        
        Args:
            orders: Lista de ordens
            
        Returns:
            Dicionário com totais de compra e venda
        """
        buy_total = 0
        sell_total = 0
        
        for order in orders:
            price = float(order.get('price', 0))
            quantity = float(order.get('quantity', 0))
            side = order.get('side', '')
            
            if side == 'Bid':
                buy_total += price * quantity
            elif side == 'Ask':
                sell_total += price * quantity
        
        return {
            'buy_total': round(buy_total, 2),
            'sell_total': round(sell_total, 2),
            'total': round(buy_total + sell_total, 2)
        }