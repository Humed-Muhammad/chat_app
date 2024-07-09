import uuid
from chat.models import User, Chat

# # Example usage:
try:
    # Provide a userId when putting an item
    user_id1 = str(uuid.uuid4())
    user_id2 = str(uuid.uuid4())
    user1 = User.put(item={
        'userId': user_id1,
        'username': "bob",
        'email': "bob@gmail.com",
        'password': "123456",
        'userType': "therapist",
    })

    user2 = User.put(item={
        'userId': user_id2,
        'username': "fatima",
        'email': "fatima@gmail.com",
        'password': "123456",
        'userType': "parent",
        'childrenCount': 1
    })
    
    print(f"User {user_id1} added successfully.")
except Exception as e:
    print(f"Error putting item: {e}")

