from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class BodyPart(Base):
	__tablename__ = 'bodypart'

	name = Column(String(250), nullable = False)
	description = Column(String(1000))
	id = Column(Integer, primary_key = True)

class WorkoutMovement(Base):
	__tablename__ = 'movement'

	name = Column(String(250), nullable = False)
	id = Column(Integer, primary_key = True)
	personal_record = Column(String(30))
	bodypart = relationship(BodyPart)
	bodypart_id = Column(Integer, ForeignKey('bodypart.id'))


engine = create_engine('sqlite:///workoutmovement.db')
Base.metadata.create_all(engine)