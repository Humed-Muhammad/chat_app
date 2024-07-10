import jwt
from chat_app.settings import SECRET_KEY
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Check if the view is protected
        if getattr(view_func, 'is_protected', False):
            token = request.headers.get('Authorization')
            if token:
                try:
                    # Verify and decode the JWT token
                    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                    request.user = payload['email']
                except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                    return JsonResponse({'error': 'Invalid or expired token'}, status=401)
            else:
                return JsonResponse({'error': 'Authentication token missing'}, status=401)

        return None