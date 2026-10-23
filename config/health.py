from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db import connections,DatabaseError
@require_GET
def health(request):return JsonResponse({'status':'ok'})
@require_GET
def ready(request):
    try:
        with connections['default'].cursor() as cursor:cursor.execute('SELECT 1')
    except DatabaseError:return JsonResponse({'status':'unavailable'},status=503)
    return JsonResponse({'status':'ok'})
