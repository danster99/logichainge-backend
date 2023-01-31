from app.database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text, orm
from sqlalchemy.orm import relationship, backref


class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    activity_reference = Column(String, nullable=False)
    transport_file_id = Column(Integer, ForeignKey('transport_file.id'))
    transport_file = relationship('Transport_file', backref = backref('Activity', cascade = "all, delete-orphan"))
    sequence_id = Column(Integer, nullable=True)
    activity_type = Column(String, nullable=False)  # Can be converted to ENUM
    address_id = Column(Integer, ForeignKey('address.id'))
    address = orm.relationship('Address')

    """ Uses String because of conversion issues with Date type, but can be replaced"""
    date = Column(String, nullable=True)
    time_prefix = Column(String, nullable=True)
    time_1 = Column(String, nullable=True)
    time_2 = Column(String, nullable=True)
    instructions = Column(String, nullable=False)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    contact = orm.relationship('Contact')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

