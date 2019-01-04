from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# ------create local permission system:


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    email = Column(String(250))
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
           'name': self.name,
           'id': self.id,
           'email': self.email,
           'picture': self.piecture,
           }
# ------


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

# -----user local permission
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
# -----user local permission

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            # 'user_id': self.user_id
            }


class ListItem(Base):
    __tablename__ = 'list_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

# -----user local permission
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
# -----user local permission

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            # 'user_id': self.user_id
        }

# engine = create_engine('sqlite:///analysislists.db')


engine = create_engine('sqlite:///analysislists_withusers.db')


Base.metadata.create_all(engine)
