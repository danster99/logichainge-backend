from app.database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
import uuid

class Token(Base):
	__tablename__ = "token"
	
	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
	access_token = Column(String, nullable=False)
	token_type = Column(String, nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))