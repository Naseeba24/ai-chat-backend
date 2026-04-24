AI Chat Backend — Technical Assessment
Overview

This project is a backend API that simulates a WhatsApp-style chat system.
It receives incoming messages, determines the appropriate agent (sales, support, or general), generates a reply, and stores the conversation in a database.

Tech Stack
Python 3
FastAPI
SQLite
SQLAlchemy
python-dotenv
Project Structure
ai-chat-backend/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── router.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
Setup Instructions
1. Open Project

Open the project folder in VS Code.

2. Create Virtual Environment
python -m venv venv

Activate it:

Windows:

venv\Scripts\activate
3. Install Dependencies
pip install fastapi uvicorn sqlalchemy python-dotenv

(Optional — if requirements.txt exists)

pip install -r requirements.txt
4. Environment Variables

Create a .env file in the root folder:

SECRET_TOKEN=mysecrettoken123
5. Run the Server
uvicorn main:app --reload

Server will run at:

http://127.0.0.1:8000
6. Open API Documentation

Go to:

http://127.0.0.1:8000/docs
Authentication

All requests to /webhook/whatsapp must include a Bearer token:

Authorization: Bearer mysecrettoken123

Requests without a valid token will return 401 Unauthorized.

API Endpoints
POST /webhook/whatsapp

Receives incoming messages.

Request Body:

{
  "event_id": "evt_001",
  "user_id": "user_123",
  "message": "I want to know the price"
}

Response:

{
  "reply": "Thanks for your interest. Can you share what you are looking for?"
}
POST /simulate

Simulates a message internally (used for demo/testing).

No authentication required.

GET /sessions

Returns all chat sessions.

GET /sessions/{session_id}/messages

Returns all messages for a specific session.

Database
sessions table
id (Primary Key)
user_id
agent
last_active
messages table
id (Primary Key)
session_id (Foreign Key)
role (user / assistant)
content
event_id (Unique)
Duplicate Handling

Duplicate messages are prevented using a unique constraint on event_id.
If the same event is received again, it will not be saved.

Agent Routing Logic

Simple keyword-based routing:

Sales → "price", "buy"
Support → "problem", "issue"
General → all other messages
Reply Generation

Replies are generated using a simple mock function:

Sales → interest response
Support → troubleshooting response
General → general help response

If AI integration fails, fallback responses are used.

End-to-End Flow
Incoming request received
Token is verified
Duplicate check is performed
Agent type is determined
Reply is generated
Session is created
Messages are stored in database
Reply is returned to user