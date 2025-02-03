import uuid
from attrs import define


@define
class User:
    email: str = ""
    full_name: str = ""
    password: str = ""
    profile_photo: dict = {}
    id: str = ""


class UsersRepository:
    def __init__(self):
        self.users: list[User] = [
            User(
                email="7GxkZ@example.com",
                full_name="John Doe",
                password="password123",
                id=uuid.UUID('cd3374d0-a263-4d4d-a8c8-580116fad2e7')
            )
        ]

    def create_user(self, email: str, full_name: str, password: str) -> User:
        for user in self.users:
            if user.email == email:
                return {"error": "Email already exists"}
        
        user = User(
            email=email,
            full_name=full_name,
            password=password,
            id=self.generate_id()
        )
        self.users.append(user)
        return user 

    def get_user_by_email(self, email: str) -> User:
        for user in self.users:
            if user.email == email:
                return user
        return None  
    
    def get_user_by_id(self, user_id: str) -> User:
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def save_profile_photo(self, user_id: str, profile_photo: dict) -> User:
        user = self.get_user_by_id(user_id)
        if user: 
            user.profile_photo = profile_photo["profile_photo"]
            return user
        return None
    
    def generate_id(self) -> uuid.UUID:
        id = uuid.uuid4()
        return id




