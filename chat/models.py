from marshmallow import Schema, fields, validate, validates
import datetime
import time
import uuid
from dynamorm import DynaModel, GlobalIndex, ProjectAll


class UserSchema(Schema):
    username = fields.String(required=True)
    email = fields.String(required=True)

    @validates('username')
    def validate_unique_username(self, value):
        if User.count(User.username == value):
            raise ValidationError('Username already exists.')

    @validates('email')
    def validate_unique_email(self, value):
        if User.count(User.email == value):
            raise ValidationError('Email already exists.')

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
        hash_key = 'userId'
        range_key = 'username'
        read = 25
        write = 5
        projection = ProjectAll()

    class Schema:
        userId = fields.String(load_default=lambda: str(uuid.uuid4()))
        username = fields.String(required=True)
        email = fields.String(required=True)
        password = fields.String(required=True)
        createdAt = fields.DateTime(load_default=datetime.datetime.utcnow)
        userType = fields.String(required=True, validate=validate.OneOf(['parent', 'therapist']))
        specialization = fields.String(allow_none=True)
        childrenCount = fields.Integer(allow_none=True)

    @classmethod
    def create_user(cls, data):
        schema = UserSchema()
        errors = schema.validate(data)
        print({errors})
        if errors:
            raise ValidationError(errors)
        
        return cls.put(data)

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

