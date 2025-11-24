"""Huvudprogram för bibliotekssystemet."""

from .book_manager import (
    get_all_books, search_books, add_book, get_available_books, get_book_by_id
)
from .member_manager import (
    get_all_members, add_member, search_members, get_member_by_id
)
from .loan_manager import (
    register_loan, register_return, get_active_loans, get_overdue_loans
)


def show_menu():
    """Visar huvudmenyn."""
    print("\n" + "="*50)
    print("    BIBLIOTEKSSYSTEM")
    print("="*50)
    print("1. Bokhantering")
    print("2. Medlemshantering")
    print("3. Lånehantering")
    print("4. Statistik & Rapporter")
    print("0. Avsluta")
    print("-"*50)


def book_menu():
    """Hanterar bokhantering."""
    while True:
        print("\n--- BOKHANTERING ---")
        print("1. Visa alla böcker")
        print("2. Sök böcker")
        print("3. Lägg till ny bok")
        print("4. Visa tillgängliga böcker")
        print("0. Tillbaka till huvudmeny")
        
        choice = input("Välj alternativ: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            books = get_all_books()
            print(f"\nTotalt antal böcker: {len(books)}")
            for book in books:
                print(f"  [{book['id']}] {book['title']} av {book['author']} "
                      f"({book['available_copies']}/{book['total_copies']} tillgängliga)")
        elif choice == "2":
            search_term = input("Sökterm (titel eller författare): ").strip()
            books = search_books(search_term)
            if books:
                print(f"\nHittade {len(books)} bok(er):")
                for book in books:
                    print(f"  [{book['id']}] {book['title']} av {book['author']}")
            else:
                print("Inga böcker hittades.")
        elif choice == "3":
            title = input("Titel: ").strip()
            author = input("Författare: ").strip()
            isbn = input("ISBN (valfritt): ").strip() or None
            year = input("Utgivningsår (valfritt): ").strip()
            year = int(year) if year else None
            category = input("Kategori (valfritt): ").strip() or None
            copies = input("Antal exemplar (standard 1): ").strip()
            copies = int(copies) if copies else 1
            
            if add_book(title, author, isbn, year, category, copies):
                print("Bok tillagd!")
            else:
                print("Kunde inte lägga till bok.")
        elif choice == "4":
            books = get_available_books()
            print(f"\nTillgängliga böcker: {len(books)}")
            for book in books:
                print(f"  [{book['id']}] {book['title']} av {book['author']} "
                      f"({book['available_copies']} tillgängliga)")
        else:
            print("Ogiltigt val. Försök igen.")


def member_menu():
    """Hanterar medlemshantering."""
    while True:
        print("\n--- MEDLEMSHANTERING ---")
        print("1. Visa alla medlemmar")
        print("2. Lägg till ny medlem")
        print("3. Sök medlemmar")
        print("0. Tillbaka till huvudmeny")
        
        choice = input("Välj alternativ: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            members = get_all_members()
            print(f"\nTotalt antal medlemmar: {len(members)}")
            for member in members:
                print(f"  [{member['id']}] {member['first_name']} {member['last_name']} "
                      f"({member['email']})")
        elif choice == "2":
            first_name = input("Förnamn: ").strip()
            last_name = input("Efternamn: ").strip()
            email = input("Email: ").strip()
            phone = input("Telefon (valfritt): ").strip() or None
            
            if add_member(first_name, last_name, email, phone):
                print("Medlem tillagd!")
            else:
                print("Kunde inte lägga till medlem.")
        elif choice == "3":
            search_term = input("Sökterm (namn eller email): ").strip()
            members = search_members(search_term)
            if members:
                print(f"\nHittade {len(members)} medlem(mar):")
                for member in members:
                    print(f"  [{member['id']}] {member['first_name']} {member['last_name']} "
                          f"({member['email']})")
            else:
                print("Inga medlemmar hittades.")
        else:
            print("Ogiltigt val. Försök igen.")


def loan_menu():
    """Hanterar lånehantering."""
    while True:
        print("\n--- LÅNEHANTERING ---")
        print("1. Registrera nytt lån")
        print("2. Registrera återlämning")
        print("3. Visa aktiva lån")
        print("4. Visa försenade lån")
        print("0. Tillbaka till huvudmeny")
        
        choice = input("Välj alternativ: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            try:
                book_id = int(input("Bok-ID: ").strip())
                member_id = int(input("Medlems-ID: ").strip())
                days = input("Låneperiod i dagar (standard 14): ").strip()
                days = int(days) if days else 14
                
                if register_loan(book_id, member_id, days):
                    print("Lån registrerat!")
                else:
                    print("Kunde inte registrera lån.")
            except ValueError:
                print("Fel: Ogiltig inmatning. Ange siffror.")
        elif choice == "2":
            try:
                loan_id = int(input("Lån-ID: ").strip())
                if register_return(loan_id):
                    print("Återlämning registrerad!")
                else:
                    print("Kunde inte registrera återlämning.")
            except ValueError:
                print("Fel: Ogiltig inmatning. Ange ett nummer.")
        elif choice == "3":
            loans = get_active_loans()
            print(f"\nAktiva lån: {len(loans)}")
            for loan in loans:
                print(f"  [{loan['id']}] {loan['book_title']} - "
                      f"{loan['member_name']} (Förfaller: {loan['due_date']})")
        elif choice == "4":
            loans = get_overdue_loans()
            print(f"\nFörsenade lån: {len(loans)}")
            for loan in loans:
                print(f"  [{loan['id']}] {loan['book_title']} - "
                      f"{loan['member_name']} ({loan['days_overdue']} dagar försenad)")
        else:
            print("Ogiltigt val. Försök igen.")


def statistics_menu():
    """Visar statistik och rapporter."""
    from sqlalchemy import func, and_
    from datetime import date
    from .database import get_session
    from .models import Book, Member, Loan
    
    print("\n--- STATISTIK & RAPPORTER ---")
    
    with get_session() as session:
        total_books = session.query(Book).count()
        total_members = session.query(Member).count()
        active_loans = session.query(Loan).filter(
            Loan.return_date.is_(None)
        ).count()
        
        today = date.today()
        overdue_loans = session.query(Loan).filter(
            and_(
                Loan.return_date.is_(None),
                Loan.due_date < today
            )
        ).count()
        
        popular_books = session.query(
            Book.title,
            func.count(Loan.id).label('loan_count')
        ).join(Loan).group_by(Book.id, Book.title).order_by(
            func.count(Loan.id).desc()
        ).limit(5).all()
        
        top_member = session.query(
            Member.first_name,
            Member.last_name,
            func.count(Loan.id).label('loan_count')
        ).join(Loan).group_by(
            Member.id, Member.first_name, Member.last_name
        ).order_by(func.count(Loan.id).desc()).first()
    
    print(f"\nBiblioteksöversikt:")
    print(f"  Totalt antal böcker: {total_books}")
    print(f"  Totalt antal medlemmar: {total_members}")
    print(f"  Aktiva lån: {active_loans}")
    print(f"  Försenade lån: {overdue_loans}")
    
    print(f"\nTop 5 Mest Lånade Böcker:")
    for i, (title, count) in enumerate(popular_books, 1):
        print(f"  {i}. {title} ({count} lån)")
    
    if top_member:
        name = f"{top_member.first_name} {top_member.last_name}"
        print(f"\nMedlem med Flest Lån:")
        print(f"  {name} ({top_member.loan_count} lån)")


def main():
    """Huvudprogramloop."""
    print("Välkommen till Bibliotekssystemet!")
    
    while True:
        show_menu()
        choice = input("Välj alternativ (0-4): ").strip()
        
        if choice == "0":
            print("Hej då!")
            break
        elif choice == "1":
            book_menu()
        elif choice == "2":
            member_menu()
        elif choice == "3":
            loan_menu()
        elif choice == "4":
            statistics_menu()
        else:
            print("Ogiltigt val. Försök igen.")


if __name__ == "__main__":
    main()
