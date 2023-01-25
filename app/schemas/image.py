from pydantic import BaseModel
import datetime
from uuid import UUID


class ImageBase(BaseModel):
	"""
	Image base schema
	"""
	path: str
	
	
class ImageOut(ImageBase):
	"""
	Image OUT schema, inheriting fields from Base class
	"""
	id: UUID
	attachment_id: UUID
	created_at: datetime.datetime
	