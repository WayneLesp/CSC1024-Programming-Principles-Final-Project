from helper import read_file, write_file, append_file
import time

STUDENTS_FILE = "students.txt"

# -------------------------
# Student Management
# -------------------------

# For view workflow
# -----------------------------------
"""With returning to student menu message"""


def view_students_menu():
    """Display all registered students and return the list."""
    students = read_file(STUDENTS_FILE)

    if not students:
        print("\n[-] No students registered yet.")
        return []

    # Sort students by their numeric Student ID part (e.g., S001)
    students = sorted(students, key=lambda x: int(x.split(",")[0][1:]))

    print("\n--- Registered Students ---")
    print("-" * 80)
    print("{:<10} | {:<30} | {:<35}".format("Student ID", "Name", "Email"))
    print("-" * 80)
    for s in students:
        try:
            student_id, name, email = s.split(",", 2)
            # Print the student details in a formatted table row
            print("{:<10} | {:<30} | {:<35}".format(student_id, name, email))
        except ValueError:
            print(f"[!] Invalid line in file: {s}")

    input("\nPress ENTER to return to Student Menu...")
    return students


# view workflow (for edit/delete)
# -----------------------------------
def view_students_list():
    """View students for Edit/Delete without returning to student menu message."""
    students = read_file(STUDENTS_FILE)
    if not students:
        print("\n[-] No students registered yet.")
        return []

    students = sorted(students, key=lambda x: int(x.split(",")[0][1:]))
    print("\n--- Registered Students ---")
    print("-" * 80)
    print("{:<10} | {:<30} | {:<35}".format("Student ID", "Name", "Email"))
    print("-" * 80)
    for s in students:
        try:
            student_id, name, email = s.split(",", 2)
            print("{:<10} | {:<30} | {:<35}".format(student_id, name, email))
        except ValueError:
            print(f"[!] Invalid line in file: {s}")

    return students


# For add workflow
# -----------------------------------
def add_student():
    """Add a new student (ID, name, email)."""
    print("\n--- Add New Student ---")
    students = read_file(STUDENTS_FILE)

    # ID input loop
    while True:
        student_id = input("Enter Student ID (e.g., S001) or 'back' to cancel: ").strip()
        if student_id.lower() == "back":
            print("Returning to Student Menu...")
            time.sleep(1)
            return

        # Validation: Format S + 3 digits
        if not (student_id.upper().startswith("S") and len(student_id) == 4 and student_id[1:].isdigit()):
            print("[-] Invalid format! Must be S + 3 digits (e.g., S001).")
            continue

        # Validation: Check for duplicate ID
        if any(s.split(",")[0] == student_id.upper() for s in students):
            print("[-] Student ID already exists! Enter a new ID.")
            continue

        student_id = student_id.upper()
        break

    # Name input loop
    while True:
        name = input("Enter Student Name or 'back' to cancel: ").strip()
        if name.lower() == "back":
            return
        if not name:
            print("[-] Student name cannot be empty.")
            continue
        break

    # Email input loop
    while True:
        email = input("Enter Student Email or 'back' to cancel: ").strip()
        if email.lower() == "back":
            return
        if not email:
            print("[-] Email cannot be empty.")
            continue

        # Basic email format check
        if "@" not in email or "." not in email:
            print("[-] Please enter a valid email address.")
            continue
        break

    # Append to file
    append_file(STUDENTS_FILE, f"{student_id},{name},{email}")
    print("[+] Student added successfully!")

    # Ask the user next action (recursive call)
    while True:
        choice = input("Do you want to add another student? (Y/N): ").strip().lower()
        if choice == "y":
            return add_student()
        elif choice == "n":
            print("Returning to Student Menu...")
            time.sleep(1)
            return
        else:
            print("[-] Invalid choice! Please enter Y or N.")


# For edit workflow
# -----------------------------------
def edit_student():
    """Edit an existing student's name or email."""
    print("\n--- Edit Student Details ---")
    students = view_students_list()
    if not students:
        return

    while True:
        student_id = input("Enter Student ID to edit (or 'back' to cancel): ").strip().upper()

        if student_id.lower() == "back":
            return

        # Validate format
        if not (student_id.startswith("S") and len(student_id) == 4 and student_id[1:].isdigit()):
            print("[-] Invalid Student ID format! Example: S001.")
            continue

        found = False

        # Search for student ID
        for i, s_line in enumerate(students):
            parts = s_line.split(",", 2)
            if parts[0] == student_id:
                found = True

                current_name = parts[1]
                current_email = parts[2]

                print(f"\n[Current Name]: {current_name}")
                new_name = input("Enter New Student Name (or 'skip', or 'back' to cancel): ").strip()

                if new_name.lower() == "back": return

                # Update Name
                if new_name and new_name.lower() != 'skip':
                    name_to_save = new_name
                else:
                    name_to_save = current_name

                print(f"[Current Email]: {current_email}")
                new_email = input("Enter New Student Email (or 'skip', or 'back' to cancel): ").strip()

                if new_email.lower() == "back": return

                # Update Email
                if new_email and new_email.lower() != 'skip':
                    # Basic email format check
                    if "@" not in new_email or "." not in new_email:
                        print("[-] Invalid new email format. Update cancelled for this field.")
                        email_to_save = current_email
                    else:
                        email_to_save = new_email
                else:
                    email_to_save = current_email

                # Check if any actual change occurred
                if name_to_save == current_name and email_to_save == current_email:
                    print("[!] No changes were applied.")
                else:
                    # Update student line in list
                    students[i] = f"{student_id},{name_to_save},{email_to_save}"
                    write_file(STUDENTS_FILE, students)
                    print(f"[+] Student {student_id} updated successfully!")

                # Ask want edit another or no
                while True:
                    choice = input("Do you want to edit another student? (Y/N): ").strip().lower()
                    if choice == "y":
                        return edit_student()
                    elif choice == "n":
                        print("Returning to Student Menu...")
                        time.sleep(1)
                        return
                    else:
                        print("[-] Invalid choice! Please enter Y or N.")

        # If ID not found after loop
        if not found:
            print("[-] Student ID not found! Please enter a valid ID.")


# For delete workflow
# -----------------------------------
def delete_student():
    """Delete a student record."""
    print("\n--- Delete Student ---")
    students = view_students_list()
    if not students:
        return

    while True:
        student_id = input("Enter Student ID to delete (or 'back' to cancel): ").strip().upper()

        if student_id.lower() == "back":
            return

        # Validate format
        if not (student_id.startswith("S") and len(student_id) == 4 and student_id[1:].isdigit()):
            print("[-] Invalid Student ID format! Example: S001.")
            continue

        # Attempt delete
        student_line_to_delete = next((s for s in students if s.split(",")[0] == student_id), None)

        if student_line_to_delete is None:
            print("[-] Student ID not found! Please enter a valid ID.")
            continue

        name_to_delete = student_line_to_delete.split(",")[1]

        confirm = input(
            f"WARNING: Deleting '{name_to_delete}' ({student_id}) will also remove all their grades. Confirm? (yes/no): ").strip().lower()

        if confirm == 'yes':
            # 1. Delete from students list
            new_students = [s for s in students if s.split(",")[0] != student_id]

            # 2. Delete associated grades (This step requires a function from grades.py)
            # You will need to implement this in grades.py:
            # from grades import delete_grades_by_student
            # delete_grades_by_student(student_id)
            print(
                "[NOTE] Associated grades will be deleted when 'delete_grades_by_student' is implemented in grades.py.")

            write_file(STUDENTS_FILE, new_students)
            print(f"[+] Student {student_id} and their records deleted successfully!")
        else:
            print("[!] Deletion cancelled.")

        # Ask if delete another
        while True:
            choice = input("Do you want to delete another student? (Y/N): ").strip().lower()
            if choice == "y":
                return delete_student()
            elif choice == "n":
                print("Returning to Student Menu...")
                time.sleep(1)
                return
            else:
                print("[-] Invalid choice! Please enter Y or N.")