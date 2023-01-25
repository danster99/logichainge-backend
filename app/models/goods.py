from app.database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, text


class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    activity_id = Column(Integer, ForeignKey('activity.id'))
    unit_type = Column(String, nullable=False)
    stackable = Column(Boolean, default=False, nullable=False)
    quantity = Column(String, default="1", nullable=False)
    description = Column(String, nullable=False)
    loading_meters = Column(String, nullable=False)
    net_weight = Column(String, nullable=True)
    gross_weight = Column(String, nullable=False)
    dangerous_goods = Column(Boolean, default=False, nullable=False)
    dg_class = Column(String, nullable=True)
    dg_product_group = Column(String, nullable=True)
    dg_un_code = Column(String, nullable=True)
    dg_technical_name = Column(String, nullable=True)
    
    size = Column(String, nullable=False)
    volume_cbm = Column(String, nullable=False)

    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    