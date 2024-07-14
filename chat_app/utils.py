from functools import wraps
from chat_app.settings import dynamodb
from boto3.dynamodb.conditions import Attr


def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapper.is_protected = True
    return wrapper


users_table = dynamodb.Table('users')
def get_user_by_type(user_type:str):
    try:
        response = users_table.scan(
            FilterExpression=Attr('userType').eq(user_type)
        )
        items = response.get('Items', [])

        if items:
            # Filter out the 'password' field from the user data
            filtered_users = [
                {k: v for k, v in user.items() if k != 'password'}
                for user in items
            ]
            return filtered_users
        else:
            return None
    except Exception as e:
        print(f"Error retrieving user: {str(e)}")
        return None


chats_table = dynamodb.Table('chats')

def get_chats_by_user(messageId: str, size: int = 10, pageNo:int=1) -> list[dict]:
    try:
        response = chats_table.scan(
            FilterExpression=Attr('messageId').eq(messageId)
        )

        items = response.get('Items', [])

        if items:
            return items
        else:
            return []
    except Exception as e:
        print(f"Error retrieving chats: {str(e)}")
        return []