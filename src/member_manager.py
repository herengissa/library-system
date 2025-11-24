"""Hantering av medlemmar."""

from typing import List, Dict, Optional
from sqlalchemy import or_
from .database import get_session
from .models import Member


def _member_to_dict(member: Member) -> Dict:
    """Konverterar Member-objekt till dictionary."""
    return {
        'id': member.id,
        'first_name': member.first_name,
        'last_name': member.last_name,
        'email': member.email,
        'phone': member.phone,
        'membership_date': member.membership_date
    }


def get_all_members() -> List[Dict]:
    """Hämtar alla medlemmar."""
    with get_session() as session:
        members = session.query(Member).order_by(
            Member.last_name, Member.first_name
        ).all()
        return [_member_to_dict(member) for member in members]


def add_member(first_name: str, last_name: str, email: str, 
               phone: Optional[str] = None) -> bool:
    """Lägger till en ny medlem."""
    try:
        with get_session() as session:
            member = Member(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )
            session.add(member)
            session.commit()
            return True
    except Exception as e:
        print(f"Kunde inte lägga till medlem: {e}")
        return False


def search_members(search_term: str) -> List[Dict]:
    """Söker efter medlemmar på namn eller email."""
    with get_session() as session:
        search = f"%{search_term}%"
        members = session.query(Member).filter(
            or_(
                Member.first_name.ilike(search),
                Member.last_name.ilike(search),
                Member.email.ilike(search)
            )
        ).order_by(Member.last_name, Member.first_name).all()
        return [_member_to_dict(member) for member in members]


def get_member_by_id(member_id: int) -> Optional[Dict]:
    """Hämtar en medlem via ID."""
    with get_session() as session:
        member = session.query(Member).filter(Member.id == member_id).first()
        if member:
            return _member_to_dict(member)
        return None

