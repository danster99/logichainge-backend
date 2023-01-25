from datetime import datetime
from pydantic import BaseModel


class ClientBase(BaseModel):
	"""
	Client BASE schema
	"""

	# transport_file_id: int
	client_identifier: str
	name: str
	
	class Config:
		orm_mode = True
	
	
class ClientOut(ClientBase):
	"""
	Client OUT schema, inheriting fields from Base class
	"""
	id: int
	created_at: datetime
	