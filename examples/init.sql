PRAGMA foreign_keys = ON;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name  TEXT NOT NULL,
    last_name   TEXT NOT NULL,
    email       TEXT UNIQUE NOT NULL,
    phone       TEXT,
    city        TEXT,
    created_at  TEXT DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO customers (first_name, last_name, email, phone, city) VALUES
    ('Chinedu',  'Okafor',   'chinedu.okafor@example.com',    '08035550101', 'Zamfara'),
    ('Aisha',    'Bello',    'aisha.bello@example.com',       '08055550102', 'Kano'),
    ('Emeka',    'Nwosu',    'emeka.nwosu@example.com',       '08075550103', 'Enugu'),
    ('Mojirade', 'Adekanmi', 'mojirade.adekanmi@example.com', '08095550104', 'Lagos'),
    ('Ibrahim',  'Musa',     'ibrahim.musa@example.com',      '08105550105', 'Abuja');


CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id  INTEGER NOT NULL,
    order_date   TEXT NOT NULL,
    total_amount REAL NOT NULL,
    status       TEXT NOT NULL CHECK(status IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled')),
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id) ON DELETE CASCADE
);

INSERT INTO orders (customer_id, order_date, total_amount, status) VALUES
    (1, '2026-10-01', 149.99, 'Delivered'),
    (2, '2026-10-05',  45.50, 'Shipped'),
    (3, '2026-10-12', 299.00, 'Processing'),
    (1, '2026-10-18',  89.25, 'Delivered'),
    (4, '2026-10-22', 510.75, 'Pending');


CREATE TABLE students (
    student_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT UNIQUE NOT NULL,
    major           TEXT NOT NULL,
    gpa             REAL CHECK(gpa >= 0.0 AND gpa <= 5.0),
    enrollment_year INTEGER NOT NULL
);

INSERT INTO students (first_name, last_name, email, major, gpa, enrollment_year) VALUES
    ('Chioma', 'Okolie',     'chioma.okolie@university.edu',      'Computer Science',  4.85, 2023),
    ('Ade',    'Babatunde',   'ade.babatunde@university.edu',     'Data Science',      4.92, 2022),
    ('Funke',  'Yussuf',   'funke.yussuf@university.edu',     'Mathematics',       4.40, 2024),
    ('Tunde',  'Lawal',   'tunde.lawal@university.edu',     'Physics',           4.78, 2023),
    ('Nkechi', 'Okoro',   'nkechi.okoro@university.edu',  'Economics',         4.65, 2021);