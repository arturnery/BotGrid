import time
import logging
from typing import List, Dict
from config import *
from auth import BackpackAuth
from grid import GridStrategy
from orders import OrderManager

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('grid_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class GridBot:
    def __init__(self):
        """Inicializa o bot de grid trading para futuros perpétuos"""
        self.auth = BackpackAuth()
        self.order_manager = OrderManager(self.auth)
        self.grid = None
        self.running = False
        
    def start(self):
        """Inicia o bot"""
        logger.info("=" * 50)
        logger.info("BOT DE GRID TRADING - FUTUROS PERPÉTUOS")
        logger.info("=" * 50)
        
        self.running = True
        
        try:
            # Verifica conexão
            if not self.auth.test_connection():
                logger.error("Falha ao conectar com a API.")
                return
            
            # Busca preço atual
            logger.info(f"Buscando preço atual de {SYMBOL}...")
            try:
                ticker = self.auth.get_ticker(SYMBOL)
                current_price = float(ticker['lastPrice'])
                logger.info(f"✅ Preço atual: ${current_price}")
            except Exception as e:
                logger.warning(f"Não foi possível obter preço: {e}")
                current_price = (LOWER_PRICE + UPPER_PRICE) / 2
            
            # Calcula range baseado no preço atual
            range_percentage = 10  # ±10% do preço atual
            lower_price = current_price * (1 - range_percentage / 100)
            upper_price = current_price * (1 + range_percentage / 100)
            
            logger.info(f"Par: {SYMBOL}")
            logger.info(f"Preço Atual: ${current_price}")
            logger.info(f"Range Calculado: ${round(lower_price, 2)} - ${round(upper_price, 2)} ({range_percentage}%)")
            logger.info(f"Modo: {MODE}")
            logger.info(f"Níveis: {NUMBER_OF_GRIDS}")
            logger.info(f"Quantidade/Grid: {QUANTITY_PER_GRID}")
            logger.info("=" * 50)
            
            # Inicializa grid
            self.grid = GridStrategy(
                symbol=SYMBOL,
                lower_price=lower_price,
                upper_price=upper_price,
                grid_count=NUMBER_OF_GRIDS,
                quantity_per_grid=QUANTITY_PER_GRID,
                price_decimal=PRICE_DECIMAL,
                mode=MODE
            )
            
            # Cancela ordens antigas
            logger.info("Cancelando ordens antigas...")
            self.order_manager.cancel_all_orders(SYMBOL)
            
            # Calcula grid
            grid_levels = self.grid.calculate_grid_levels()
            
            # Coloca ordens
            logger.info("Colocando ordens do grid...")
            self.place_grid_orders(grid_levels)
            
            # Loop de monitoramento
            logger.info("Entrando no loop de monitoramento...")
            self.run_loop()
            
        except KeyboardInterrupt:
            logger.info("\nBot interrompido pelo usuário")
            self.stop()
        except Exception as e:
            logger.error(f"Erro fatal: {e}", exc_info=True)
            self.stop()
    
    def place_grid_orders(self, grid_levels: List[Dict]):
        """Coloca todas as ordens do grid"""
        placed = 0
        failed = 0
        
        for level in grid_levels:
            try:
                side = 'Bid' if level['side'] == 'buy' else 'Ask'
                
                result = self.order_manager.place_limit_order(
                    symbol=SYMBOL,
                    side=side,
                    price=level['price'],
                    quantity=level['quantity']
                )
                
                if result:
                    placed += 1
                else:
                    failed += 1
                
                time.sleep(0.1)  # Evita rate limit
                
            except Exception as e:
                logger.error(f"Erro ao colocar ordem: {e}")
                failed += 1
        
        logger.info("=" * 50)
        logger.info(f"✅ Ordens colocadas: {placed}")
        logger.info(f"❌ Ordens falhadas: {failed}")
        logger.info("=" * 50)
    
    def run_loop(self):
        """Loop de monitoramento"""
        while self.running:
            try:
                # Obtém ordens abertas
                open_orders = self.order_manager.get_open_orders(SYMBOL)
                logger.info(f"📊 Ordens abertas: {len(open_orders)}")
                
                # Aguarda
                time.sleep(UPDATE_INTERVAL)
                
            except Exception as e:
                logger.error(f"Erro no loop: {e}", exc_info=True)
                time.sleep(UPDATE_INTERVAL)
    
    def stop(self):
        """Para o bot"""
        logger.info("Parando o bot...")
        self.running = False
        
        if CANCEL_ON_EXIT:
            logger.info("Cancelando todas as ordens...")
            self.order_manager.cancel_all_orders(SYMBOL)
        
        logger.info("Bot parado!")


if __name__ == "__main__":
    bot = GridBot()
    bot.start()