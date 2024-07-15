from functools import wraps
from chat_app.settings import dynamodb, s3_bucket, AWS_STORAGE_BUCKET_NAME, AWS_REGION
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


def upload_file_to_s3(file_obj, file_name="uploaded"):
    """
    Uploads a file to the configured S3 bucket and returns the public URL of the uploaded file.
    
    Args:
        file_obj (django.core.files.File): The file object to be uploaded.
        file_name (str): The name of the file to be used in S3.
    
    Returns:
        str: The public URL of the uploaded file.
    """
    try:
        # Upload the file to S3
        s3_bucket.upload_fileobj(file_obj, file_name)
        
        # Generate the public URL of the uploaded file
        file_url = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_name}"
        
        return file_url
    
    except Exception as e:
        # Handle any errors that occurred during the upload
        print(f"Error uploading file to S3: {e}")
        return None