from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from api.core.database import Base


class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    telefono = Column(String, primary_key=False, nullable=False)
    email = Column(String, primary_key=False, nullable=False)
    direccion = Column(String, primary_key=False, nullable=False)
    id_ciudad = Column(Integer, ForeignKey("ciudad.id"))
    
    ciudad = relationship("Ciudad", back_populates="cliente", uselist=False)
    # condicion_entrega = Column(Date, primary_key=False, nullable=False) --> Revisar si esto va en Cliente