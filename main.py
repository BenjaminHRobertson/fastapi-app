 
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# ✅ SQLite Database (Simple for Testing)
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ Define ChatMessage Table
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    bot_response = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# ✅ Dependency to Get Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Home Route
@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

# ✅ Save Chat Endpoint
@app.post("/save_chat/")
def save_chat(user_message: str, bot_response: str, db: Session = Depends(get_db)):
    chat = ChatMessage(user_message=user_message, bot_response=bot_response)
    db.add(chat)
    db.commit()
    return {"status": "Chat saved!"}

# ✅ Get Chat History Endpoint
@app.get("/get_chats/")
def get_chats(db: Session = Depends(get_db)):
    chats = db.query(ChatMessage).all()
    return {"history": [{"user_message": c.user_message, "bot_response": c.bot_response} for c in chats]}
