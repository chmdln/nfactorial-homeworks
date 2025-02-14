import uuid
from attrs import define
from sqlalchemy.orm import Session

from app.database.models import User
from app.utils import hash 


@define
class UserCreate:
    email: str = ""
    full_name: str = ""
    password: str = ""
    profile_photo: dict = {}
    

class UsersRepository:
    def create_user(self, db: Session, user: UserCreate) -> User:

        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user: 
            return {"error": "Email already exists"}
        
        db_user = User(
            email=user.email,
            full_name=user.full_name,
            password=hash(user.password),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user 

    def get_user_by_email(self, db: Session, email: str) -> User:
        db_user = db.query(User).filter(User.email == email).first()
        if db_user: 
            return db_user
        return None  
    
    def get_user_by_id(self, db: Session, user_id: str) -> User:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user: 
            return db_user 
        return None
    
    def save_profile_photo(self, db: Session, user_id: str, profile_photo: dict) -> User:
        user = self.get_user_by_id(db, user_id)
        if user: 
            user.profile_photo = profile_photo["profile_photo"]
            db.commit()
            db.refresh(user)
            return user
        return None
    
    # def generate_id(self) -> uuid.UUID:
    #     id = uuid.uuid4()
    #     return id




