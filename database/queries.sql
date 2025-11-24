-- SQL-queries för biblioteket
-- 15 olika queries för att testa olika SQL-funktioner

-- ============================================
-- GRUNDLÄGGANDE QUERIES
-- ============================================

-- 1. Visa alla böcker sorterade efter titel
SELECT id, title, author, category, available_copies, total_copies
FROM books
ORDER BY title;

-- 2. Visa alla medlemmar som blev medlemmar 2024
SELECT id, first_name, last_name, email, membership_date
FROM members
WHERE EXTRACT(YEAR FROM membership_date) = 2024
ORDER BY membership_date;

-- 3. Visa alla böcker i kategorin "Fiction"
SELECT id, title, author, publication_year, available_copies
FROM books
WHERE category = 'Fiction'
ORDER BY title;

-- 4. Visa alla aktiva lån (inte återlämnade än)
SELECT id, book_id, member_id, loan_date, due_date
FROM loans
WHERE return_date IS NULL
ORDER BY due_date;

-- 5. Visa böcker som har ISBN
SELECT id, title, author, isbn, category
FROM books
WHERE isbn IS NOT NULL
ORDER BY title;

-- ============================================
-- JOIN-QUERIES
-- ============================================

-- 6. Visa alla lån med boktitel och medlemsnamn
SELECT 
    l.id AS loan_id,
    b.title AS book_title,
    b.author AS book_author,
    m.first_name || ' ' || m.last_name AS member_name,
    l.loan_date,
    l.due_date,
    l.return_date
FROM loans l
JOIN books b ON l.book_id = b.id
JOIN members m ON l.member_id = m.id
ORDER BY l.loan_date DESC;

-- 7. Visa alla böcker en specifik medlem har lånat
-- (byt ut 1 mot det member_id du vill kolla)
SELECT 
    b.title,
    b.author,
    b.category,
    l.loan_date,
    l.due_date,
    l.return_date,
    CASE 
        WHEN l.return_date IS NULL THEN 'Aktivt lån'
        ELSE 'Återlämnad'
    END AS loan_status
FROM loans l
JOIN books b ON l.book_id = b.id
WHERE l.member_id = 1
ORDER BY l.loan_date DESC;

-- 8. Visa medlemmar som har lånat böcker av en specifik författare
-- (byt ut 'George Orwell' mot den författare du vill kolla)
SELECT DISTINCT
    m.id,
    m.first_name || ' ' || m.last_name AS member_name,
    m.email,
    b.author AS author_name
FROM members m
JOIN loans l ON m.id = l.member_id
JOIN books b ON l.book_id = b.id
WHERE b.author = 'George Orwell'
ORDER BY member_name;

-- 9. Visa böcker som aldrig har lånats
SELECT 
    b.id,
    b.title,
    b.author,
    b.category,
    b.available_copies,
    b.total_copies
FROM books b
LEFT JOIN loans l ON b.id = l.book_id
WHERE l.id IS NULL
ORDER BY b.title;

-- 10. Visa medlemmar som inte har några aktiva lån
SELECT 
    m.id,
    m.first_name || ' ' || m.last_name AS member_name,
    m.email,
    m.membership_date
FROM members m
LEFT JOIN loans l ON m.id = l.member_id AND l.return_date IS NULL
WHERE l.id IS NULL
ORDER BY member_name;

-- ============================================
-- AGGRGERING OCH ANALYS
-- ============================================

-- 11. Räkna antal böcker per kategori
SELECT 
    category,
    COUNT(*) AS total_books,
    SUM(total_copies) AS total_copies,
    SUM(available_copies) AS available_copies
FROM books
WHERE category IS NOT NULL
GROUP BY category
ORDER BY total_books DESC;

-- 12. Hitta de 5 mest populära böckerna (mest lånade)
SELECT 
    b.id,
    b.title,
    b.author,
    COUNT(l.id) AS total_loans
FROM books b
JOIN loans l ON b.id = l.book_id
GROUP BY b.id, b.title, b.author
ORDER BY total_loans DESC
LIMIT 5;

-- 13. Visa medlemmar med flest antal lån
SELECT 
    m.id,
    m.first_name || ' ' || m.last_name AS member_name,
    m.email,
    COUNT(l.id) AS total_loans
FROM members m
JOIN loans l ON m.id = l.member_id
GROUP BY m.id, m.first_name, m.last_name, m.email
ORDER BY total_loans DESC;

-- 14. Beräkna genomsnittligt antal dagar mellan lån och återlämning
SELECT 
    AVG(return_date - loan_date) AS avg_days_borrowed
FROM loans
WHERE return_date IS NOT NULL;

-- 15. Visa försenade lån (förfallodatum passerat men inte återlämnade)
SELECT 
    l.id,
    b.title AS book_title,
    m.first_name || ' ' || m.last_name AS member_name,
    m.email,
    l.loan_date,
    l.due_date,
    CURRENT_DATE - l.due_date AS days_overdue
FROM loans l
JOIN books b ON l.book_id = b.id
JOIN members m ON l.member_id = m.id
WHERE l.return_date IS NULL 
  AND l.due_date < CURRENT_DATE
ORDER BY days_overdue DESC;
