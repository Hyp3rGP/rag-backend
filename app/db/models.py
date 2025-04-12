from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey, Table, ARRAY
from sqlalchemy.orm import relationship
from .database import Base

class Document(Base):
    __tablename__ = "Document"
    docID = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    author = Column(Text)
    keywords = Column(ARRAY(Text))
    content = Column(Text)
    category = Column(Text)
    uploadDate = Column(TIMESTAMP)

class RAGEEngine(Base):
    __tablename__ = "RAGEEngine"
    queryID = Column(Integer, primary_key=True)
    queryText = Column(Text)
    responseText = Column(Text)

class RetrievedDocuments(Base):
    __tablename__ = "RetrievedDocuments"
    queryID = Column(Integer, ForeignKey("RAGEEngine.queryID", ondelete="CASCADE"), primary_key=True)
    docID = Column(Integer, ForeignKey("Document.docID", ondelete="CASCADE"), primary_key=True)

class User(Base):
    __tablename__ = "User"
    userID = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    email = Column(Text, unique=True)
    password = Column(Text)
    role = Column(Text)

class ChatHistory(Base):
    __tablename__ = "ChatHistory"
    chatID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey("User.userID", ondelete="CASCADE"))
    messages = Column(ARRAY(Text))
    timestamp = Column(TIMESTAMP)
    saved = Column(Boolean)
    archived = Column(Boolean)


class Report(Base):
    __tablename__ = "Report"
    reportID = Column(Integer, primary_key=True)
    generatedBy = Column(Integer, ForeignKey("Admin.adminID", ondelete="SET NULL"))
    date = Column(TIMESTAMP)
    content = Column(Text)
    reportType = Column(Text)

class Admin(Base):
    __tablename__ = "Admin"
    adminID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey("User.userID", ondelete="CASCADE"), unique=True)

