"""Hantering av lån."""

from datetime import date, timedelta
from typing import List, Dict
from sqlalchemy import and_
from .database import get_session
from .models import Loan, Book, Member


def register_loan(book_id: int, member_id: int, loan_days: int = 14) -> bool:
    """Registrerar ett nytt lån."""
    try:
        with get_session() as session:
            # Kolla om boken finns och är tillgänglig
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                print("Fel: Boken hittades inte")
                return False
            
            if book.available_copies <= 0:
                print("Fel: Inga exemplar tillgängliga")
                return False
            
            # Kolla om medlemmen finns
            member = session.query(Member).filter(Member.id == member_id).first()
            if not member:
                print("Fel: Medlemmen hittades inte")
                return False
            
            # Skapa lånet
            loan_date = date.today()
            due_date = loan_date + timedelta(days=loan_days)
            
            loan = Loan(
                book_id=book_id,
                member_id=member_id,
                loan_date=loan_date,
                due_date=due_date
            )
            session.add(loan)
            
            # Minska antal tillgängliga exemplar
            book.available_copies -= 1
            
            session.commit()
            return True
    except Exception as e:
        print(f"Kunde inte registrera lån: {e}")
        return False


def register_return(loan_id: int) -> bool:
    """Registrerar återlämning av bok."""
    try:
        with get_session() as session:
            loan = session.query(Loan).filter(Loan.id == loan_id).first()
            if not loan:
                print("Fel: Lånet hittades inte")
                return False
            
            if loan.return_date:
                print("Fel: Boken är redan återlämnad")
                return False
            
            # Sätt återlämningsdatum
            loan.return_date = date.today()
            
            # Öka antal tillgängliga exemplar
            book = session.query(Book).filter(Book.id == loan.book_id).first()
            if book:
                book.available_copies += 1
            
            session.commit()
            return True
    except Exception as e:
        print(f"Kunde inte registrera återlämning: {e}")
        return False


def get_active_loans() -> List[Dict]:
    """Hämtar alla aktiva lån."""
    with get_session() as session:
        loans = session.query(Loan).join(Book).join(Member).filter(
            Loan.return_date.is_(None)
        ).order_by(Loan.due_date).all()
        
        result = []
        for loan in loans:
            result.append({
                'id': loan.id,
                'book_id': loan.book_id,
                'member_id': loan.member_id,
                'loan_date': loan.loan_date,
                'due_date': loan.due_date,
                'book_title': loan.book.title,
                'member_name': loan.member.full_name
            })
        return result


def get_overdue_loans() -> List[Dict]:
    """Hämtar alla försenade lån."""
    with get_session() as session:
        today = date.today()
        loans = session.query(Loan).join(Book).join(Member).filter(
            and_(
                Loan.return_date.is_(None),
                Loan.due_date < today
            )
        ).order_by(Loan.due_date).all()
        
        result = []
        for loan in loans:
            result.append({
                'id': loan.id,
                'book_id': loan.book_id,
                'member_id': loan.member_id,
                'loan_date': loan.loan_date,
                'due_date': loan.due_date,
                'days_overdue': loan.days_overdue,
                'book_title': loan.book.title,
                'member_name': loan.member.full_name,
                'member_email': loan.member.email
            })
        return result

