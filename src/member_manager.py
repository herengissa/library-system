"""
Member management functions for the Library Management System.
"""

from typing import List, Dict, Optional
from .database import get_connection


def get_all_members() -> List[Dict]:
    """Retrieve all members from the database."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, first_name, last_name, email, phone, membership_date
                FROM members
                ORDER BY last_name, first_name
            """)
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]


def add_member(first_name: str, last_name: str, email: str, 
               phone: Optional[str] = None) -> bool:
    """Add a new member to the database."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO members (first_name, last_name, email, phone)
                    VALUES (%s, %s, %s, %s)
                """, (first_name, last_name, email, phone))
        return True
    except Exception as e:
        print(f"Error adding member: {e}")
        return False


def search_members(search_term: str) -> List[Dict]:
    """Search for members by name or email."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, first_name, last_name, email, phone, membership_date
                FROM members
                WHERE first_name ILIKE %s 
                   OR last_name ILIKE %s 
                   OR email ILIKE %s
                ORDER BY last_name, first_name
            """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]


def get_member_by_id(member_id: int) -> Optional[Dict]:
    """Get a member by their ID."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, first_name, last_name, email, phone, membership_date
                FROM members
                WHERE id = %s
            """, (member_id,))
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                return dict(zip(columns, row))
            return None

