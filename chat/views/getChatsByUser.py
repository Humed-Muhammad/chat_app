from chat_app.utils import jwt_required, get_chats_by_user
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

@csrf_exempt
@require_http_methods(["GET"])
@jwt_required
def get_chats(request):
    try:
        # Get the user type from the query parameter
        user_id = request.GET.get('user_id', None)
        if user_id:
            users = get_chats_by_user(user_id)
            return JsonResponse({'data': users})
        else:
            return JsonResponse({'error': 'user_id parameter is required'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)