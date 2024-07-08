import uuid
import boto3
from models import User, Chat, dynamodb




def create_tables():
    print("Creating tables...")
    user_table = dynamodb.create_table(
        TableName='users',
        KeySchema=[
            {
                'AttributeName': 'userId',
                'KeyType': 'HASH'  # Partition key
            },
           
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'userId',
                'AttributeType': 'S'  # String
            },
            # { 'AttributeName': 'username', 'AttributeType': 'S' },
            # { 'AttributeName': 'email', 'AttributeType': 'S' },
            # { 'AttributeName': 'password', 'AttributeType': 'S' },
            # { 'AttributeName': 'createdAt', 'AttributeType': 'S' },
            # { 'AttributeName': 'userType', 'AttributeType': 'S' },
            # { 'AttributeName': 'specialization', 'AttributeType': 'S' },
            # { 'AttributeName': 'childrenCount', 'AttributeType': 'S' },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Table 'User' status:", user_table.table_status)

    chat_table = dynamodb.create_table(
        TableName='chats',
        KeySchema=[
            {
                'AttributeName': 'chatId',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'messageId',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'chatId',
                'AttributeType': 'S'  # String
            },
            {
                'AttributeName': 'messageId',
                'AttributeType': 'S'  # String
            },
            # {'AttributeName':'timestamp', 'AttributeType': 'S'},
            # {'AttributeName':'senderId', 'AttributeType': 'S'},
            # {'AttributeName':'recipientId', 'AttributeType': 'S'},
            # {'AttributeName':'readAt', 'AttributeType': 'S'},
            # {'AttributeName':'createdAt', 'AttributeType': 'S'},
            # {'AttributeName':'content', 'AttributeType': 'M' }, # 'M' denotes a map (JSON-like object)
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    print("Table 'Chat' status:", chat_table.table_status)
    print("Tables created successfully.")


def seed_users():
    print("Seeding users...")
    users = [
        {
            "username": "dr_smith",
            "email": "drsmith@example.com",
            "passwordHash": "hashed_password_1",
            "userType": "therapist",
            "specialization": "Child Psychology"
        },
        {
            "username": "dr_johnson",
            "email": "drjohnson@example.com",
            "passwordHash": "hashed_password_2",
            "userType": "therapist",
            "specialization": "Family Therapy"
        },
        {
            "username": "alice_mom",
            "email": "alice@example.com",
            "passwordHash": "hashed_password_3",
            "userType": "parent",
            "childrenCount": 2
        },
        {
            "username": "bob_dad",
            "email": "bob@example.com",
            "passwordHash": "hashed_password_4",
            "userType": "parent",
            "childrenCount": 1
        }
    ]

    for user_data in users:
        user = User(**user_data)
        user.save()
        print(f"Created user: {user.username} ({user.userType})")

    return User.scan()

def seed_chats(users):
    print("Seeding chats...")
    therapists = [user for user in users if user.userType == 'therapist']
    parents = [user for user in users if user.userType == 'parent']

    for parent in parents:
        for therapist in therapists:
            chat_id = str(uuid.uuid4())
            for _ in range(5):  # 5 messages per chat
                sender = parent if _ % 2 == 0 else therapist
                recipient = therapist if _ % 2 == 0 else parent
                
                # Alternating between text, image, and video for demonstration
                content_type = ['text', 'image', 'video'][_ % 3]
                
                chat_data = {
                    "chatId": chat_id,
                    "senderId": sender.userId,
                    "recipientId": recipient.userId,
                    "content": {
                        "type": content_type,
                        "value": f"Sample {content_type} content from {sender.username} to {recipient.username}."
                    }
                }
                
                chat = Chat(**chat_data)
                chat.save()
            
            print(f"Created 5 messages for chat between {parent.username} and {therapist.username}")

def main():
    create_tables()
    users = seed_users()
    seed_chats(users)
    print("Seeding completed successfully!")

if __name__ == "__main__":
    main()