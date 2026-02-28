from django.shortcuts import render

def dashboard_home(request):
    """
    Temporary mock view for PriceCom dashboard UI verification.
    Provides realistic data to test Django Cotton components before API integration.
    """
    context = {
        'total_tracked': 8421,
        'drops_today': 284,
        'drops_trend': -12.4,
        'avg_change': 0,
        'avg_change_trend': 2.1,
        'active_alerts': 12,
        
        'prediction': {
            'signal': 'WAIT',
            'confidence': 78,
            'time_frame': '3 DAYS',
            'velocity': 'high',
            'trend': 'dropping'
        }
    }
    return render(request, 'dashboard/index.html', context)
