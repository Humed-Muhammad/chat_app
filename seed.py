import uuid
from chat.models import User, Chat
import bcrypt
from chat_app.settings import BCRYPT_SALT

def hash_password(password): 
    return bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT)

# # Example usage:
try:
    # Provide a userId when putting an item
    user_id1 = str(uuid.uuid4())
    user_id2 = str(uuid.uuid4())
    user1 = User.put(item={
        'userId': user_id1,
        'username': "bob",
        'email': "bob@gmail.com",
        'password': hash_password(password="123456"),
        'userType': "therapist",
    })

    user2 = User.put(item={
        'userId': user_id2,
        'username': "fatima",
        'email': "fatima@gmail.com",
        'password': hash_password(password="123456"),
        'userType': "parent",
        'childrenCount': 1
    })
    
    print(f"User {user_id1} added successfully.")
except Exception as e:
    print(f"Error putting item: {e}")

