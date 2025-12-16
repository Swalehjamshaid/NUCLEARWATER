
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String(50), default="user")  # 'admin' or 'user'
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    websites = relationship("Website", back_populates="owner")

class Website(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    url = Column(String(512), nullable=False)
    name = Column(String(255), nullable=True)
    schedule = Column(String(50), default="manual")  # weekly | monthly | manual
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="websites")
    audits = relationship("Audit", back_populates="website")

class Audit(Base):
    __tablename__ = "audits"
    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey("websites.id"), nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(50), default="queued")  # queued | running | done | failed
    score = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)  # list of module results
    report = Column(Text, nullable=True)

   
