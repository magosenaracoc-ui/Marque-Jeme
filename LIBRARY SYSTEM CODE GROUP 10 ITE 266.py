import re
from datetime import datetime, timedelta

print("Welcome to PHINMA COC Library System")


#Pre-added subject books
library = [
    {"book_no": "B001", "title": "Python Programming Basics", "author": "John Reyes",
     "category": "Information Technology", "copies": 5, "borrowed": 0, "borrowers": []},
    {"book_no": "B002", "title": "Data Structures and Algorithms", "author": "Maria Santos",
     "category": "Computer Science", "copies": 3, "borrowed": 0, "borrowers": []},
    {"book_no": "B003", "title": "Networking Fundamentals", "author": "A. Dela Cruz",
     "category": "Information Technology", "copies": 4, "borrowed": 0, "borrowers": []},
    {"book_no": "B004", "title": "Database Management Systems", "author": "R. Villanueva",
     "category": "Information Technology", "copies": 2, "borrowed": 0, "borrowers": []},
    {"book_no": "B005", "title": "Introduction to Computing", "author": "L. Fernandez",
     "category": "Computer Science", "copies": 6, "borrowed": 0, "borrowers": []}]

#STUDENT FACULTY AND DATA
student_ids, student_names, student_courses = [], [], []
faculty_ids, faculty_names, faculty_departments = [], [], []

departments = [
    "Management and Accountancy", "Engineering and Architecture", "Education",
    "Criminology and Criminal Justice", "Information Technology",
    "Allied Health Sciences", "Graduate School"]

#FUNCTIONS OF ADD BOOKS
def add_book():
    print("\n--- ADD BOOK ---")
    book_no = input("Book No.: ")
    title = input("Book Name: ")
    author = input("Author: ")
    category = input("Category: ")

    while True:
        try:
            copies = int(input("No. of Copies: "))
            if copies < 1:
                print("Please enter at least 1 copy.")
            else:
                break
        except ValueError:
            print("Please enter a valid number.")

    book = {"book_no": book_no, "title": title, "author": author, "category": category,
            "copies": copies, "borrowed": 0, "borrowers": []}
    library.append(book)
    print(f"\nBook '{title}' added successfully!\n")

#BOOK VIEWING
def view_books():
    if not library:
        print("\nNo books in the library yet.")
        return
    print("\n================= Library Collection =================")
    print(f"{'Book No.':<10} {'Book Name':<28} {'Author':<20} {'Category':<20} "
          f"{'Copies':<8} {'Borrowed':<10} {'Available':<10}")
    print("-" * 110)
    for book in library:
        available = book["copies"] - book["borrowed"]
        print(f"{book['book_no']:<10} {book['title']:<28} {book['author']:<20} {book['category']:<20} "
              f"{book['copies']:<8} {book['borrowed']:<10} {available:<10}")
    print("=" * 110)

#BOOK BORROWING
def borrow_book():
    if not library:
        print("\nNo books available to borrow.")
        return

    print("\nWho is borrowing the book?")
    print("1. Student")
    print("2. Faculty")
    choice_type = input("Select 1 or 2: ")

    if choice_type == "1":
        sid = input("Enter Student ID: ")
        if sid not in student_ids:
            print("Student not found! Add the student first.")
            return
        borrower_name = student_names[student_ids.index(sid)]
        borrower_id = sid
        borrower_course_dept = student_courses[student_ids.index(sid)]
        borrower_type = "Student"
    elif choice_type == "2":
        fid = input("Enter Faculty ID: ")
        if fid not in faculty_ids:
            print("Faculty not found! Add the faculty first.")
            return
        borrower_name = faculty_names[faculty_ids.index(fid)]
        borrower_id = fid
        borrower_course_dept = faculty_departments[faculty_ids.index(fid)]
        borrower_type = "Faculty"
    else:
        print("Invalid choice!")
        return

    while True:
        view_books()
        book_no = input("\nEnter Book No. to borrow: ")
        book = next((b for b in library if b["book_no"] == book_no), None)
        if not book:
            print("Book not found! Try again.")
            continue

        available_copies = book["copies"] - book["borrowed"]
        if available_copies == 0:
            print("No available copies!")
            continue

        while True:
            try:
                num_copies = int(input(f"How many copies do you want to borrow? (Available: {available_copies}): "))
                if num_copies < 1:
                    print("You must borrow at least 1 copy.")
                elif num_copies > available_copies:
                    print(f"You cannot borrow more than {available_copies} copies.")
                else:
                    break
            except ValueError:
                print("Invalid input! Enter a number.")

        due_date = datetime.now() + timedelta(days=7) #7 DAYS DUE DATE
        due_str = due_date.strftime("%Y-%m-%d")

        #BORROWING SUMMARRY
        print("\n======== BORROWING SUMMARY ========")
        print(f"STUDENT/FACULTY NAME: {borrower_name}")
        print(f"STUDENT/FACULTY ID: {borrower_id}")
        print(f"COURSE/DEPARTMENT: {borrower_course_dept}")
        print(f"Book No.: {book['book_no']}")
        print(f"Book Name: {book['title']}")
        print(f"Copies: {num_copies}")
        print(f"Due Date: {due_str}")
        print("===================================")

        confirm = input("\nAre you sure this is the book you want to borrow? (YES/NO): ").strip().lower()
        if confirm == "yes":
            book["borrowed"] += num_copies
            for _ in range(num_copies):
                book["borrowers"].append({"name": borrower_name, "type": borrower_type, "due": due_str})
            print(f"\n{borrower_name} successfully borrowed {num_copies} copy/copies of '{book['title']}'!\n")
            break
        else:
            print("\nLet's choose the book again.")
            

#REURTING BOOK
def return_book():
    name = input("\nEnter your name: ")
    found = False
    for book in library:
        for borrower in book["borrowers"]:
            if borrower["name"] == name:
                book["borrowers"].remove(borrower)
                book["borrowed"] -= 1
                print(f"{name} returned '{book['title']}'.")
                found = True
                break
    if not found:
        print("No borrowed books found for that name.")

#ADD STUDENT FUNCTION
def add_student():
    # Student ID
    sid = input("Enter Student ID: ")
    if not sid.isdigit() or len(sid) != 6:
        print("Invalid ID! Student ID must be exactly 6 digits.")
        return
    if sid in student_ids:
        print("This Student ID already exists!")
        return

    #student Name
    name = input("Student Name: ")
    if not re.fullmatch(r"[A-Za-z ]+", name.strip()):
        print("Invalid Name! Only letters and spaces are allowed.")
        return

    #Course
    course = input("Course: ")
    if not re.fullmatch(r"[A-Za-z ]+", course.strip()):
        print("Invalid Course! Only letters and spaces are allowed.")
        return

    student_ids.append(sid)
    student_names.append(name)
    student_courses.append(course)
    print(f"Student '{name}' with ID {sid} added successfully!")

#ADD FACULTY FUNCTIONS
def add_faculty():
    #Faculty ID
    fid = input("Faculty ID: ")
    if not fid.isdigit() or len(fid) != 6:
        print("Invalid ID! Faculty ID must be exactly 6 digits.")
        return
    if fid in faculty_ids:
        print("This Faculty ID already exists!")
        return

    #Faculty Name
    name = input("Faculty Name: ")
    if not re.fullmatch(r"[A-Za-z ]+", name.strip()):
        print("Invalid Name! Only letters and spaces are allowed.")
        return

    #Department
    dept = input("What department are you? ")
    if not re.fullmatch(r"[A-Za-z ]+", dept.strip()):
        print("Invalid Department! Only letters and spaces are allowed.")
        return

    faculty_ids.append(fid)
    faculty_names.append(name)
    faculty_departments.append(dept)
    print(f"\nFaculty '{name}' added successfully to the {dept} department!")


#MAIN MENU LOOP
while True:
    print("\n====== Library System Menu ======")
    print("1. Add Book")
    print("2. View Books")
    print("3. Add Student")
    print("4. Add Faculty")
    print("5. Borrow Book")
    print("6. Return Book")
    print("7. Exit")

    choice = input("Select a number (1–7): ")

    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()
    elif choice == "3":
        add_student()
    elif choice == "4":
        add_faculty()
    elif choice == "5":
        borrow_book()
    elif choice == "6":
        return_book()
    elif choice == "7":
        print("\nExiting PHINMA COC Library System. Goodbye!\n")
        break
    else:
        print("Invalid choice. Please select 1–7.")