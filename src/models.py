"""Database models för biblioteket."""

from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Book(Base):
    """Bok i biblioteket."""
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    isbn = Column(String(20), unique=True)
    publication_year = Column(Integer)
    category = Column(String(100))
    total_copies = Column(Integer, default=1, nullable=False)
    available_copies = Column(Integer, default=1, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    loans = relationship("Loan", back_populates="book", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint('total_copies > 0', name='check_total_copies_positive'),
        CheckConstraint('available_copies >= 0', name='check_available_copies_non_negative'),
        CheckConstraint('available_copies <= total_copies', name='check_available_not_exceed_total'),
    )
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"


class Member(Base):
    """Medlem i biblioteket."""
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    membership_date = Column(Date, default=date.today)
    created_at = Column(DateTime, default=datetime.now)
    
    loans = relationship("Loan", back_populates="member", cascade="all, delete-orphan")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<Member(id={self.id}, name='{self.full_name}', email='{self.email}')>"


class Loan(Base):
    """Lån av bok."""
    __tablename__ = 'loans'
    
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE'), nullable=False)
    loan_date = Column(Date, default=date.today, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)
    created_at = Column(DateTime, default=datetime.now)
    
    book = relationship("Book", back_populates="loans")
    member = relationship("Member", back_populates="loans")
    
    __table_args__ = (
        CheckConstraint('due_date >= loan_date', name='check_due_after_loan'),
        CheckConstraint('return_date IS NULL OR return_date >= loan_date', name='check_return_after_loan'),
    )
    
    @property
    def is_overdue(self):
        if self.return_date:
            return False
        return self.due_date < date.today()
    
    @property
    def days_overdue(self):
        if not self.is_overdue:
            return 0
        return (date.today() - self.due_date).days
    
    def __repr__(self):
        return f"<Loan(id={self.id}, book_id={self.book_id}, member_id={self.member_id}, due={self.due_date})>"

