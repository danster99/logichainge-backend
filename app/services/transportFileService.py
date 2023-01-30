from typing import Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import update
from app import models, schemas
from app.schemas.transportFile import TransportFileBase
from app.services import contactService, clientService, employeeService, \
    departmentService, activityService, \
    goodsService, addressService, attachmentService


def get_all_transport_file(db: Session):
    """
    Get all transport_files from the db.
    """

    result = {"count":db.query(models.TransportFile).count(), "transport_files" : db.query(models.TransportFile).all()}

    return result


def get_all_transport_file_by_status(db: Session, status: str):
    """
    Get all transport files filtered by status from the db.
    """

    all_transport_files_by_status = db.query(models.TransportFile) \
        .filter(models.TransportFile.tr_file_status == status) \
        .all()
    for db_transport_file in all_transport_files_by_status:
        db_transport_file.first_activity = db.query(models.Activity).filter(models.Activity.transport_file_id == db_transport_file.id).order_by(models.Activity.sequence_id.asc()).first()
        db_transport_file.last_activity = db.query(models.Activity).filter(models.Activity.transport_file_id == db_transport_file.id).order_by(models.Activity.sequence_id.desc()).first()

    return all_transport_files_by_status


def get_transport_file(db: Session, id: int):
    """
    Get a transport file by id from the db.
    """

    db_transport_file = db.query(models.TransportFile).filter(models.TransportFile.id == id).first()

    # db_transport_file.client_name = db_transport_file.client.name
    # db_transport_file.contact_name = db_transport_file.contact.name
    # db_transport_file.contact_mobile = db_transport_file.contact.mobile
    # db_transport_file.dep_name = db_transport_file.department.name
    
    

    # db_transport_file.goods_gross_weight = db_transport_file.activities[0].goods[0].gross_weight
    # db_transport_file.goods_net_weight = db_transport_file.activities[0].goods[0].net_weight
    # db_transport_file.goods_loading_meters = db_transport_file.activities[0].goods[0].loading_meters

    return db_transport_file


def save_transport_file_basic_fields(db: Session, transport_file_in: TransportFileBase, ) -> Any:
    """
    Save a transport file to the db, but excluding nested objects
    """
    transport_file_data = jsonable_encoder(
        transport_file_in,
        exclude={"client", "contact", "department", "employee", "activities"})

    db_transport_file = models.TransportFile(**transport_file_data)

    db.add(db_transport_file)
    db.commit()
    db.refresh(db_transport_file)
    return db_transport_file


def save_transport_file(db: Session, transport_file_in: TransportFileBase, ) -> Any:
    """
    Save a transport file to the db.
    """
    transport_file_data = jsonable_encoder(transport_file_in)
    db_transport_file = models.TransportFile(**transport_file_data)

    db.add(db_transport_file)
    db.commit()
    db.refresh(db_transport_file)
    return db_transport_file


# def save_transport_file_full(db: Session, transport_file_in: TransportFileIn, ) -> Any:
#     """
#     Save a full transport file to the db (with nested objects).

#     First persists nested objects (client, employee, department, contact, attachment) separately.
#     Then save foreign keys of created object to the root transport_file object.
#     Then persists root transport_file itself

#     Then persists nested Activity and Goods objects, by looping over the list and adding transprot_file id as their
#     foreign key.


#     Can be improved:
#     - nested for loops are inefficient
#     - relationships between object is set up, but due to large changes
#     from initial scope, they can be modified to better match requirements
#     """

#     # First persisting nested objects with foreign keys in transport file
#     db_client = clientService.create(db=db, obj_in=transport_file_in.client)
#     db_employee = employeeService.create(db=db, obj_in=transport_file_in.employee)
#     db_department = departmentService.create(db=db, obj_in=transport_file_in.department)
#     db_contact = contactService.create(db=db, obj_in=transport_file_in.contact)

#     attachmentService.create(db=db, obj_in=transport_file_in.attachment)

#     # Saving foreign keys to root transport_file and persisting the transport_file
#     transport_file_in.client_id = db_client.id
#     transport_file_in.employee_id = db_employee.id
#     transport_file_in.department_id = db_department.id
#     transport_file_in.contact_id = db_contact.id

#     db_new_tr_file = save_transport_file_basic_fields(db, transport_file_in)

#     # Looping over list of activities and goods to persists separately with tr_file_id as foreign key
#     for a in transport_file_in.activities:
#         # Persisting address nested object
#         db_address = addressService.save_address(db=db, address_in=a.address)

#         a.address_id = db_address.id
#         a.transport_file_id = db_new_tr_file.id

#         db_activity = activityService.save_activity_basic_fields(db=db, activity_in=a)

#         for g in a.goods:
#             g.activity_id = db_activity.activity_reference
#             goodsService.save_goods_basic_fields(db=db, goods_in=g)

#     return_file = get_transport_file(db, db_new_tr_file.id)

#     return return_file





def update_transport_file(db: Session, transport_file_update: TransportFileBase, id: int):
    """
    Update only basic transport_file fields
    """
    tr_file_query = {}
    stmt = (
        update(models.TransportFile)
        .where(models.TransportFile.id == id)
        .values(transport_file_update.dict(
        exclude={
            "client", "contact", "department",
            "employee", "activities"
        }))
    )
    db.execute(stmt)
    db.commit()
    tr_file_query = db.query(models.TransportFile).filter(models.TransportFile.id == id).first()

    return tr_file_query

def mark_transport_file_as_reported(db: Session, id: int):
    """
    Mark the transport file as reported by user as incorrect or incomplete
    """
    tr_file_query = {}
    stmt = (
        update(models.TransportFile)
        .where(models.TransportFile.id == id)
        .values({"reported" : True})
    )
    db.execute(stmt)
    db.commit()

    return True


def delete_transport_file(db: Session, id: int):
    """
    Delete a transport file from the db.
    """
    transport_file_to_delete = get_transport_file(db, id)
    db.delete(transport_file_to_delete)
    db.commit()
    return transport_file_to_delete
