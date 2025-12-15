from course import add_course, edit_course, delete_course, view_courses_menu
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
# Main Menu
# -------------------------
def main_menu():
    while True:
        print("\n" + "="*50)
        print("\t\t\tSTUDENT GRADING SYSTEM")
        print("="*50)
        print("[1] Course Management")
        print("[2] Student Management")
        print("[3] Grades Management")
        print("[4] Performance Report")
        print("[5] Export Report")
        print("[0] Exit")
        print("="*50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            course_menu()
        elif choice == "2":
            student_menu()
        elif choice == "0":
            print("\nThank you for using the Student Grading System. Goodbye!")
            break
        else:
            print("[-] Invalid choice. Please enter a valid number.")

if __name__ == "__main__":
    main_menu()
