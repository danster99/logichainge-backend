from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class TokenBase(BaseModel):
	"""
	User BASE schema
	"""

	user_id: int
	access_token: str
	token_type: str
	
	class Config:
		orm_mode = True
	

class TokenOut(TokenBase):
	"""
	Client OUT schema, inheriting fields from Base class
	"""
	id: int
	created_at: datetime

