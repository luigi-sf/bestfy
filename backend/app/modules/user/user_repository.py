from app.models.user import User
from sqlalchemy.orm import Session
from uuid import UUID
from app.modules.user.user_schema import UserCreate, UserUpdate
from app.core.security.hashed import hash_password


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: UserCreate):

        dbUser = User(
            **user.model_dump() # tranforma o model em dic ai ele passa sozinho
        )

        self.db.add(dbUser)
        self.db.commit()
        self.db.refresh(dbUser)

        return dbUser

    def list(self):
        return self.db.query(User).all() #self.db.query e filtra oq vc vai pegar

    def get_by_id(self, user_id: UUID):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def update(self, user_id: UUID, user: UserUpdate):

        dbUser = self.get_by_id(user_id)

        if not dbUser:
            return None

        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(dbUser, key, value)

        self.db.commit()
        self.db.refresh(dbUser)

        return dbUser

    def delete(self, user_id: UUID):

        dbUser = self.get_by_id(user_id)

        if not dbUser:
            return None

        self.db.delete(dbUser)
        self.db.commit()

        return dbUser