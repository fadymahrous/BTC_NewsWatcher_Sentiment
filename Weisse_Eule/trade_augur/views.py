from django.shortcuts import render
from .models import news_healines
from datetime import datetime, timedelta, timezone
import json
from django.contrib.auth.decorators import login_required

@login_required
def home_page(request):
    twelve_hours_ago = datetime.now(timezone.utc) - timedelta(hours=24)
    news=news_healines.objects.filter(published_on__gt=twelve_hours_ago)
    # Convert hexenmeinung string to dict
    for item in news:
        if isinstance(item.hexenmeinung, str):
            try:
                item.hexenmeinung = json.loads(item.hexenmeinung)
            except json.JSONDecodeError:
                item.hexenmeinung = {}

    return render(request, 'home.html', {'news': news})