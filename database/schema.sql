-- Library Management System Database Schema
-- PostgreSQL Database Schema for Library System
-- Kurs: Databasteknik PIA25

-- Skapa databas (kör detta först i psql som superuser)
-- CREATE DATABASE library_db;

-- Byt anslutning till library_db innan du kör resterande script
-- I pgAdmin: högerklicka på library_db och välj "Query Tool"
-- I psql: \connect library_db

-- Säkerställ ren miljö
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;
SET search_path TO public;

-- Tabell: Books (Böcker)
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    publication_year INTEGER,
    category VARCHAR(100),
    total_copies INTEGER DEFAULT 1 CHECK (total_copies > 0),
    available_copies INTEGER DEFAULT 1 CHECK (available_copies >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Säkerställ att available_copies inte överstiger total_copies
    CHECK (available_copies <= total_copies)
);

-- Tabell: Members (Medlemmar)
CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    membership_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabell: Loans (Lån)
CREATE TABLE loans (
    id SERIAL PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
    member_id INTEGER NOT NULL REFERENCES members(id) ON DELETE CASCADE,
    loan_date DATE DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Säkerställ att due_date är efter loan_date
    CHECK (due_date >= loan_date),
    -- Säkerställ att return_date är efter loan_date om den är satt
    CHECK (return_date IS NULL OR return_date >= loan_date)
);

-- Index för prestanda
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_author ON books(author);
CREATE INDEX idx_books_category ON books(category);
CREATE INDEX idx_books_isbn ON books(isbn);
CREATE INDEX idx_members_email ON members(email);
CREATE INDEX idx_members_name ON members(last_name, first_name);
CREATE INDEX idx_loans_book_id ON loans(book_id);
CREATE INDEX idx_loans_member_id ON loans(member_id);
CREATE INDEX idx_loans_loan_date ON loans(loan_date);
CREATE INDEX idx_loans_due_date ON loans(due_date);
CREATE INDEX idx_loans_return_date ON loans(return_date);

-- Kommentarer för dokumentation
COMMENT ON TABLE books IS 'Stores information about books in the library';
COMMENT ON TABLE members IS 'Stores information about library members';
COMMENT ON TABLE loans IS 'Stores information about book loans';

