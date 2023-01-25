from pydantic import BaseModel
import datetime
from typing import List, Optional
from uuid import UUID
from app.schemas import ImageOut, ImageBase


class AttachmentBase(BaseModel):
	"""
	Attachment BASE schema
	"""
	base_url: str
	
	class Config:
		orm_mode = True


class AttachmentIn(AttachmentBase):
	"""
	Attachment IN schema, inheriting fields from Base class
	"""
	tr_file_id: int
	images: Optional[List[ImageBase]]


class AttachmentOut(AttachmentBase):
	"""
	Attachment OUT schema, inheriting fields from Base class
	"""
	id: UUID
	tr_file_id: int
	images: List[ImageOut]
	created_at: datetime.datetime
	
	