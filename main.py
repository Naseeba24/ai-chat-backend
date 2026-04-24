from fastapi import FastAPI, Header, HTTPException
from database import Base, engine, SessionLocal
from models import Session, Message
from schemas import MessageRequest
from router import get_agent, generate_reply
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

SECRET_TOKEN = os.getenv("SECRET_TOKEN")


def verify_token(auth_header: str):
    if auth_header != f"Bearer {SECRET_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.post("/webhook/whatsapp")
def receive_message(data: MessageRequest, authorization: str = Header(...)):
    verify_token(authorization)

    db = SessionLocal()

    # check duplicate
    existing = db.query(Message).filter_by(event_id=data.event_id).first()
    if existing:
        return {"message": "Duplicate event ignored"}

    agent = get_agent(data.message)
    reply = generate_reply(agent)

    # create session
    session = Session(
        user_id=data.user_id,
        agent=agent,
        last_active="now"
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # save messages
    user_msg = Message(
        session_id=session.id,
        role="user",
        content=data.message,
        event_id=data.event_id
    )

    bot_msg = Message(
        session_id=session.id,
        role="assistant",
        content=reply,
        event_id=data.event_id + "_reply"
    )

    db.add(user_msg)
    db.add(bot_msg)
    db.commit()

    return {"reply": reply}


@app.post("/simulate")
def simulate():
    return receive_message(
        MessageRequest(
            event_id="evt_test",
            user_id="user_test",
            message="I want price"
        ),
        authorization=f"Bearer {SECRET_TOKEN}"
    )


@app.get("/sessions")
def get_sessions():
    db = SessionLocal()
    return db.query(Session).all()


@app.get("/sessions/{session_id}/messages")
def get_messages(session_id: int):
    db = SessionLocal()
    return db.query(Message).filter_by(session_id=session_id).all()