CREATE DATABASE LibraryManagement;
USE LibraryManagement;

CREATE TABLE Students(
    s_id INT PRIMARY KEY AUTO_INCREMENT,
    s_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    course VARCHAR(100) NOT NULL
);
CREATE TABLE Books(
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    available_copies INT NOT NULL CHECK(available_copies>=0)
);
CREATE TABLE Borrowed_books(
    borrow_id INT PRIMARY KEY AUTO_INCREMENT,
    s_id INT,
    book_id INT,
    issue_date DATE DEFAULT CURRENT_DATE,
    return_date DATE,
    fine DECIMAL(5,2) DEFAULT 0.00,
    FOREIGN KEY (s_id) REFERENCES Students(s_id) ON DELETE CASCADE,
    FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE

);
