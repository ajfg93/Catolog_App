from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'
	email = Column(String(250), nullable=False, unique = True)
	name = Column(String(250), nullable=True, default = "anonymous")
	picture = Column(String(250), nullable=True)
	id = Column(Integer, primary_key=True)
	password = Column(String(250), nullable=True)

class Category(Base):
	__tablename__ = 'category'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)

	@property
	def serialize(self):
		return {
		"id" : self.id,
		"name" : self.name,
		"Item" : [],
	}

class Item(Base):
	__tablename__ = 'item'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False, unique = True)
	description = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	user = relationship(User)

	@property
	def serialize(self):
		return {
			'cat_id' : self.category_id,
			'description' : self.description,
			'id' : self.id,
			'title' : self.name
		}


engine = create_engine('sqlite:///catelog_app.db')

Base.metadata.create_all(engine)