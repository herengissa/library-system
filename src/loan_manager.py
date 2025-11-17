"""
Loan management functions for the Library Management System.
"""

from datetime import date, timedelta
from typing import List, Dict, Optional
from .database import get_connection


def register_loan(book_id: int, member_id: int, loan_days: int = 14) -> bool:
    """Register a new loan. Returns True if successful, False otherwise."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Check if book exists and is available
                cur.execute("""
                    SELECT available_copies FROM books WHERE id = %s
                """, (book_id,))
                result = cur.fetchone()
                
                if result is None:
                    print("Error: Book not found")
                    return False
                
                available_copies = result[0]
                if available_copies <= 0:
                    print("Error: No copies available")
                    return False
                
                # Check if member exists
                cur.execute("SELECT id FROM members WHERE id = %s", (member_id,))
                if cur.fetchone() is None:
                    print("Error: Member not found")
                    return False
                
                # Create loan
                loan_date = date.today()
                due_date = loan_date + timedelta(days=loan_days)
                
                cur.execute("""
                    INSERT INTO loans (book_id, member_id, loan_date, due_date)
                    VALUES (%s, %s, %s, %s)
                """, (book_id, member_id, loan_date, due_date))
                
                # Update available copies
                cur.execute("""
                    UPDATE books 
                    SET available_copies = available_copies - 1
                    WHERE id = %s
                """, (book_id,))
        
        return True
    except Exception as e:
        print(f"Error registering loan: {e}")
        return False


def register_return(loan_id: int) -> bool:
    """Register the return of a book. Returns True if successful."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Get loan information
                cur.execute("""
                    SELECT book_id, return_date FROM loans WHERE id = %s
                """, (loan_id,))
                result = cur.fetchone()
                
                if result is None:
                    print("Error: Loan not found")
                    return False
                
                book_id, return_date = result
                if return_date is not None:
                    print("Error: Book already returned")
                    return False
                
                # Update loan with return date
                cur.execute("""
                    UPDATE loans 
                    SET return_date = %s
                    WHERE id = %s
                """, (date.today(), loan_id))
                
                # Update available copies
                cur.execute("""
                    UPDATE books 
                    SET available_copies = available_copies + 1
                    WHERE id = %s
                """, (book_id,))
        
        return True
    except Exception as e:
        print(f"Error registering return: {e}")
        return False


def get_active_loans() -> List[Dict]:
    """Get all active loans (not returned)."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT l.id, l.book_id, l.member_id, l.loan_date, l.due_date,
                       b.title AS book_title,
                       m.first_name || ' ' || m.last_name AS member_name
                FROM loans l
                JOIN books b ON l.book_id = b.id
                JOIN members m ON l.member_id = m.id
                WHERE l.return_date IS NULL
                ORDER BY l.due_date
            """)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]


def get_overdue_loans() -> List[Dict]:
    """Get all overdue loans (due_date passed but not returned)."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT l.id, l.book_id, l.member_id, l.loan_date, l.due_date,
                       CURRENT_DATE - l.due_date AS days_overdue,
                       b.title AS book_title,
                       m.first_name || ' ' || m.last_name AS member_name,
                       m.email AS member_email
                FROM loans l
                JOIN books b ON l.book_id = b.id
                JOIN members m ON l.member_id = m.id
                WHERE l.return_date IS NULL 
                  AND l.due_date < CURRENT_DATE
                ORDER BY days_overdue DESC
            """)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]

