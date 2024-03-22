from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Crea una base de datos SQLite
Base = declarative_base()

# Tabla generator
class dbGenerator(Base):
    __tablename__ = 'generator'
    id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    measure = relationship('dbMeasure', backref='generator')

# Tabla measure
class dbMeasure(Base):
    __tablename__ = 'measure'
    id = Column(Integer, primary_key=True, autoincrement=True)
    generator_id = Column(Integer, ForeignKey('generator.id'))
    production = Column(Float)
    state = Column(Boolean)
    datetime = Column(String)

# Crea una base de datos SQLite
engine = create_engine("sqlite:///./concentrator_data.db")
