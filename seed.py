import uuid
import bcrypt
from chat_app.settings import BCRYPT_SALT
from chat.models import User, Chat, WebSocketConnections

def create_tables():
    print("Creating tables...")
    User.Table.create_table()
    Chat.Table.create_table()
    # WebSocketConnections.Table.create_table()
    print("Tables created successfully.")


def hash_password(password): 
    return bcrypt.hashpw(password.encode('utf-8'), BCRYPT_SALT)

# # Example usage:


def main():
    create_tables()
    print("Start Seeding!")
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

        WebSocketConnections.put(item={'connectionId': '123456'})
        
    except Exception as e:
        print(f"Error putting item: {e}")

    print("Seeding completed successfully!")

if __name__ == "__main__":
    main()