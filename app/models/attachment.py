from app.database.database import Base
from sqlalchemy import Column, Integer, String, orm, ForeignKey, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Attachment(Base):
	"""Meant to replace tr_file_image_ref in root Transport_file object"""

	__tablename__ = "attachment"
	
	id = Column(
		UUID(as_uuid=True), index=True,
		nullable=False, primary_key=True, default=uuid.uuid4
	)
	tr_file_id = Column(Integer, ForeignKey('transport_file.id'))
	base_url = Column(String, nullable=True)
	
	images = orm.relationship('Image')
	# documents = orm.relationship('Document')

	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

	
	