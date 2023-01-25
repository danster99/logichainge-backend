from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.services.defaultService import DefaultService
from app import models, schemas, services


class AttachmentService(
	DefaultService[models.Attachment, schemas.AttachmentIn, schemas.AttachmentIn],
):
	"""
	Attachment service implementing Default_service and its CRUD methods
	"""

	def method_for_sanity_check(self):
		return "returning from child attachment service"
	
	def create(self, db: Session, *, obj_in: schemas.AttachmentIn) -> schemas.AttachmentOut:
		"""
		Overriding create methods from Default_service
		"""

		obj_in_data = jsonable_encoder(obj_in)
		
		for i in obj_in_data.images:
			services.imageService.create(db=db, obj_in=i)
		
		db_obj = self.model(**obj_in_data)
		db.add(db_obj)
		db.commit()
		db.refresh(db_obj)
		return db_obj


attachmentService = AttachmentService(models.Attachment)
