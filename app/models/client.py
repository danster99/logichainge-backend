from app.database.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text
import uuid

class Client(Base):
	__tablename__ = "client"
	
	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	client_identifier = Column(String, nullable=False)
	name = Column(String, nullable=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
