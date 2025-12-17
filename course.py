import time
from helper import read_file, write_file, append_file
COURSES_FILE = "courses.txt"

# -------------------------
# Course Management
# -------------------------

#For view workflow
# -----------------------------------
"""With returning to courses menu message"""
def view_courses_menu():
    """Display all available courses and return the list."""
    courses = read_file(COURSES_FILE)

    #if no courses are found,show error message
    if not courses:
        print("\n[-] No courses available.")
        return []

    # Sort courses by their numeric course ID
    courses = sorted(courses, key=lambda x: int(x.split(",")[0][1:]))

    print("\n--- Available Courses ---")
    print("-"*45)
    print("{:<10} | {:<30}".format("Course ID", "Course Name"))
    print("-"*45)
    for c in courses:
        try:
            course_id, course_name = c.split(",", 1)
            # Print the course details in a formatted table row
            print("{:<10} | {:<30}".format(course_id, course_name))
        except ValueError:
            print(f"[!] Invalid line in file: {c}")
    input("\nPress ENTER to return to Courses Menu...")
    return courses

# view workflow (for edit/delete)
# -----------------------------------
def view_courses_list():
    """View courses for Edit/Delete without returning to course menu message."""
    courses = read_file(COURSES_FILE)
    if not courses:
        print("\n[-] No courses available.")
        return []

    # Sort courses by course ID (numeric part)
    courses = sorted(courses, key=lambda x: int(x.split(",")[0][1:]))
    print("\n--- Available Courses ---")
    print("-"*45)
    print("{:<10} | {:<30}".format("Course ID", "Course Name"))
    print("-"*45)
    for c in courses:
        try:
            course_id, course_name = c.split(",", 1)
            print("{:<10} | {:<30}".format(course_id, course_name))
        except ValueError:
            print(f"[!] Invalid line in file: {c}")

    return courses

# For add workflow
# -----------------------------------
def add_course():
    """Add a new course."""
    print("\n--- Add New Course ---")
    courses = read_file(COURSES_FILE)

    # ID input loop
    while True:
        course_id = input("Enter Course ID (e.g., C001) or 'back' to cancel: ").strip()
        if course_id.lower() == "back":
            print("Returning to Course Menu...")
            time.sleep(1)
            return courses
        if not (course_id.startswith("C") and len(course_id) == 4 and course_id[1:].isdigit()):
            print("[-] Invalid format! Must be C + 3 digits (e.g., C001).")
            continue
        if any(c.split(",")[0] == course_id for c in courses):
            print("[-] Course ID already exists! Enter a new ID.")
            continue
        break

    # Name input loop
    while True:
        course_name = input("Enter Course Name or 'back' to cancel: ").strip()
        if course_name.lower() == "back":
            return courses
        if not course_name:
            print("[-] Course name cannot be empty.")
            continue
        if any(c.split(",")[1].strip().lower() == course_name.lower() for c in courses):
            print("[-] Course name already exists! Enter a new name.")
            continue
        break
    #Append to file
    append_file(COURSES_FILE, f"{course_id},{course_name}")
    print("[+] Course added successfully!")

    #Ask the user next action
    while True:
        choice = input("Do you want to add another course? (Y/N): ").strip().lower()
        if choice == "y":
            return add_course()
        elif choice == "n":
            print("Returning to Course Menu...")
            time.sleep(1)
            return courses  # go back to course menu
        else:
            print("[-] Invalid choice! Please enter Y or N.")

# For edit workflow
# -----------------------------------
def edit_course():
    """Edit an existing course."""
    print("\n--- Edit Course ---")
    courses = view_courses_list()
    if not courses:
        return

    while True:
        course_id = input("Enter Course ID to edit (or 'back' to cancel): ").strip()

        # allow exit
        if course_id.lower() == "back":
            return

        # ---- validate format: must be C + exactly 3 digits ----
        if not (
            course_id.upper().startswith("C") and
            len(course_id) == 4 and
            course_id[1:].isdigit()
        ):
            print("[-] Invalid Course ID format! Example: C001, C120, C450")
            continue

        found = False

        # ---- search for course ID ----
        for i, c in enumerate(courses):
            if c.split(",")[0] == course_id:
                found = True

                # --- edit course name ---
                while True:
                    new_name = input("Enter new Course Name (or 'back' to cancel): ").strip()

                    if new_name.lower() == "back":
                        return

                    if not new_name:
                        print("[-] Course name cannot be empty.")
                        continue

                    # prevent duplicate names
                    if any(
                        courses[j].split(",")[1].strip().lower() == new_name.lower()
                        for j in range(len(courses)) if j != i
                    ):
                        print("[-] Course name already exists!")
                        continue

                    # update course
                    courses[i] = f"{course_id},{new_name}"
                    write_file(COURSES_FILE, courses)
                    print("[+] Course updated successfully!")

                    # ask want edit another or no
                    while True:
                        choice = input("Do you want to edit another course? (Y/N): ").strip().lower()

                        if choice == "y":
                            return edit_course()
                        elif choice == "n":
                            print("Returning to Course Menu...")
                            time.sleep(1)
                            return
                        else:
                            print("[-] Invalid choice! Please enter Y or N.")

        # ---- if ID not found after loop ----
        if not found:
            print("[-] Course ID not found! Please enter a valid ID.")

# For delete workflow
# -----------------------------------
def delete_course():
    """Delete a course."""
    print("\n--- Delete Course ---")
    courses = view_courses_list()
    if not courses:
        return

    while True:
        course_id = input("Enter Course ID to delete (or 'back' to cancel): ").strip()

        # allow exit
        if course_id.lower() == "back":
            return

        # ---- validate format: must be C + exactly 3 digits ----
        if not (course_id.upper().startswith("C") and len(course_id) == 4 and course_id[1:].isdigit()):
            print("[-] Invalid Course ID format! Example: C001, C123, C450")
            continue

        # attempt delete
        new_courses = [c for c in courses if c.split(",")[0] != course_id]

        # ---- if ID not found ----
        if len(new_courses) == len(courses):
            print("[-] Course ID not found! Please enter a valid ID.")
            continue   # simply ask again

        # ---- delete course ----
        write_file(COURSES_FILE, new_courses)
        print("[+] Course deleted successfully!")

        # ---- ask if delete another ----
        while True:
            choice = input("Do you want to delete another course? (Y/N): ").strip().lower()
            if choice == "y":
                return delete_course()
            elif choice == "n":
                print("Returning to Course Menu...")
                time.sleep(1)
                return
            else:
                print("[-] Invalid choice! Please enter Y or N.")


