from app.database.database import Base
from sqlalchemy import Column, Integer, String, orm, ForeignKey, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID

class Attachment(Base):
	"""Meant to replace tr_file_image_ref in root Transport_file object"""

	__tablename__ = "attachment"
	
	id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
	tr_file_id = Column(Integer, ForeignKey('transport_file.id'))
	url = Column(String, nullable=True)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	
	