from course import add_course, edit_course, delete_course, view_courses_menu

from student import add_student, edit_student, delete_student, view_students_menu 

from grades import grades_management_menu, performance_report_menu, export_report_menu

# ===============================================
# 2. MENU DEFINITIONS
# ===============================================

# -------------------------
# Course Management Menu
# -------------------------
def course_menu():
    while True:
        print("\n" + "="*50)
        print("\t\t\tCOURSE MANAGEMENT")
        print("="*50)
        print("[1] Add New Course")
        print("[2] Edit Course")
        print("[3] Delete Course")
        print("[4] View All Courses")
        print("[0] Back to Main Menu")
        print("="*50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_course()
        elif choice == "2":
            edit_course()
        elif choice == "3":
            delete_course()
        elif choice == "4":
            view_courses_menu()
        elif choice == "0":
            break
        else:
            print("[-] Invalid choice. Please enter a valid number.")

# -------------------------
# Student Management Menu 
# -------------------------
def student_menu():
    while True:
        print("\n" + "="*50)
        print("\t\t\tSTUDENT MANAGEMENT")
        print("="*50)
        print("[1] Add New Student")
        print("[2] Edit Student Details")
        print("[3] Delete Student")
        print("[4] View All Students")
        print("[0] Back to Main Menu")
        print("="*50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            edit_student()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            view_students_menu()
        elif choice == "0":
            break
        else:
            print("[-] Invalid choice. Please enter a valid number.")


# -------------------------
# Main Menu
# -------------------------
def main_menu():
    while True:
        print("\n" + "="*50)
        print("\t\t\tSTUDENT GRADING SYSTEM")
        print("="*50)
        print("[1] Course Management")       # Calls course_menu()
        print("[2] Student Management")      # Calls student_menu()
        print("[3] Grades Management")       # Calls grades_management_menu()
        print("[4] Performance Report")      # Calls performance_report_menu()
        print("[5] Export Report")           # Calls export_report_menu()
        print("[0] Exit")
        print("="*50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            course_menu()
        elif choice == "2":
            student_menu()
        elif choice == "3":
            grades_management_menu()
        elif choice == "4":
            performance_report_menu()
        elif choice == "5":
            export_report_menu()
        elif choice == "0":
            print("\nThank you for using the Student Grading System. Goodbye!")
            break
        else:
            print("[-] Invalid choice. Please enter a valid number.")

if __name__ == "__main__":

    main_menu()
