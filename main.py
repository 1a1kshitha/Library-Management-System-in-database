import sqlite3

def init_db():
    conn=sqlite3.connect("library.db")
    cursor=conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Students(
                        s_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VTEXT NOT NULL,
                        email TEXT NOT NULL,
                        course TEXT NOT NULL) ''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books(
                     book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     author TEXT NOT NULL,
                     category TEXT,
                     available_copies INTEGER NOT NULL CHECK (available_copies>=0))''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Borrowed_books(
                        borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        s_id INTEGER,
                        book_id INTEGER,
                        issue_date TEXT DEFAULT CURRERNT_DATE,
                        return_date TEXT,
                        fine REAL DEFAULT 0.00,
                        FOREIGN KEY (s_id) REFERENCES Students(s_id) ON DELETE CASCADE,
                        FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE)''' )
    
    
    conn.commit()
    conn.close()


def add_student():
    name=input("Enter student name:")
    email=input("Enter student email:")
    course=input("Enter course id:")

    conn=sqlite3.connect("library.db")
    cursor=conn.cursor()
    try:
        cursor.execute("INSERT INTO Students(name,email,course) VALUES (?,?,?)",(name,email,course))
        conn.commit()
        print("Student registered Successfully!")
    except sqlite3.IntegrityError:
        print("Error:Email was already taken!")
    conn.close()

def view_student():
    conn=sqlite3.connect("library.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Students")
    Students=cursor.fetchall()
    conn.close()



    if Students:
        print("\nRegistered Students:")
        print("{:<5}{:<20}{:<25}{:<15}".format("id","name","email","course"))
        print("-"*70)
        for student in Students:
            print("{:<5}{:<20}{:<25}{:<15}".format(student[0],student[1],student[2],student[3]))
    else:
        print("No Student Registered Yet!")


def issue_book():
    s_id=input("Enter student id:")
    book_id=input("Enter book id:")

    conn=sqlite3.connect("library.db")
    cursor=conn.cursor()
    cursor.execute("SELECT available_copies FROM Books WHERE book_id=?",(book_id,))
    book=cursor.fetchone()


    if book and book[0]>0:
        cursor.execute("INSERT Students Borrowed_books(s_id,book_id)VALUES (?,?,?)",(s_id,book_id))
        cursor.execute("UPDATE Books SET available_copies=available_copies-1 WHERE book_id=?",(book_id,))
        conn.commit()
        print("Book issued Successfully!")

    else:
        print("Error:Book is not available.")
    conn.close()


def generate_report():
    conn=sqlite3.connect("library.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Borrowed_books")
    Borrowed_books=cursor.fetchall()
    conn.close()

    html="<html><head><title><Library Report</title></head><body>"
    html+="<h2>Borrowed Books Repport</h2>"
    html+="<table border='1'><tr><th>Borrow ID</th><th>Student Id</th><th>Book ID</th><th>Issue date</th><th>Return date</th><th>Fine</th></tr>"
    

    for book in Borrowed_books:
        html+=f"<tr><td>{book[0]}</td><td>{book[1]}</td><td>{book[2]}</td><td>{book[3]}</td><td>{book[4]}</td><td>{book[5]}</td></tr>"
    html+="</table></body></html>"

    with open("templates/report.html","w") as file:
        file.write(html)
    print("Report generated successfully!")



def main():
    init_db()
    while True:
        print("1.Add student:")
        print("2.View student:")
        print("3.Issue Book:")
        print("4.Report Student:")
        print("5.Exit")
        choice=input("Enter any number:")

        if choice=="1":
            add_student()
        elif choice=="2":
            view_student()
        elif choice=="3":
            issue_book()
        elif  choice=="4":
            generate_report()
        elif choice=="5":
            print("Exiting..")
            break
        else:
            print("Invalid choice.Try again")

if __name__=="__main__":
    main()






