from app.database.database import Base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, text


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    street_1 = Column(String, nullable=False)
    street_2 = Column(String, nullable=True)
    street_3 = Column(String, nullable=True)
    zipcode = Column(String, nullable=False)
    city = Column(String, nullable=True, server_default=text("'Example_city'"))
    country = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
