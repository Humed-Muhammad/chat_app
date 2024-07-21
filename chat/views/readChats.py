from chat_app.utils import jwt_required, chatsHaveBeenRead
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
import json

@csrf_exempt
@require_http_methods(["POST"])
@jwt_required
def readChats(request):
    try:
        data:list[str] = json.loads(request.body)
        print(data)
        
        # Get the user type from the query parameter
        
        ids = chatsHaveBeenRead(data.get('ids'))
        return JsonResponse({'data': ids})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)