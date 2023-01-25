from datetime import datetime

from pydantic import BaseModel


class AddressBase(BaseModel):
	"""
	Address BASE schema
	"""
	name: str
	street_1: str
	street_2: str
	street_3: str
	zipcode: str
	city: str
	country: str
	latitude: float
	longitude: float
	
	class Config:
		orm_mode = True


class AddressOut(AddressBase):
	"""
	Address OUT schema, inheriting fields from Base class
	"""
	id: int
	created_at: datetime
	