# from app.database.database import Base
# from sqlalchemy import Column, Integer, String, Boolean, orm, ForeignKey, TIMESTAMP, text
# from sqlalchemy.dialects.postgresql import UUID
# import uuid
#
#
# class Document(Base):
# 	__tablename__ = "document"
#
# 	id = Column(
# 		UUID(as_uuid=True), index=True,
# 		nullable=False, primary_key=True, default=uuid.uuid4
# 	)
#
# 	path = Column(String, nullable=True)
# 	attachment_id = Column(UUID(as_uuid=True), ForeignKey('attachment.id'))


""" For implementation with attachment object """
