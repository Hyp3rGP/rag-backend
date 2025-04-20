from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    Boolean,
    ForeignKey,
    Table,
    ARRAY,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "User"

    userID = Column(Integer, primary_key=True, index=True)
    name = Column(Text)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    role = Column(Text, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    __table_args__ = (
        Index("only_one_admin", "is_admin", unique=True, postgresql_where=(is_admin == True)),
    )


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


class ChatHistory(Base):
    __tablename__ = "ChatHistory"

    chatID = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey("User.userID", ondelete="CASCADE"))
    messages = Column(ARRAY(Text))
    timestamp = Column(TIMESTAMP)
    saved = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)


class Report(Base):
    __tablename__ = "Report"

    reportID = Column(Integer, primary_key=True)
    generatedBy = Column(Integer, ForeignKey("User.userID", ondelete="SET NULL"))  # Must be admin
    date = Column(TIMESTAMP)
    content = Column(Text)
    reportType = Column(Text)


class ActionLog(Base):
    __tablename__ = "ActionLog"

    logID = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, ForeignKey("User.userID", ondelete="SET NULL"))
    action = Column(Text, nullable=False)          
    target_table = Column(Text, nullable=False)    
    target_id = Column(Integer, nullable=True)     
    timestamp = Column(TIMESTAMP)
    themetadata = Column(Text)                        
