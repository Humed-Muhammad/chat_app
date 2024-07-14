from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import bcrypt
from chat_app.settings import dynamodb, SECRET_KEY
from boto3.dynamodb.conditions import Attr
import jwt


users_table = dynamodb.Table('users')

def get_user_by_email(email):
    try:
        response = users_table.scan(
            FilterExpression=Attr('email').eq(email)
        )
        items = response.get('Items', [])
        print(items)
        if items:
            return items[0]  # Return the first matching user
        else:
            return None  # No user found with this email
    except Exception as e:
        print(f"Error retrieving user: {str(e)}")
        return None


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')
    print(email, password)

    if email is None or password is None:
        return JsonResponse({'error': 'Please provide email and password'}, status=400)

    try:
        # Query DynamoDB for the user
        response = get_user_by_email(email)
        # print(response)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    if response is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    # if 'Item' not in response:

  
    stored_password = response.get('password', '').encode('utf-8')
    print(stored_password)

    # Check if the provided password matches the stored hashed password
    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
         # Generate JWT token
        payload = {
            'email': email,
            'userType': response.get('userType'),
            'userId': response.get('userId')
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return JsonResponse({"token": token, "userId": response.get('userId'),  'userType': response.get('userType') })
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)