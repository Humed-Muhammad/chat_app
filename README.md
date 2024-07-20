# ChatApp: Real-time Messaging Application for Parent-Therapist Communication

## Overview

ChatApp is a robust, scalable real-time messaging application built with modern web technologies and leveraging the power of AWS services. This application facilitates secure communication between parents and therapists, allowing for efficient exchange of text, image, and video content.

### How It Works

1. Users (parents and therapists) interact with the frontend application.
2. The frontend communicates with a Django backend API hosted on an EC2 instance.
3. User authentication is handled securely, with passwords stored safely in DynamoDB.
4. Real-time messaging is facilitated through WebSocket connections.
5. Messages and user data are stored in DynamoDB for quick access and scalability.
6. Users can share text, images, and videos within their conversations.

## Technology Choices

We've leveraged several AWS services for this application, each chosen for specific reasons:

1. **EC2 (Elastic Compute Cloud)**: Hosts our Django backend, providing a flexible and scalable compute platform.

2. **DynamoDB**: A NoSQL database service used for storing user data, chat messages, and WebSocket connections. Chosen for its low-latency performance and automatic scaling capabilities.

3. **S3 (Simple Storage Service)**: Used for storing image and video content shared in chats. S3 provides durability, availability, and performance for object storage.

4. **Lambda**: Serverless compute service used for background tasks and event-driven processes. It allows us to run code without provisioning servers (for working with ApiGateWay).

5. **ApiGateWay (Socket)**: Real-time communication

6. **Supervisor and Gunicorn**: Used to manage our Django application processes on EC2, ensuring high availability and efficient resource utilization.

## Data Model

Our data model is designed for efficiency and scalability:

1. **Users Table**:

   - Partition Key: userId
   - Attributes: username, email, password, createdAt, userType, specialization, childrenCount
   - Global Secondary Index: by-user-type (hash key: userId, range key: username)

2. **Chats Table**:

   - Partition Key: id
   - Attributes: messageId, createdAt, senderId, recipientId, content (nested: contentType, value), readAt

3. **WebSocketConnections Table**:
   - Partition Key: userId
   - Attributes: connectionId

This model allows for efficient user management, quick retrieval of messages, and real-time WebSocket communication.

## Key Features

1. **User Types**: The application supports two user types - 'parent' and 'therapist'.
2. **Specialized Profiles**: Therapists can specify their specialization, while parents can indicate their number of children.
3. **Real-time Messaging**: Users can send and receive messages in real-time.
4. **Multi-media Support**: The chat supports text, image, and video content.
5. **Read Receipts**: Messages include a 'readAt' timestamp to indicate when they were read.

## Setup and Running the Application

### Prerequisites

- AWS Account with appropriate permissions
- GitHub account
- Python 3.8+ installed locally

### Step-by-Step Guide For Django backend

1. **Clone the repository and set up environment**:

```bash

git clone https://github.com/Humed-Muhammad/chat_app.git
cd chat_app
cp .env.example .env

```

2. **Activate venv ( virtual Environment)**:

```bash

python -m venv venv
source venv/bin/activate

```

3. **Run the Seeder**:

```bash

python seed.py

```

4. **Run the application (Django Api)**:

```bash

python manage.py runserver

```
