#!/usr/bin/env python3
"""
Script para verificar mercados disponíveis na Backpack Exchange
Execute antes de configurar o bot
"""

import requests
import json

def get_available_markets():
    """Busca todos os mercados disponíveis na Backpack"""
    try:
        url = "https://api.backpack.exchange/api/v1/markets"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Erro ao buscar mercados: {e}")
        return []

def main():
    print("=" * 70)
    print("MERCADOS DISPONÍVEIS NA BACKPACK EXCHANGE")
    print("=" * 70)
    print()
    
    markets = get_available_markets()
    
    if not markets:
        print("❌ Não foi possível obter a lista de mercados")
        return
    
    # Filtra apenas mercados SPOT (não perpétuos)
    spot_markets = [m for m in markets if not m['symbol'].endswith('_PERP')]
    perp_markets = [m for m in markets if m['symbol'].endswith('_PERP')]
    
    print("📊 MERCADOS SPOT (Para Grid Trading):")
    print("-" * 70)
    
    if spot_markets:
        # Agrupa por moeda base
        usdc_markets = [m for m in spot_markets if 'USDC' in m['symbol']]
        usdt_markets = [m for m in spot_markets if 'USDT' in m['symbol']]
        
        if usdc_markets:
            print("\n💵 Pares com USDC:")
            for market in sorted(usdc_markets, key=lambda x: x['symbol']):
                print(f"  ✓ {market['symbol']}")
        
        if usdt_markets:
            print("\n💵 Pares com USDT:")
            for market in sorted(usdt_markets, key=lambda x: x['symbol']):
                print(f"  ✓ {market['symbol']}")
    else:
        print("❌ Nenhum mercado SPOT encontrado")
    
    print()
    print("=" * 70)
    print(f"Total de mercados SPOT: {len(spot_markets)}")
    print(f"Total de mercados PERP (futuros): {len(perp_markets)}")
    print("=" * 70)
    print()
    print("💡 DICA: Use os símbolos SPOT acima no seu config.py")
    print("   Exemplo: SYMBOL = 'SOL_USDC'")
    print()
    
    # Mostra detalhes de alguns mercados populares
    print("📈 DETALHES DE MERCADOS POPULARES:")
    print("-" * 70)
    
    popular = ['SOL_USDC', 'BTC_USDC', 'ETH_USDC']
    for symbol in popular:
        market = next((m for m in spot_markets if m['symbol'] == symbol), None)
        if market:
            print(f"\n{symbol}:")
            print(f"  Preço mínimo: {market.get('filters', {}).get('price', {}).get('minPrice', 'N/A')}")
            print(f"  Tick size: {market.get('filters', {}).get('price', {}).get('tickSize', 'N/A')}")
            print(f"  Quantidade mínima: {market.get('filters', {}).get('quantity', {}).get('minQuantity', 'N/A')}")
            print(f"  Step size: {market.get('filters', {}).get('quantity', {}).get('stepSize', 'N/A')}")

if __name__ == "__main__":
    main()