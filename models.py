"""Models for the app"""
from sqlalchemy import (
    Column, DateTime, Float, ForeignKey, Integer, Sequence, String
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# from config import engine


Base = declarative_base()


class Branch(Base):
    """Model for the DMV branches"""
    __tablename__ = 'branches'
    address = Column(String(64))
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    hours = Column(String(64))
    latitude = Column(Float)
    longitude = Column(Float)
    name = Column(String(64))
    number = Column(Integer)
    nearby1 = Column(Integer)
    nearby2 = Column(Integer)
    nearby3 = Column(Integer)
    nearby4 = Column(Integer)
    nearby5 = Column(Integer)
    region = Column(Integer)
    timestamp = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    wait_times = relationship('WaitTime')

    def __repr__(self):
        name = self.name
        number = self.number
        return f'<{name}: {number}>'


class WaitTime(Base):
    """Model for the wait times of a DMV office"""
    __tablename__ = 'wait_times'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    appt = Column(Integer)
    branch_id = Column(Integer, ForeignKey('branches.number'))
    # branch = relationship('Branch', back_populates='wait_times')
    non_appt = Column(Integer)
    # timestamp = Column(DateTime, server_default=func.now()) # only for command line stuff
    timestamp = Column(DateTime)

    def __repr__(self):
        return f'<{self.branch_id}'

"""
class Branch(Model):
    __tablename__ = 'branch'
    address = Column(String(64))
    branch_id = Column(Integer, primary_key=True)
    hours = Column(String(64))
    latitude = Column(Float)
    longitude = Column(Float)
    name = Column(String(64))
    number = Column(Integer)
    nearby1 = Column(Integer)
    nearby2 = Column(Integer)
    nearby3 = Column(Integer)
    nearby4 = Column(Integer)
    nearby5 = Column(Integer)
    region = Column(Integer)
    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class BranchSchema(ma.ModelSchema):
    class Meta:
        model = Branch
        sqla_session = session
"""
