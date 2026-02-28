from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Members(Base):

    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    age = Column(Integer)
    gender = Column(String(1), index=True)
    marital_status = Column(String(255), index=True)
    active = Column(Boolean, default=False)
