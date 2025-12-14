# Add Student
def add_student():
    sid = input("Enter Student ID: ")
    if not validate_id(sid):
        print(" Invalid ID format!")
        return

    name = input("Enter Student Name: ")
    email = input("Enter Student Email: ")

    if not validate_email(email):
        print(" Invalid email address!")
        return

    students = read_file("students.txt")

    for s in students:
        if sid == s.split(",")[0]:
            print(" Student ID already exists!")
            return

    with open("students.txt", "a") as f:
        f.write(f"{sid},{name},{email}\n")
    print(" Student added successfully!")


# Update/Delete Student
def update_delete_student():
    sid = input("Enter Student ID to update/delete: ")
    students = read_file("students.txt")

    new_list = []
    found = False

    for s in students:
        data = s.split(",")
        if sid == data[0]:
            found = True
            print("\n1. Update Student")
            print("2. Delete Student")
            choice = input("Choose option: ")

            if choice == "1":
                name = input("Enter new name: ")
                email = input("Enter new email: ")
                if validate_email(email):
                    new_list.append(f"{sid},{name},{email}")
                    print(" Student updated!")
                else:
                    print(" Invalid email! Update cancelled.")
                    new_list.append(s)
            elif choice == "2":
                print(" Student deleted!")
                continue  # skip adding to list
            else:
                print(" Invalid choice! No changes made.")
                new_list.append(s)
        else:
            new_list.append(s)

    if not found:
        print(" Student ID not found!")
    else:
        write_file("students.txt", new_list)
