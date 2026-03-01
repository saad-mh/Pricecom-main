import json
from django.shortcuts import render
from django.http import JsonResponse
from core.models import Product, StorePrice, PriceHistory
from django.db.models import Min, F
import random

def dashboard_home(request):
    """
    Dashboard Home View
    Initializes Alpine store and base layout.
    """
    context = {
        'total_tracked': Product.objects.count() if Product.objects.exists() else 8421,
        'active_alerts': 12,
        'prediction': {
            'signal': 'WAIT 3 DAYS',
            'confidence': 78,
            'signals': [
                'Competitor restock detected',
                'Flash sale pattern -72h',
                'Demand elasticity neutral'
            ]
        }
    }
    return render(request, 'dashboard/index.html', context)

def api_products(request):
    """
    HTMX endpoint returning table rows for products.
    """
    # Fetch real data
    products = Product.objects.prefetch_related('prices').all()[:10]
    
    # If no data, use some fallback mocks for visual purposes
    product_list = []
    if not products:
        product_list = [
            {'id': 1, 'name': 'IPHONE-14-128-BLK', 'amz': 62999, 'flip': 61499, 'min': 61499, 'delta': 'DROP_1.5K', 'status': 'LIVE'},
            {'id': 2, 'name': 'MACBOOK-AIR-M2-256', 'amz': 89900, 'flip': 88990, 'min': 88990, 'delta': 'STABLE_00', 'status': 'T-300s'},
            {'id': 3, 'name': 'SAMSUNG-S23-256', 'amz': 64999, 'flip': 65999, 'min': 64999, 'delta': 'RISE_1.0K', 'status': 'T-3600s'},
        ]
    else:
        for p in products:
            prices = p.prices.all()
            amz = next((sp.current_price for sp in prices if sp.store_name == 'Amazon'), 0)
            flip = next((sp.current_price for sp in prices if sp.store_name == 'Flipkart'), 0)
            min_val = min([amz, flip]) if amz and flip else (amz or flip)
            product_list.append({
                'id': p.id,
                'name': p.name.upper()[:20],
                'amz': f"₹{int(amz):,}" if amz else 'N/A',
                'flip': f"₹{int(flip):,}" if flip else 'N/A',
                'min': f"₹{int(min_val):,}" if min_val else '0',
                'delta': 'STABLE_00',
                'status': 'LIVE'
            })

    return render(request, 'dashboard/partials/product_rows.html', {'products': product_list})

def api_product_history(request, uuid):
    """
    Returns JSON price history for ApexCharts
    """
    # Generate some mock data or fetch real if available
    # For chart update
    data = {
        'series': [
            {'name': 'Amazon', 'data': [random.randint(400, 500) for _ in range(7)]},
            {'name': 'Flipkart', 'data': [random.randint(400, 500) for _ in range(7)]}
        ]
    }
    return JsonResponse(data)

def api_watchlist(request):
    """
    HTMX endpoint for watchlist panel
    """
    # Mock return for visual
    items = [
        {'name': 'IPHONE-14-BLK', 'target': '₹60K', 'current': '₹61,499', 'delta': '+1.5K_DELTA', 'pct': 95},
        {'name': 'SONY-XM5', 'target': '₹22K', 'current': '₹26,499', 'delta': '+4.4K_DELTA', 'pct': 85},
    ]
    return render(request, 'dashboard/partials/watchlist_items.html', {'items': items})

def api_system_health(request):
    """
    HTMX endpoint for system health
    """
    context = {
        'nodes': '12/12',
        'queue': f"{random.randint(2000, 3000)}/s",
        'latency': f"{random.randint(8, 20)}ms",
        'cpu': random.randint(30, 60)
    }
    return render(request, 'dashboard/partials/system_health_content.html', context)

def api_search(request):
    """
    HTMX POST endpoint for search
    """
    query = request.POST.get('q', '')
    return render(request, 'dashboard/partials/search_results.html', {'query': query})
