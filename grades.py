from helper import read_file, write_file

# import time # NOTE: Removed unused 'import time'

# --- Constants (Assuming same file names as in other modules) ---
GRADES_FILE = "grades.txt"
STUDENTS_FILE = "students.txt"
COURSES_FILE = "courses.txt"


# --- Grade calculation logic ---

def calculate_letter_grade(marks):
    """
    Converts numerical marks (0-100) into a letter grade.
    """
    try:
        marks = int(marks)
    except ValueError:
        return "N/A"

    if marks < 0 or marks > 100:
        return "Invalid"

    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    elif marks >= 70:
        return "C"
    elif marks >= 60:
        return "D"
    else:
        return "F"


# --- Data Lookup Helpers (from other modules' data files) ---

def find_entity_name(entity_id, filename):
    lines = read_file(filename)
    for line in lines:
        parts = line.split(",", 2)
        if parts[0] == entity_id:
            return parts[1]
    return None


def find_student_name(student_id):
    return find_entity_name(student_id, STUDENTS_FILE)


def find_course_name(course_id):
    return find_entity_name(course_id, COURSES_FILE)


def get_mark_record(student_id, course_id, grades):
    """
    Helper to find an existing mark record.
    Returns the index and the full record string if found, otherwise None, None.
    """
    for i, g in enumerate(grades):
        g_id, c_id, *rest = g.split(",", 2)
        if g_id == student_id and c_id == course_id:
            return i, g  # Returns index and the full record string
    return None, None


# --- Delete Function for data (Used by student.py and course.py) ---

def delete_grades_by_student(student_id):
    """Deletes all grade records for a given student ID."""
    grades = read_file(GRADES_FILE)
    new_grades = [g for g in grades if g.split(",")[0] != student_id]
    write_file(GRADES_FILE, new_grades)


def delete_grades_by_course(course_id):
    """Deletes all grade records for a given course ID."""
    grades = read_file(GRADES_FILE)
    new_grades = [g for g in grades if g.split(",")[1] != course_id]
    write_file(GRADES_FILE, new_grades)


# -----------------------------------------------
# 1. GRADES MANAGEMENT (ADD, EDIT, DELETE)
# -----------------------------------------------

def get_validated_marks():
    """Helper function to loop until valid marks (0-100) are entered."""
    while True:
        try:
            marks_str = input("Enter Marks (0-100): ").strip()
            marks = int(marks_str)
            if 0 <= marks <= 100:
                return marks
            else:
                print("[-] Marks must be between 0 and 100.")
        except ValueError:
            print("[-] Invalid input. Please enter a number.")


def add_mark():
    """Adds a new mark record for a student in a course."""
    print("\n--- ADD NEW MARK ---")

    student_id = input("Enter Student ID (or 'back'): ").strip().upper()
    if student_id == 'BACK': return

    course_id = input("Enter Course ID (or 'back'): ").strip().upper()
    if course_id == 'BACK': return

    # --- Validation ---
    if not find_student_name(student_id):
        print(f"[-] Error: Student ID {student_id} not found.")
        return
    if not find_course_name(course_id):
        print(f"[-] Error: Course ID {course_id} not found.")
        return

    grades = read_file(GRADES_FILE)

    # Check for existing mark 
    if get_mark_record(student_id, course_id, grades)[0] is not None:
        print(f"[!] Mark already exists for {student_id} in {course_id}. Use 'Edit Mark' instead.")
        return

    marks = get_validated_marks()
    letter_grade = calculate_letter_grade(marks)

    new_record = f"{student_id},{course_id},{marks},{letter_grade}"
    grades.append(new_record)
    write_file(GRADES_FILE, grades)

    print(f"[+] Mark added successfully: {marks} ({letter_grade})")
    input("\nPress ENTER to continue...")


def edit_mark():
    """Edits an existing mark record for a student in a course, displaying current mark."""
    print("\n--- EDIT EXISTING MARK ---")

    student_id = input("Enter Student ID to edit mark for (or 'back'): ").strip().upper()
    if student_id == 'BACK': return

    course_id = input("Enter Course ID to edit mark for (or 'back'): ").strip().upper()
    if course_id == 'BACK': return

    grades = read_file(GRADES_FILE)
    index, old_record = get_mark_record(student_id, course_id, grades)

    # Check existence
    if index is None:
        print(f"[!] No existing mark found for {student_id} in {course_id}. Use 'Add Mark' instead.")
        return

    # Display existing mark
    old_marks = old_record.split(",")[2]
    old_grade = old_record.split(",")[3]

    print(f"\n[i] Found existing mark for Student {student_id} in Course {course_id}.")
    print(f"    Current Mark: {old_marks} ({old_grade})")

    # Get new mark
    marks = get_validated_marks()
    letter_grade = calculate_letter_grade(marks)

    # Update and save
    new_record = f"{student_id},{course_id},{marks},{letter_grade}"
    grades[index] = new_record  # Update existing record in the list
    write_file(GRADES_FILE, grades)

    print(f"[+] Mark updated successfully: {marks} ({letter_grade})")
    input("\nPress ENTER to continue...")


def delete_mark():
    """Deletes a specific mark record by Student ID and Course ID, confirming deletion."""
    print("\n--- DELETE MARK ---")

    student_id = input("Enter Student ID to delete mark from (or 'back'): ").strip().upper()
    if student_id == 'BACK': return

    course_id = input("Enter Course ID to delete mark for (or 'back'): ").strip().upper()
    if course_id == 'BACK': return

    if not find_student_name(student_id) or not find_course_name(course_id):
        print("[-] Error: Invalid Student ID or Course ID.")
        return

    grades = read_file(GRADES_FILE)
    index, record_to_delete = get_mark_record(student_id, course_id, grades)

    if index is None:
        print(f"[!] Mark for Student {student_id} in Course {course_id} was not found.")
        return

    # Display existing mark for confirmation
    mark, grade = record_to_delete.split(",")[2:]
    print(f"\n[i] Found Mark: {mark} ({grade}) for Student {student_id} in Course {course_id}.")
    confirm = input("Are you sure you want to DELETE this mark? (Y/N): ").strip().upper()

    if confirm == 'Y':
        del grades[index]
        write_file(GRADES_FILE, grades)
        print(f"[+] Success! Mark has been deleted.")
    else:
        print("[!] Deletion cancelled.")

    input("\nPress ENTER to continue...")


def grades_management_menu():
    """Menu for all grades management options (Menu Option 3)."""
    while True:
        print("\n--- GRADES MANAGEMENT ---")
        print("[1] Add New Mark")
        print("[2] Edit Existing Mark")
        print("[3] Delete Mark")
        print("[0] Back to Main Menu")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            add_mark()
        elif choice == '2':
            edit_mark()
        elif choice == '3':
            delete_mark()
        elif choice == '0':
            break
        else:
            print("[-] Invalid choice.")

# ===============================================
# 2. PERFORMANCE REPORTS (Display Summaries)
# ===============================================

def display_individual_performance():
    """Displays the performance report of a student (Core Requirement)."""
    print("\n--- INDIVIDUAL STUDENT REPORT ---")

    student_id = input("Enter Student ID (or 'back'): ").strip().upper()
    if student_id == 'BACK': return

    student_name = find_student_name(student_id)
    if not student_name:
        print(f"[-] Error: Student ID {student_id} not found.")
        return

    grades = read_file(GRADES_FILE)
    student_grades = [g for g in grades if g.startswith(student_id + ',')]

    if not student_grades:
        print(f"[!] Student {student_name} ({student_id}) has no recorded grades.")
        return

    print(f"\nReport for: {student_name} ({student_id})")
    print("-" * 50)
    print("{:<15} | {:<25} | {:<8} | {:<5}".format("Course ID", "Course Name", "Marks", "Grade"))
    print("-" * 50)

    total_marks = 0
    count = 0

    for g in student_grades:
        try:
            _, course_id, marks_str, grade = g.split(",", 3)
            course_name = find_course_name(course_id) or "N/A"
            marks = int(marks_str)
            total_marks += marks
            count += 1
            print("{:<15} | {:<25} | {:<8} | {:<5}".format(course_id, course_name, marks, grade))
        except Exception:
            print(f"[!] Corrupted grade record: {g}")

    print("-" * 50)
    if count > 0:
        average = total_marks / count
        print(f"Overall Average Mark: {average:.2f}")

    input("\nPress ENTER to return to Report Menu...")


def display_course_summary():
    """Displays the list of students, with average, highest, and lowest marks (Core Requirement)."""
    print("\n--- COURSE PERFORMANCE SUMMARY ---")

    course_id = input("Enter Course ID (or 'back'): ").strip().upper()
    if course_id == 'BACK': return

    course_name = find_course_name(course_id)
    if not course_name:
        print(f"[-] Error: Course ID {course_id} not found.")
        return

    grades = read_file(GRADES_FILE)
    course_grades = []
    course_marks = []

    # 1. Filter grades for the specific course
    for g in grades:
        try:
            g_student_id, g_course_id, marks_str, grade = g.split(",", 3)
            if g_course_id == course_id:
                marks = int(marks_str)
                course_grades.append({'id': g_student_id, 'marks': marks, 'grade': grade})
                course_marks.append(marks)
        except Exception:
            continue

    if not course_grades:
        print(f"[!] Course {course_name} ({course_id}) has no recorded grades.")
        return

    # 2. Calculate statistics
    avg_mark = sum(course_marks) / len(course_marks)
    high_mark = max(course_marks)
    low_mark = min(course_marks)

    print(f"\nSummary for Course: {course_name} ({course_id})")
    print("-" * 75)
    print("{:<10} | {:<30} | {:<8} | {:<5}".format("ID", "Student Name", "Marks", "Grade"))
    print("-" * 75)

    # 3. Display student list
    for record in course_grades:
        student_name = find_student_name(record['id']) or "N/A"
        print("{:<10} | {:<30} | {:<8} | {:<5}".format(
            record['id'], student_name, record['marks'], record['grade']
        ))

    print("-" * 75)
    # 4. Display summary statistics
    print(f"Total Enrolled: {len(course_grades)}")
    print(f"Average Mark: {avg_mark:.2f}")
    print(f"Highest Mark: {high_mark}")
    print(f"Lowest Mark: {low_mark}")

    input("\nPress ENTER to return to Report Menu...")


def performance_report_menu():
    """Menu for displaying individual and course performance summaries (Menu Option 4)."""
    while True:
        print("\n--- PERFORMANCE REPORTS ---")
        print("[1] Individual Student Report")
        print("[2] Course Performance Summary")
        print("[0] Back to Main Menu")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            display_individual_performance()
        elif choice == '2':
            display_course_summary()
        elif choice == '0':
            break
        else:
            print("[-] Invalid choice.")


# ===============================================
# 3. EXPORT REPORTS (File Export)
# ===============================================

def export_report_logic(report_type):
    """Handles the file writing for exporting reports"""

    if report_type == 'individual':
        student_id = input("Enter Student ID for export: ").strip().upper()
        if not find_student_name(student_id):
            print(f"[-] Error: Student ID {student_id} not found.")
            return

        report_content = []
        # Reuse display_individual_performance logic to build content
        student_name = find_student_name(student_id)
        grades = read_file(GRADES_FILE)
        student_grades = [g for g in grades if g.startswith(student_id + ',')]

        if not student_grades:
            print("[!] No grades to export for this student.")
            return

        report_content.append(f"Performance Report for: {student_name} ({student_id})\n")
        report_content.append("{:<15} | {:<25} | {:<8} | {:<5}".format("Course ID", "Course Name", "Marks", "Grade"))
        report_content.append("-" * 55)

        for g in student_grades:
            try:
                _, course_id, marks_str, grade = g.split(",", 3)
                course_name = find_course_name(course_id) or "N/A"
                report_content.append(
                    "{:<15} | {:<25} | {:<8} | {:<5}".format(course_id, course_name, marks_str, grade))
            except Exception:
                pass

        filename = f"report_student_{student_id}.txt"

    elif report_type == 'course':
        course_id = input("Enter Course ID for export: ").strip().upper()
        course_name = find_course_name(course_id)
        if not course_name:
            print(f"[-] Error: Course ID {course_id} not found.")
            return

        report_content = []
        grades = read_file(GRADES_FILE)
        course_grades = []
        course_marks = []

        # Filter grades and calculate stats 
        for g in grades:
            try:
                g_student_id, g_course_id, marks_str, grade = g.split(",", 3)
                if g_course_id == course_id:
                    marks = int(marks_str)
                    course_grades.append({'id': g_student_id, 'marks': marks, 'grade': grade})
                    course_marks.append(marks)
            except Exception:
                pass

        if not course_grades:
            print("[!] No grades to export for this course.")
            return

        avg_mark = sum(course_marks) / len(course_marks)
        high_mark = max(course_marks)
        low_mark = min(course_marks)

        report_content.append(f"Course Performance Summary for: {course_name} ({course_id})\n")
        report_content.append(f"Average Mark: {avg_mark:.2f}")
        report_content.append(f"Highest Mark: {high_mark}")
        report_content.append(f"Lowest Mark: {low_mark}")
        report_content.append("\nStudent Enrollments:")
        report_content.append("{:<10} | {:<30} | {:<8} | {:<5}".format("ID", "Student Name", "Marks", "Grade"))
        report_content.append("-" * 55)

        for record in course_grades:
            student_name = find_student_name(record['id']) or "N/A"
            report_content.append("{:<10} | {:<30} | {:<8} | {:<5}".format(
                record['id'], student_name, record['marks'], record['grade']
            ))

        filename = f"report_course_{course_id}.txt"
    else:
        return

    # Write content to file
    try:
        with open(filename, 'w') as f:
            for line in report_content:
                f.write(line + "\n")
        print(f"[+] Success! Report exported to {filename}")
    except Exception as e:
        print(f"[-] Error exporting report: {e}")


def export_report_menu():
    """Menu for exporting reports to files (Menu Option 5)."""
    while True:
        print("\n--- EXPORT REPORTS ---")
        print("[1] Export Individual Student Report")
        print("[2] Export Course Performance Summary")
        print("[0] Back to Main Menu")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            export_report_logic('individual')
        elif choice == '2':
            export_report_logic('course')
        elif choice == '0':
            break
        else:
            print("[-] Invalid choice.")
