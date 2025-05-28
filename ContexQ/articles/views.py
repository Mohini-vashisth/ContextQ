from django.http import JsonResponse
from .models import Article

def news_list(request):
    country = request.GET.get("country")
    lang = request.GET.get("lang")

    # Query from DB with optional filters
    queryset = Article.objects.all()
    if country:
        queryset = queryset.filter(country__iexact=country)
    if lang:
        queryset = queryset.filter(language=lang)

    # Convert to dicts
    data = list(queryset.values())

    return JsonResponse(data, safe=False)