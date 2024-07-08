from marshmallow import Schema, fields, validate
import datetime
import time
import uuid
import boto3
from dynamorm import DynaModel, GlobalIndex, ProjectAll

AWS_ACCESS_KEY_ID = 'i5z17r'
AWS_SECRET_ACCESS_KEY = 'tfwhua'
AWS_REGION = 'eu-west-2'
DYNAMODB_ENDPOINT_URL = 'http://localhost:8001'

# Set up the boto3 session to connect to local DynamoDB with dummy credentials
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
    
)

dynamodb = session.resource('dynamodb', endpoint_url=DYNAMODB_ENDPOINT_URL)

for table in dynamodb.tables.all():
    print(table.name)

class ContentSchema(Schema):
    contentType = fields.String(validate=validate.OneOf(['text', 'image', 'video']))
    value = fields.String()


class User(DynaModel):
    class Table:
        name = 'users'
        hash_key = 'userId'
        read = 25
        write = 5

    class ByUserType(GlobalIndex):
        name = 'by-user-type'
        hash_key = 'userType'
        range_key = 'username'
        read = 25
        write = 5
        projection = ProjectAll()

    class Schema:
        userId = fields.String(load_default=lambda: str(uuid.uuid4()))
        username = fields.String()
        email = fields.String()
        password = fields.String()
        createdAt = fields.DateTime(load_default=datetime.datetime.utcnow)
        userType = fields.String(required=True, validate=validate.OneOf(['parent', 'therapist']))
        specialization = fields.String(allow_none=True)
        childrenCount = fields.Integer(allow_none=True)

class Chat(DynaModel):
    class Table:
        name = 'chats'
        hash_key = 'chatId'
        range_key = 'timestamp'
        read = 25
        write = 5

    class BySender(GlobalIndex):
        name = 'by-sender'
        hash_key = 'senderId'
        range_key = 'timestamp'
        read = 25
        write = 5
        projection = ProjectAll()

    class ByRecipient(GlobalIndex):
        name = 'by-recipient'
        hash_key = 'recipientId'
        range_key = 'timestamp'
        read = 25
        write = 5
        projection = ProjectAll()

    class Schema:
        chatId = fields.String()
        timestamp = fields.Integer(load_default=lambda: int(time.time() * 1000))
        messageId = fields.String(load_default=lambda: str(uuid.uuid4()))
        senderId = fields.String()
        recipientId = fields.String()
        content = fields.Nested(ContentSchema)
        readAt = fields.DateTime(allow_none=True)
        createdAt = fields.DateTime(load_default=datetime.datetime.utcnow())



# # Example usage:
try:
    # Provide a userId when putting an item
    user_id = str(uuid.uuid4())
    user1 = User.put(item={
        'userId': user_id,
        'username': "alice",
        'email': "bob@example.com",
        'password': "123456",
        'userType': "parent",
        'childrenCount': 1
    })
    print(f"Result {user1}")
    print(f"User {user_id} added successfully.")
except Exception as e:
    print(f"Error putting item: {e}")

