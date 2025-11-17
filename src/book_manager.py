"""
Book management functions for the Library Management System.
"""

from typing import List, Dict, Optional
from .database import get_connection


def get_all_books() -> List[Dict]:
    """Retrieve all books from the database."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, author, isbn, publication_year, 
                       category, total_copies, available_copies
                FROM books
                ORDER BY title
            """)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]


def search_books(search_term: str) -> List[Dict]:
    """Search for books by title or author."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, author, isbn, publication_year, 
                       category, total_copies, available_copies
                FROM books
                WHERE title ILIKE %s OR author ILIKE %s
                ORDER BY title
            """, (f"%{search_term}%", f"%{search_term}%"))
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]


def add_book(title: str, author: str, isbn: Optional[str] = None,
             publication_year: Optional[int] = None, category: Optional[str] = None,
             total_copies: int = 1) -> bool:
    """Add a new book to the database."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO books (title, author, isbn, publication_year, 
                                     category, total_copies, available_copies)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (title, author, isbn, publication_year, category, 
                      total_copies, total_copies))
        return True
    except Exception as e:
        print(f"Error adding book: {e}")
        return False


def get_available_books() -> List[Dict]:
    """Get all books that are currently available (available_copies > 0)."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, author, isbn, publication_year, 
                       category, total_copies, available_copies
                FROM books
                WHERE available_copies > 0
                ORDER BY title
            """)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]


def get_book_by_id(book_id: int) -> Optional[Dict]:
    """Get a book by its ID."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, author, isbn, publication_year, 
                       category, total_copies, available_copies
                FROM books
                WHERE id = %s
            """, (book_id,))
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

