import bcrypt
from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

salt = bcrypt.gensalt()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False, unique=True)
  password = Column(String(100), nullable=False)

  @validates('email')
  def validate_email(self, key, email):
    # Make sure email address contains @ character.
    assert '@' in email
    return email
  
  @validates('password')
  def validate_password(self, key, password):
    # Validate and hash password before storing.
    assert len(password) > 4
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

  def verify_password(self, password):
    return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))