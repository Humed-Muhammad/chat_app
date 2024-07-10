from chat_app.utils import jwt_required, get_user_by_type
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

@csrf_exempt
@require_http_methods(["GET"])
@jwt_required
def get_users(request):
    try:
        # Get the user type from the query parameter
        user_type = request.GET.get('user_type', None)
        if user_type:
            users = get_user_by_type(user_type)
            return JsonResponse({'data': users})
        else:
            return JsonResponse({'error': 'user_type parameter is required'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)