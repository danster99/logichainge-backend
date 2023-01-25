from app.services.defaultService import DefaultService
from app import models, schemas


class ImageService(
	DefaultService[models.Image, schemas.ImageBase, schemas.ImageBase],
):
	"""
	Image service implementing Default_service and its CRUD methods
	"""
	def method_for_sanity_check(self):
		return "returning from child image service"


imageService = ImageService(models.Image)
