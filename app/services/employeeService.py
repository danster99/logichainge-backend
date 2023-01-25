from app.services.defaultService import DefaultService
from app import models, schemas


class EmployeeService(
	DefaultService[models.Employee, schemas.EmployeeBase, schemas.EmployeeBase],
):
	"""
	Employee service implementing Default_service and its CRUD methods
	"""
	def method_for_sanity_check(self):
		return "returning from child employee service"


employeeService = EmployeeService(models.Employee)
