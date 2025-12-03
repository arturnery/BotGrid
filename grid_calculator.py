"""
Calculador de Grid Trading
Calcula os níveis de grid baseado nos parâmetros configurados
"""

import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)


class GridLevel:
    """Representa um nível de grid"""

    def __init__(self, level: int, price: float, quantity: float, side: str):
        self.level = level
        self.price = price
        self.quantity = quantity
        self.side = side  # BUY ou SELL

    def __repr__(self):
        return f"GridLevel(level={self.level}, {self.side} {self.quantity} @ {self.price})"


class GridCalculator:
    """Calcula os níveis de grid para trading"""

    @staticmethod
    def calculate_geometric_grid(
        base_price: float,
        price_range: float,
        grid_levels: int,
        order_size: float,
        mode: str = "NEUTRAL",
        percentage: float = 2,
    ) -> List[GridLevel]:
        """
        Calcula grid com distribuição geométrica (percentual fixo)

        Args:
            base_price: Preço central
            price_range: Amplitude total do grid
            grid_levels: Número de níveis
            order_size: Tamanho de cada ordem
            mode: LONG, SHORT ou NEUTRAL
            percentage: Percentual de diferença entre níveis

        Returns:
            Lista de níveis de grid
        """
        levels = []

        if mode == "NEUTRAL":
            # Metade acima, metade abaixo
            for i in range(1, grid_levels + 1):
                # Níveis de compra (abaixo do preço base)
                price_buy = base_price * ((100 - percentage) / 100) ** i
                levels.append(GridLevel(i, price_buy, order_size, "BUY"))

                # Níveis de venda (acima do preço base)
                price_sell = base_price * ((100 + percentage) / 100) ** i
                levels.append(GridLevel(grid_levels + i, price_sell, order_size, "SELL"))

        elif mode == "LONG":
            # Apenas compra abaixo e venda acima
            for i in range(1, grid_levels + 1):
                # Níveis de compra (abaixo do preço base)
                price_buy = base_price * ((100 - percentage) / 100) ** i
                levels.append(GridLevel(i, price_buy, order_size, "BUY"))

            for i in range(1, grid_levels + 1):
                # Níveis de venda (acima do preço base)
                price_sell = base_price * ((100 + percentage) / 100) ** i
                levels.append(GridLevel(grid_levels + i, price_sell, order_size, "SELL"))

        elif mode == "SHORT":
            # Apenas venda acima e compra abaixo
            for i in range(1, grid_levels + 1):
                # Níveis de venda (acima do preço base)
                price_sell = base_price * ((100 + percentage) / 100) ** i
                levels.append(GridLevel(i, price_sell, order_size, "SELL"))

            for i in range(1, grid_levels + 1):
                # Níveis de compra (abaixo do preço base)
                price_buy = base_price * ((100 - percentage) / 100) ** i
                levels.append(GridLevel(grid_levels + i, price_buy, order_size, "BUY"))

        return sorted(levels, key=lambda x: x.price)

    @staticmethod
    def calculate_arithmetic_grid(
        base_price: float,
        price_range: float,
        grid_levels: int,
        order_size: float,
        mode: str = "NEUTRAL",
        step: float = 100,
    ) -> List[GridLevel]:
        """
        Calcula grid com distribuição aritmética (preço fixo)

        Args:
            base_price: Preço central
            price_range: Amplitude total do grid
            grid_levels: Número de níveis
            order_size: Tamanho de cada ordem
            mode: LONG, SHORT ou NEUTRAL
            step: Diferença de preço entre níveis

        Returns:
            Lista de níveis de grid
        """
        levels = []

        if mode == "NEUTRAL":
            # Metade acima, metade abaixo
            for i in range(1, grid_levels + 1):
                # Níveis de compra (abaixo do preço base)
                price_buy = base_price - (step * i)
                levels.append(GridLevel(i, price_buy, order_size, "BUY"))

                # Níveis de venda (acima do preço base)
                price_sell = base_price + (step * i)
                levels.append(GridLevel(grid_levels + i, price_sell, order_size, "SELL"))

        elif mode == "LONG":
            # Apenas compra abaixo e venda acima
            for i in range(1, grid_levels + 1):
                # Níveis de compra (abaixo do preço base)
                price_buy = base_price - (step * i)
                levels.append(GridLevel(i, price_buy, order_size, "BUY"))

            for i in range(1, grid_levels + 1):
                # Níveis de venda (acima do preço base)
                price_sell = base_price + (step * i)
                levels.append(GridLevel(grid_levels + i, price_sell, order_size, "SELL"))

        elif mode == "SHORT":
            # Apenas venda acima e compra abaixo
            for i in range(1, grid_levels + 1):
                # Níveis de venda (acima do preço base)
                price_sell = base_price + (step * i)
                levels.append(GridLevel(i, price_sell, order_size, "SELL"))

            for i in range(1, grid_levels + 1):
                # Níveis de compra (abaixo do preço base)
                price_buy = base_price - (step * i)
                levels.append(GridLevel(grid_levels + i, price_buy, order_size, "BUY"))

        return sorted(levels, key=lambda x: x.price)

    @staticmethod
    def calculate_grid(
        base_price: float,
        price_range: float,
        grid_levels: int,
        order_size: float,
        grid_type: str = "GEOMETRIC",
        mode: str = "NEUTRAL",
        **kwargs,
    ) -> List[GridLevel]:
        """
        Calcula o grid baseado no tipo especificado

        Args:
            base_price: Preço central
            price_range: Amplitude total do grid
            grid_levels: Número de níveis
            order_size: Tamanho de cada ordem
            grid_type: GEOMETRIC ou ARITHMETIC
            mode: LONG, SHORT ou NEUTRAL
            **kwargs: Parâmetros adicionais (percentage, step)

        Returns:
            Lista de níveis de grid
        """
        if grid_type == "GEOMETRIC":
            percentage = kwargs.get("percentage", 2)
            return GridCalculator.calculate_geometric_grid(
                base_price, price_range, grid_levels, order_size, mode, percentage
            )
        elif grid_type == "ARITHMETIC":
            step = kwargs.get("step", 100)
            return GridCalculator.calculate_arithmetic_grid(
                base_price, price_range, grid_levels, order_size, mode, step
            )
        else:
            raise ValueError(f"Tipo de grid desconhecido: {grid_type}")

    @staticmethod
    def print_grid(levels: List[GridLevel], symbol: str = ""):
        """
        Imprime o grid de forma legível

        Args:
            levels: Lista de níveis de grid
            symbol: Símbolo do par (para exibição)
        """
        print(f"\n{'='*60}")
        print(f"Grid de Trading para {symbol}")
        print(f"{'='*60}")
        print(f"{'Nível':<8} {'Tipo':<8} {'Preço':<15} {'Quantidade':<15}")
        print(f"{'-'*60}")

        for level in levels:
            print(f"{level.level:<8} {level.side:<8} {level.price:<15.2f} {level.quantity:<15.6f}")

        print(f"{'='*60}\n")

        # Resumo
        buy_levels = [l for l in levels if l.side == "BUY"]
        sell_levels = [l for l in levels if l.side == "SELL"]

        print(f"Resumo:")
        print(f"  Total de ordens: {len(levels)}")
        print(f"  Ordens de compra (BUY): {len(buy_levels)}")
        print(f"  Ordens de venda (SELL): {len(sell_levels)}")
        print(f"  Preço mínimo: {min(l.price for l in levels):.2f}")
        print(f"  Preço máximo: {max(l.price for l in levels):.2f}")
        print(f"  Investimento total (aprox): {sum(l.quantity * l.price for l in buy_levels):.2f}")
        print()
