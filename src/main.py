"""
Library Management System - Main Application
Kurs: Databasteknik PIA25

A console-based library management system for managing books, members, and loans.
"""

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
    """Display the main menu."""
    print("\n" + "="*50)
    print("    LIBRARY MANAGEMENT SYSTEM")
    print("="*50)
    print("1. Book Management")
    print("2. Member Management")
    print("3. Loan Management")
    print("4. Statistics & Reports")
    print("0. Exit")
    print("-"*50)


def book_menu():
    """Handle book management operations."""
    while True:
        print("\n--- BOOK MANAGEMENT ---")
        print("1. View all books")
        print("2. Search books")
        print("3. Add new book")
        print("4. View available books")
        print("0. Back to main menu")
        
        choice = input("Choose option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            books = get_all_books()
            print(f"\nTotal books: {len(books)}")
            for book in books:
                print(f"  [{book['id']}] {book['title']} by {book['author']} "
                      f"({book['available_copies']}/{book['total_copies']} available)")
        elif choice == "2":
            search_term = input("Enter search term (title or author): ").strip()
            books = search_books(search_term)
            if books:
                print(f"\nFound {len(books)} book(s):")
                for book in books:
                    print(f"  [{book['id']}] {book['title']} by {book['author']}")
            else:
                print("No books found.")
        elif choice == "3":
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            isbn = input("ISBN (optional): ").strip() or None
            year = input("Publication year (optional): ").strip()
            year = int(year) if year else None
            category = input("Category (optional): ").strip() or None
            copies = input("Total copies (default 1): ").strip()
            copies = int(copies) if copies else 1
            
            if add_book(title, author, isbn, year, category, copies):
                print("Book added successfully!")
            else:
                print("Failed to add book.")
        elif choice == "4":
            books = get_available_books()
            print(f"\nAvailable books: {len(books)}")
            for book in books:
                print(f"  [{book['id']}] {book['title']} by {book['author']} "
                      f"({book['available_copies']} available)")
        else:
            print("Invalid choice. Try again.")


def member_menu():
    """Handle member management operations."""
    while True:
        print("\n--- MEMBER MANAGEMENT ---")
        print("1. View all members")
        print("2. Add new member")
        print("3. Search members")
        print("0. Back to main menu")
        
        choice = input("Choose option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            members = get_all_members()
            print(f"\nTotal members: {len(members)}")
            for member in members:
                print(f"  [{member['id']}] {member['first_name']} {member['last_name']} "
                      f"({member['email']})")
        elif choice == "2":
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone (optional): ").strip() or None
            
            if add_member(first_name, last_name, email, phone):
                print("Member added successfully!")
            else:
                print("Failed to add member.")
        elif choice == "3":
            search_term = input("Enter search term (name or email): ").strip()
            members = search_members(search_term)
            if members:
                print(f"\nFound {len(members)} member(s):")
                for member in members:
                    print(f"  [{member['id']}] {member['first_name']} {member['last_name']} "
                          f"({member['email']})")
            else:
                print("No members found.")
        else:
            print("Invalid choice. Try again.")


def loan_menu():
    """Handle loan management operations."""
    while True:
        print("\n--- LOAN MANAGEMENT ---")
        print("1. Register new loan")
        print("2. Register return")
        print("3. View active loans")
        print("4. View overdue loans")
        print("0. Back to main menu")
        
        choice = input("Choose option: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            try:
                book_id = int(input("Book ID: ").strip())
                member_id = int(input("Member ID: ").strip())
                days = input("Loan period in days (default 14): ").strip()
                days = int(days) if days else 14
                
                if register_loan(book_id, member_id, days):
                    print("Loan registered successfully!")
                else:
                    print("Failed to register loan.")
            except ValueError:
                print("Error: Invalid input. Please enter numbers.")
        elif choice == "2":
            try:
                loan_id = int(input("Loan ID: ").strip())
                if register_return(loan_id):
                    print("Return registered successfully!")
                else:
                    print("Failed to register return.")
            except ValueError:
                print("Error: Invalid input. Please enter a number.")
        elif choice == "3":
            loans = get_active_loans()
            print(f"\nActive loans: {len(loans)}")
            for loan in loans:
                print(f"  [{loan['id']}] {loan['book_title']} - "
                      f"{loan['member_name']} (Due: {loan['due_date']})")
        elif choice == "4":
            loans = get_overdue_loans()
            print(f"\nOverdue loans: {len(loans)}")
            for loan in loans:
                print(f"  [{loan['id']}] {loan['book_title']} - "
                      f"{loan['member_name']} ({loan['days_overdue']} days overdue)")
        else:
            print("Invalid choice. Try again.")


def statistics_menu():
    """Display statistics and reports."""
    from .database import get_connection
    
    print("\n--- STATISTICS & REPORTS ---")
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Total books
            cur.execute("SELECT COUNT(*) FROM books")
            total_books = cur.fetchone()[0]
            
            # Total members
            cur.execute("SELECT COUNT(*) FROM members")
            total_members = cur.fetchone()[0]
            
            # Active loans
            cur.execute("SELECT COUNT(*) FROM loans WHERE return_date IS NULL")
            active_loans = cur.fetchone()[0]
            
            # Overdue loans
            cur.execute("""
                SELECT COUNT(*) FROM loans 
                WHERE return_date IS NULL AND due_date < CURRENT_DATE
            """)
            overdue_loans = cur.fetchone()[0]
            
            # Most borrowed books
            cur.execute("""
                SELECT b.title, COUNT(l.id) AS loan_count
                FROM books b
                JOIN loans l ON b.id = l.book_id
                GROUP BY b.id, b.title
                ORDER BY loan_count DESC
                LIMIT 5
            """)
            popular_books = cur.fetchall()
            
            # Member with most loans
            cur.execute("""
                SELECT m.first_name || ' ' || m.last_name AS name, COUNT(l.id) AS loan_count
                FROM members m
                JOIN loans l ON m.id = l.member_id
                GROUP BY m.id, m.first_name, m.last_name
                ORDER BY loan_count DESC
                LIMIT 1
            """)
            top_member = cur.fetchone()
    
    print(f"\nLibrary Overview:")
    print(f"  Total books: {total_books}")
    print(f"  Total members: {total_members}")
    print(f"  Active loans: {active_loans}")
    print(f"  Overdue loans: {overdue_loans}")
    
    print(f"\nTop 5 Most Borrowed Books:")
    for i, (title, count) in enumerate(popular_books, 1):
        print(f"  {i}. {title} ({count} loans)")
    
    if top_member:
        print(f"\nMember with Most Loans:")
        print(f"  {top_member[0]} ({top_member[1]} loans)")


def main():
    """Main application loop."""
    print("Welcome to the Library Management System!")
    
    while True:
        show_menu()
        choice = input("Choose option (0-4): ").strip()
        
        if choice == "0":
            print("Goodbye!")
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
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()

