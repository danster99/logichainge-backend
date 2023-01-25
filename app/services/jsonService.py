from typing import List, Generic, Type, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app import models
from app.schemas import ActivityBase, ClientBase, ContactBase, TransportFileBase, GoodsBase, AddressBase, DepartmentBase, EmployeeBase, JsonBase
from sqlalchemy import exc
from pydantic import errors
from app.models import Activity


	
def populate_with_data_from_json(
		db: Session,
		json_data: Any
) -> Any:
	"""
	Save new activity item to the db from parent transport_file, but excluding some fields.
	"""
	print(json_data)
	return True

