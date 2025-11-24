"""Hantering av böcker."""

from typing import List, Dict, Optional
from sqlalchemy import or_
from .database import get_session
from .models import Book


def _book_to_dict(book: Book) -> Dict:
    """Konverterar Book-objekt till dictionary."""
    return {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'publication_year': book.publication_year,
        'category': book.category,
        'total_copies': book.total_copies,
        'available_copies': book.available_copies
    }


def get_all_books() -> List[Dict]:
    """Hämtar alla böcker."""
    with get_session() as session:
        books = session.query(Book).order_by(Book.title).all()
        return [_book_to_dict(book) for book in books]


def search_books(search_term: str) -> List[Dict]:
    """Söker efter böcker på titel eller författare."""
    with get_session() as session:
        search = f"%{search_term}%"
        books = session.query(Book).filter(
            or_(
                Book.title.ilike(search),
                Book.author.ilike(search)
            )
        ).order_by(Book.title).all()
        return [_book_to_dict(book) for book in books]


def add_book(title: str, author: str, isbn: Optional[str] = None,
             publication_year: Optional[int] = None, category: Optional[str] = None,
             total_copies: int = 1) -> bool:
    """Lägger till en ny bok."""
    try:
        with get_session() as session:
            book = Book(
                title=title,
                author=author,
                isbn=isbn,
                publication_year=publication_year,
                category=category,
                total_copies=total_copies,
                available_copies=total_copies
            )
            session.add(book)
            session.commit()
            return True
    except Exception as e:
        print(f"Kunde inte lägga till bok: {e}")
        return False


def get_available_books() -> List[Dict]:
    """Hämtar alla tillgängliga böcker."""
    with get_session() as session:
        books = session.query(Book).filter(
            Book.available_copies > 0
        ).order_by(Book.title).all()
        return [_book_to_dict(book) for book in books]


def get_book_by_id(book_id: int) -> Optional[Dict]:
    """Hämtar en bok via ID."""
    with get_session() as session:
        book = session.query(Book).filter(Book.id == book_id).first()
        if book:
            return _book_to_dict(book)
        return None

