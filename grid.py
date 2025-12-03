import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


class GridStrategy:
    def __init__(self, symbol: str, lower_price: float, upper_price: float,
                 grid_count: int, quantity_per_grid: float, price_decimal: int = 2):
        """
        Inicializa a estratégia de grid para futuros perpétuos
        """
        self.symbol = symbol
        self.lower_price = lower_price
        self.upper_price = upper_price
        self.grid_count = grid_count
        self.quantity_per_grid = quantity_per_grid
        self.price_decimal = price_decimal
        
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Valida os parâmetros"""
        if self.lower_price >= self.upper_price:
            raise ValueError("LOWER_PRICE deve ser menor que UPPER_PRICE")
        
        if self.grid_count <= 0:
            raise ValueError("NUMBER_OF_GRIDS deve ser maior que zero")
        
        if self.quantity_per_grid <= 0:
            raise ValueError("QUANTITY_PER_GRID deve ser maior que zero")
    
    def calculate_grid_levels(self) -> List[Dict]:
        """
        Calcula os níveis do grid aritmético
        """
        logger.info("Calculando níveis do grid...")
        logger.info(f"Range: ${self.lower_price} - ${self.upper_price}")
        logger.info(f"Níveis: {self.grid_count}")
        
        grid_levels = []
        price_step = (self.upper_price - self.lower_price) / self.grid_count
        
        for i in range(self.grid_count + 1):
            price = self.lower_price + (i * price_step)
            price = round(price, self.price_decimal)
            
            # Ordens de compra abaixo do ponto médio
            # Ordens de venda acima do ponto médio
            mid_price = (self.lower_price + self.upper_price) / 2
            
            if price < mid_price:
                grid_levels.append({
                    'price': price,
                    'side': 'buy',
                    'quantity': self.quantity_per_grid,
                    'level': i
                })
            elif price > mid_price:
                grid_levels.append({
                    'price': price,
                    'side': 'sell',
                    'quantity': self.quantity_per_grid,
                    'level': i
                })
        
        logger.info(f"Grid calculado: {len(grid_levels)} níveis")
        self._log_grid_summary(grid_levels)
        
        return grid_levels
    
    def _log_grid_summary(self, grid_levels: List[Dict]):
        """Mostra resumo do grid"""
        buy_orders = [g for g in grid_levels if g['side'] == 'buy']
        sell_orders = [g for g in grid_levels if g['side'] == 'sell']
        
        logger.info("=" * 50)
        logger.info("RESUMO DO GRID")
        logger.info("=" * 50)
        logger.info(f"Total de ordens: {len(grid_levels)}")
        logger.info(f"Ordens de compra: {len(buy_orders)}")
        logger.info(f"Ordens de venda: {len(sell_orders)}")
        
        if buy_orders:
            logger.info(f"Menor preço de compra: ${min(o['price'] for o in buy_orders)}")
            logger.info(f"Maior preço de compra: ${max(o['price'] for o in buy_orders)}")
        
        if sell_orders:
            logger.info(f"Menor preço de venda: ${min(o['price'] for o in sell_orders)}")
            logger.info(f"Maior preço de venda: ${max(o['price'] for o in sell_orders)}")
        
        total_buy_value = sum(o['price'] * o['quantity'] for o in buy_orders)
        total_sell_qty = sum(o['quantity'] for o in sell_orders)
        
        logger.info(f"Capital necessário (USDC): ${round(total_buy_value, 2)}")
        logger.info(f"Quantidade necessária (ativo): {round(total_sell_qty, 4)}")
        logger.info("=" * 50)