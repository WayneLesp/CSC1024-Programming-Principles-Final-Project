COURSES_FILE = "courses.txt"

# -------------------------
# File handling helpers
# -------------------------
def read_file(filename):
    try:
        with open(filename, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def write_file(filename, data_list):
    with open(filename, "w") as f:
        for line in data_list:
            f.write(line + "\n")

def append_file(filename, line):
    with open(filename, "a") as f:
        f.write(line + "\n")

# -------------------------
# Course Management
# -------------------------
def view_courses():
    """Display all available courses and return the list."""
    courses = read_file(COURSES_FILE)
    if not courses:
        print("\n[-] No courses available.")
        return []

    print("\n--- Available Courses ---")
    print("{:<10} | {:<30}".format("Course ID", "Course Name"))
    print("-"*45)
    for c in courses:
        try:
            course_id, course_name = c.split(",", 1)
            print("{:<10} | {:<30}".format(course_id, course_name))
        except ValueError:
            print(f"[!] Invalid line in file: {c}")
    return courses

def add_course():
    """Add a new course."""
    print("\n--- Add New Course ---")
    courses = read_file(COURSES_FILE)

    # ID input loop
    while True:
        course_id = input("Enter Course ID (e.g., C001) or 'back' to cancel: ").strip()
        if course_id.lower() == "back":
            return
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
            return
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
            break  # back to start of while True loop
        elif choice == "n":
            return  # go back to course menu
        else:
            print("[-] Invalid choice! Please enter Y or N.")

def edit_course():
    """Edit an existing course."""
    print("\n--- Edit Course ---")
    courses = view_courses()
    if not courses:
        return

    while True:
        course_id = input("Enter Course ID to edit (or 'back' to cancel): ").strip()
        if course_id.lower() == "back":
            return

        for i, c in enumerate(courses):
            if c.split(",")[0] == course_id:
                while True:
                    new_name = input("Enter new Course Name (or 'back' to cancel): ").strip()
                    if new_name.lower() == "back":
                        return
                    if not new_name:
                        print("[-] Course name cannot be empty.")
                        continue
                    if any(courses[j].split(",")[1].strip().lower() == new_name.lower() for j in range(len(courses)) if j != i):
                        print("[-] Course name already exists!")
                        continue
                    courses[i] = f"{course_id},{new_name}"
                    write_file(COURSES_FILE, courses)
                    print("[+] Course updated successfully!")
                    return
        else:
            print("[-] Course ID not found! Try again.")

def delete_course():
    """Delete a course."""
    print("\n--- Delete Course ---")
    courses = view_courses()
    if not courses:
        return

    course_id = input("Enter Course ID to delete (or 'back' to cancel): ").strip()
    if course_id.lower() == "back":
        return

    new_courses = [c for c in courses if c.split(",")[0] != course_id]
    if len(new_courses) == len(courses):
        print("[-] Course ID not found!")
        return

    write_file(COURSES_FILE, new_courses)
    print("[+] Course deleted successfully!")


