from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List

from app.database.database import get_db
from app.database.models import (
    User, Connection, ConnectionStatus, 
    Conversation, Message
)

from app.auth import get_current_user
from app.schemas import (
    GetConnectionResponse, UserBase, 
    CreateConversationRequest
)

from .websocket import user_websocket, broadcast_message

router = APIRouter(
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


@router.get("/networking/connections", response_model=List[GetConnectionResponse])
def get_connections(user: User = Depends(get_current_user), db: Session = Depends(get_db), 
                    ):
    connections = db.query(Connection).filter(
        and_(
            or_(
                Connection.author_id == user.id,
                Connection.recipient_id == user.id
            ),
            Connection.status == ConnectionStatus.accepted
        )
    ).all()

    users = []
    for connection in connections:
        sender = connection.sender
        recipient = connection.recipient

        users.append(
            {
                "author_id": connection.author_id,
                "sender": UserBase.from_orm(sender),  
                "recipient": UserBase.from_orm(recipient),  
            }
        )
    return users 



@router.post("/messaging/conversations")
async def create_conversation(
    data: CreateConversationRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        recipient_id = data["recipient_id"]
        content = data["content"]

        recipient = db.query(User).filter(User.id == recipient_id).first()
        if not recipient:
            raise HTTPException(status_code=404, detail="Recipient not found")
        
        existing_conversation = db.query(Conversation).filter(
            ((Conversation.author_id == user.id) & (Conversation.recipient_id == recipient_id)) | 
            ((Conversation.author_id == recipient_id) & (Conversation.recipient_id == user.id))
        ).first()
        
        if existing_conversation:
            return existing_conversation

        new_conversation = Conversation(
            author_id=user.id, 
            recipient_id=recipient_id
        )
        db.add(new_conversation)
        db.commit()
        db.refresh(new_conversation)

        new_message = Message(
            conversation_id=new_conversation.id,
            sender_id=user.id,
            recipient_id=recipient_id,
            content=content
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        await broadcast_message(user.id, new_conversation)
        return new_conversation
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@router.websocket("/ws/users/{user_id}/conversations")
async def handle_user_conversation_websocket(websocket: WebSocket, user_id: int):
    await user_websocket(websocket, user_id)