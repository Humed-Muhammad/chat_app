import boto3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import bcrypt
from django.conf import settings
from chat_app.settings import dynamodb
from boto3.dynamodb.conditions import Attr


users_table = dynamodb.Table('users')

def get_user_by_email(email):
    try:
        response = users_table.scan(
            FilterExpression=Attr('email').eq(email)
        )
        print(response)
        items = response.get('Items', [])
        
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

    # user = response['Item']
    # stored_password = user.get('password', '').encode('utf-8')

    # # Check if the provided password matches the stored hashed password
    # if bcrypt.checkpw(password.encode('utf-8'), stored_password):
    #     # Password is correct, create a session or token here
        # For simplicity, we'll just return a success message
        # In a real application, you'd generate a token or start a session
    return JsonResponse({'success': 'User logged in successfully', 'email': email})
    # else:
    #     return JsonResponse({'error': 'Invalid credentials'}, status=400)