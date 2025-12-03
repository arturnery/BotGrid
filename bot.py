"""
Grid Trading Bot - Backpack Exchange
Bot de grid trading automático para rodar localmente
"""

import time
import logging
import sys
from datetime import datetime
from typing import Dict, List, Optional
from backpack_api import BackpackAPI
from grid_calculator import GridCalculator, GridLevel
import config
import auth

# ============================================
# CONFIGURAÇÃO DE LOGGING
# ============================================

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)

if config.SAVE_LOGS:
    file_handler = logging.FileHandler(config.LOG_FILE)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logging.getLogger().addHandler(file_handler)

logger = logging.getLogger(__name__)


class GridTradingBot:
    """Bot de grid trading para Backpack Exchange"""

    def __init__(self):
        """Inicializa o bot"""
        self.api = BackpackAPI(
            public_key=auth.BACKPACK_PUBLIC_KEY,
            private_key=auth.BACKPACK_PRIVATE_KEY,
            api_url=auth.BACKPACK_API_URL,
        )
        self.grid_levels: List[GridLevel] = []
        self.active_orders: Dict[str, Dict] = {}
        self.total_profit = 0
        self.total_loss = 0
        self.start_time = datetime.now()

    def validate_credentials(self) -> bool:
        """Valida se as credenciais estão configuradas corretamente"""
        if auth.BACKPACK_PUBLIC_KEY == "sua_chave_publica_aqui":
            logger.error("❌ Erro: Chave pública não foi configurada em auth.py")
            return False

        if auth.BACKPACK_PRIVATE_KEY == "sua_chave_privada_aqui":
            logger.error("❌ Erro: Chave privada não foi configurada em auth.py")
            return False

        # Tentar fazer uma requisição simples para validar as credenciais
        try:
            logger.info("🔍 Validando credenciais...")
            logger.info(f"Testando conexão com símbolo: {config.SYMBOL}")
            ticker = self.api.get_ticker(config.SYMBOL)
            logger.info(f"Resposta recebida: {ticker}")
            if ticker:
                logger.info(f"✅ Credenciais válidas! Preço atual de {config.SYMBOL}: {ticker}")
                return True
            else:
                logger.warning(f"⚠️  Resposta vazia do ticker, mas continuando...")
                return True
        except Exception as e:
            logger.error(f"❌ Erro ao validar credenciais: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def calculate_grid(self) -> bool:
        """Calcula os níveis de grid"""
        try:
            logger.info(f"📊 Calculando grid para {config.SYMBOL}...")
            logger.info(f"   Modo: {config.MODE}")
            logger.info(f"   Tipo: {config.GRID_TYPE}")
            logger.info(f"   Preço base: {config.BASE_PRICE}")
            logger.info(f"   Intervalo: {config.PRICE_RANGE}")
            logger.info(f"   Níveis: {config.GRID_LEVELS}")
            logger.info(f"   Tamanho da ordem: {config.ORDER_SIZE}")

            kwargs = {}
            if config.GRID_TYPE == "GEOMETRIC":
                kwargs["percentage"] = config.GEOMETRIC_PERCENTAGE
            else:
                kwargs["step"] = config.ARITHMETIC_STEP

            self.grid_levels = GridCalculator.calculate_grid(
                base_price=config.BASE_PRICE,
                price_range=config.PRICE_RANGE,
                grid_levels=config.GRID_LEVELS,
                order_size=config.ORDER_SIZE,
                grid_type=config.GRID_TYPE,
                mode=config.MODE,
                **kwargs,
            )

            GridCalculator.print_grid(self.grid_levels, config.SYMBOL)
            logger.info(f"✅ Grid calculado com {len(self.grid_levels)} níveis")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao calcular grid: {e}")
            return False

    def cancel_existing_orders(self) -> bool:
        """Cancela todas as ordens existentes"""
        try:
            if not config.CANCEL_EXISTING_ORDERS:
                logger.info("⏭️  Pulando cancelamento de ordens existentes")
                return True

            logger.info(f"🗑️  Cancelando ordens existentes de {config.SYMBOL}...")
            result = self.api.cancel_all_orders(config.SYMBOL)
            logger.info(f"✅ Ordens canceladas: {result}")
            return True

        except Exception as e:
            logger.warning(f"⚠️  Erro ao cancelar ordens: {e}")
            return True  # Continua mesmo se houver erro

    def create_grid_orders(self) -> bool:
        """Cria as ordens do grid"""
        try:
            logger.info(f"📝 Criando {len(self.grid_levels)} ordens de grid...")

            created_count = 0
            failed_count = 0

            for level in self.grid_levels:
                try:
                    # Criar a ordem
                    order = self.api.create_order(
                        symbol=config.SYMBOL,
                        side=level.side,
                        order_type="LIMIT",
                        quantity=level.quantity,
                        price=level.price,
                        client_order_id=f"grid_{level.level}_{int(time.time())}",
                    )

                    # Armazenar informações da ordem
                    order_id = order.get("orderId", "unknown")
                    self.active_orders[order_id] = {
                        "level": level.level,
                        "side": level.side,
                        "price": level.price,
                        "quantity": level.quantity,
                        "status": "PENDING",
                        "created_at": datetime.now(),
                    }

                    created_count += 1

                    if config.VERBOSE:
                        logger.info(
                            f"  ✓ Ordem {level.level}: {level.side} {level.quantity} @ {level.price}"
                        )

                    # Pequeno delay para não sobrecarregar a API
                    time.sleep(0.5)

                except Exception as e:
                    failed_count += 1
                    logger.warning(f"  ✗ Erro ao criar ordem {level.level}: {e}")
                    time.sleep(1)

            logger.info(
                f"✅ Grid criado: {created_count} ordens criadas, {failed_count} falharam"
            )
            return created_count > 0

        except Exception as e:
            logger.error(f"❌ Erro ao criar grid de ordens: {e}")
            return False

    def update_orders(self) -> None:
        """Atualiza o status das ordens abertas"""
        try:
            if not self.active_orders:
                logger.debug("Nenhuma ordem ativa para atualizar")
                return

            logger.debug(f"🔄 Atualizando status de {len(self.active_orders)} ordens...")

            for order_id, order_info in list(self.active_orders.items()):
                try:
                    # Obter status da ordem
                    order = self.api.get_order(order_id, config.SYMBOL)
                    status = order.get("status", "Unknown")
                    filled_qty = order.get("filledQuantity", 0)

                    if status == "Filled":
                        logger.info(
                            f"✅ Ordem {order_id} preenchida: {order_info['side']} "
                            f"{filled_qty} @ {order_info['price']}"
                        )
                        self.active_orders[order_id]["status"] = "FILLED"

                        # Se configurado, criar nova ordem para manter o grid
                        if config.AUTO_REORDER:
                            self._create_replacement_order(order_info)

                    elif status == "PartiallyFilled":
                        self.active_orders[order_id]["status"] = "PARTIALLY_FILLED"
                        if config.VERBOSE:
                            logger.debug(
                                f"⏳ Ordem {order_id} parcialmente preenchida: {filled_qty}"
                            )

                    elif status == "Canceled":
                        logger.warning(f"❌ Ordem {order_id} foi cancelada")
                        del self.active_orders[order_id]

                except Exception as e:
                    logger.warning(f"⚠️  Erro ao atualizar ordem {order_id}: {e}")

        except Exception as e:
            logger.error(f"❌ Erro ao atualizar ordens: {e}")

    def _create_replacement_order(self, filled_order: Dict) -> None:
        """Cria uma nova ordem para substituir uma que foi preenchida"""
        try:
            logger.info(f"🔄 Criando ordem de reposição para nível {filled_order['level']}...")

            # Encontrar o nível correspondente
            for level in self.grid_levels:
                if level.level == filled_order["level"]:
                    order = self.api.create_order(
                        symbol=config.SYMBOL,
                        side=level.side,
                        order_type="LIMIT",
                        quantity=level.quantity,
                        price=level.price,
                    )

                    order_id = order.get("orderId", "unknown")
                    self.active_orders[order_id] = {
                        "level": level.level,
                        "side": level.side,
                        "price": level.price,
                        "quantity": level.quantity,
                        "status": "PENDING",
                        "created_at": datetime.now(),
                    }

                    logger.info(f"✅ Ordem de reposição criada: {order_id}")
                    break

        except Exception as e:
            logger.warning(f"⚠️  Erro ao criar ordem de reposição: {e}")

    def print_status(self) -> None:
        """Imprime o status atual do bot"""
        print(f"\n{'='*70}")
        print(f"STATUS DO BOT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")

        try:
            # Preço atual
            ticker = self.api.get_ticker(config.SYMBOL)
            current_price = ticker.get("lastPrice", "N/A")
            print(f"💰 Preço atual de {config.SYMBOL}: {current_price}")
        except:
            print(f"💰 Preço atual de {config.SYMBOL}: N/A")

        # Ordens ativas
        print(f"\n📊 Ordens Ativas: {len(self.active_orders)}")

        filled_orders = [o for o in self.active_orders.values() if o["status"] == "FILLED"]
        pending_orders = [o for o in self.active_orders.values() if o["status"] == "PENDING"]
        partial_orders = [
            o for o in self.active_orders.values() if o["status"] == "PARTIALLY_FILLED"
        ]

        print(f"   ✅ Preenchidas: {len(filled_orders)}")
        print(f"   ⏳ Pendentes: {len(pending_orders)}")
        print(f"   ⚡ Parciais: {len(partial_orders)}")

        # Tempo de execução
        elapsed = datetime.now() - self.start_time
        print(f"\n⏱️  Tempo de execução: {elapsed}")

        # Próxima atualização
        print(f"🔄 Próxima atualização em {config.UPDATE_INTERVAL}s")
        print(f"{'='*70}\n")

    def check_profit_loss(self) -> bool:
        """Verifica se atingiu os limites de lucro/perda"""
        if config.TARGET_PROFIT is None and config.MAX_LOSS is None:
            return True

        try:
            # Calcular lucro/perda atual
            # (simplificado - em produção seria mais complexo)

            if config.TARGET_PROFIT is not None and self.total_profit >= config.TARGET_PROFIT:
                logger.warning(
                    f"🎯 Alvo de lucro atingido! Lucro: {self.total_profit}"
                )
                return False

            if config.MAX_LOSS is not None and self.total_loss >= config.MAX_LOSS:
                logger.warning(f"⛔ Perda máxima atingida! Perda: {self.total_loss}")
                return False

        except Exception as e:
            logger.warning(f"⚠️  Erro ao verificar lucro/perda: {e}")

        return True

    def run(self) -> None:
        """Executa o bot em loop contínuo"""
        logger.info("=" * 70)
        logger.info("🤖 GRID TRADING BOT - INICIANDO")
        logger.info("=" * 70)

        # Validar credenciais
        if not self.validate_credentials():
            logger.error("❌ Falha na validação de credenciais. Encerrando.")
            return

        # Calcular grid
        if not self.calculate_grid():
            logger.error("❌ Falha ao calcular grid. Encerrando.")
            return

        # Cancelar ordens existentes (DESABILITADO - pular direto para criar novas)
        logger.info("⏭️  Pulando cancelamento de ordens (desabilitado)")
        logger.info("💡 Para cancelar ordens manualmente, acesse: https://backpack.exchange")

        # Criar ordens do grid
        if not self.create_grid_orders():
            logger.error("❌ Falha ao criar ordens de grid. Encerrando.")
            return

        logger.info("✅ Bot iniciado com sucesso! Entrando em loop de monitoramento...")
        logger.info(f"⏱️  Intervalo de atualização: {config.UPDATE_INTERVAL}s")
        logger.info("💡 Pressione Ctrl+C para parar o bot")

        try:
            iteration = 0
            while True:
                iteration += 1

                # Atualizar status das ordens
                self.update_orders()

                # Verificar limites de lucro/perda
                if not self.check_profit_loss():
                    logger.warning("⛔ Limites de lucro/perda atingidos. Parando bot.")
                    break

                # Imprimir status a cada 10 iterações
                if iteration % 10 == 0:
                    self.print_status()

                # Aguardar até a próxima atualização
                logger.debug(f"⏳ Aguardando {config.UPDATE_INTERVAL}s até próxima atualização...")
                time.sleep(config.UPDATE_INTERVAL)

        except KeyboardInterrupt:
            logger.info("\n⛔ Bot interrompido pelo usuário")

        except Exception as e:
            logger.error(f"❌ Erro inesperado: {e}")

        finally:
            logger.info("🛑 Encerrando bot...")
            logger.info("=" * 70)


def main():
    """Função principal"""
    bot = GridTradingBot()
    bot.run()


if __name__ == "__main__":
    main()
