from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from api.core.database import Base

class Ciudad(Base):
    __tablename__ = "ciudad"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    id_provincia = Column(Integer, ForeignKey("provincia.id"))
    
    cliente = relationship("Cliente", back_populates="ciudad", uselist=False)
    provincia = relationship("Provincia", back_populates="ciudad", uselist=False)
    
class Provincia(Base):
    __tablename__ = "provincia"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    id_pais = Column(Integer, ForeignKey("pais.id"))
    
    
    ciudad = relationship("Ciudad", back_populates="provincia", uselist=False)
    pais = relationship("Pais", back_populates="provincia", uselist=False)
    
class Pais(Base):
    __tablename__ = "pais"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, primary_key=False, nullable=False)
    

    provincia = relationship("Provincia", back_populates="pais", uselist=False)