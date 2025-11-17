-- Library Management System Test Data
-- Insert test data for testing the library system

-- Insert Books (minst 15 böcker)
INSERT INTO books (title, author, isbn, publication_year, category, total_copies, available_copies) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 1925, 'Fiction', 3, 1),
('1984', 'George Orwell', '978-0-452-28423-4', 1949, 'Fiction', 2, 0),
('To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 1960, 'Fiction', 4, 2),
('Pride and Prejudice', 'Jane Austen', '978-0-14-143951-8', 1813, 'Fiction', 2, 1),
('The Catcher in the Rye', 'J.D. Salinger', '978-0-316-76948-0', 1951, 'Fiction', 3, 2),
('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', '978-0-06-231609-7', 2011, 'History', 2, 1),
('The Selfish Gene', 'Richard Dawkins', '978-0-19-286092-7', 1976, 'Science', 2, 2),
('A Brief History of Time', 'Stephen Hawking', '978-0-553-10953-5', 1988, 'Science', 3, 1),
('The Art of War', 'Sun Tzu', '978-0-486-42557-4', -500, 'Philosophy', 2, 1),
('Meditations', 'Marcus Aurelius', '978-0-14-044933-4', 180, 'Philosophy', 2, 2),
('Clean Code', 'Robert C. Martin', '978-0-13-235088-4', 2008, 'Technology', 3, 1),
('Design Patterns', 'Gang of Four', '978-0-201-63361-7', 1994, 'Technology', 2, 0),
('The Pragmatic Programmer', 'Andrew Hunt', '978-0-201-61622-4', 1999, 'Technology', 2, 1),
('Introduction to Algorithms', 'Thomas H. Cormen', '978-0-262-03384-8', 2009, 'Technology', 2, 1),
('The Lord of the Rings', 'J.R.R. Tolkien', '978-0-544-00035-4', 1954, 'Fantasy', 4, 2);

-- Insert Members (minst 10 medlemmar)
INSERT INTO members (first_name, last_name, email, phone, membership_date) VALUES
('Anna', 'Andersson', 'anna.andersson@email.com', '070-123-4567', '2023-01-15'),
('Erik', 'Eriksson', 'erik.eriksson@email.com', '070-234-5678', '2023-02-20'),
('Maria', 'Johansson', 'maria.johansson@email.com', '070-345-6789', '2023-03-10'),
('Johan', 'Nilsson', 'johan.nilsson@email.com', '070-456-7890', '2024-01-05'),
('Emma', 'Svensson', 'emma.svensson@email.com', '070-567-8901', '2024-02-12'),
('Lars', 'Gustafsson', 'lars.gustafsson@email.com', '070-678-9012', '2024-03-18'),
('Sara', 'Larsson', 'sara.larsson@email.com', '070-789-0123', '2024-04-22'),
('Anders', 'Karlsson', 'anders.karlsson@email.com', '070-890-1234', '2024-05-30'),
('Lisa', 'Olsson', 'lisa.olsson@email.com', '070-901-2345', '2024-06-15'),
('Peter', 'Lindberg', 'peter.lindberg@email.com', '070-012-3456', '2024-07-20');

-- Insert Loans (minst 20 lån - både aktiva och återlämnade)
-- Aktiva lån (inte återlämnade)
INSERT INTO loans (book_id, member_id, loan_date, due_date) VALUES
(1, 1, '2024-11-01', '2024-11-15'),
(2, 2, '2024-11-05', '2024-11-19'),
(3, 3, '2024-11-10', '2024-11-24'),
(5, 4, '2024-11-08', '2024-11-22'),
(8, 5, '2024-11-12', '2024-11-26'),
(11, 6, '2024-11-15', '2024-11-29'),
(13, 7, '2024-11-18', '2024-12-02');

-- Försenade lån (due_date har passerat men inte återlämnade)
INSERT INTO loans (book_id, member_id, loan_date, due_date) VALUES
(2, 8, '2024-10-15', '2024-10-29'),
(12, 9, '2024-10-20', '2024-11-03'),
(1, 10, '2024-10-25', '2024-11-08');

-- Återlämnade lån
INSERT INTO loans (book_id, member_id, loan_date, due_date, return_date) VALUES
(4, 1, '2024-09-01', '2024-09-15', '2024-09-12'),
(6, 2, '2024-09-05', '2024-09-19', '2024-09-18'),
(7, 3, '2024-09-10', '2024-09-24', '2024-09-22'),
(9, 4, '2024-09-15', '2024-09-29', '2024-09-27'),
(10, 5, '2024-09-20', '2024-10-04', '2024-10-02'),
(14, 6, '2024-09-25', '2024-10-09', '2024-10-07'),
(15, 7, '2024-10-01', '2024-10-15', '2024-10-13'),
(3, 8, '2024-10-05', '2024-10-19', '2024-10-17'),
(5, 9, '2024-10-10', '2024-10-24', '2024-10-22'),
(8, 10, '2024-10-15', '2024-10-29', '2024-10-27');

