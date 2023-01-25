from app.database.database import Base
from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Image(Base):
	__tablename__ = "image"
	
	id = Column(
		UUID(as_uuid=True), index=True,
		nullable=False, primary_key=True, default=uuid.uuid4
	)
	
	path = Column(String, nullable=True)
	attachment_id = Column(UUID(as_uuid=True), ForeignKey('attachment.id'))
	
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
