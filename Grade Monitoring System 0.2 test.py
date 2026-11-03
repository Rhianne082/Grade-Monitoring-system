students = [
    ["02-2526-098765", "Aria", "BSIT 1-A", [
        ["GEN 001", [90]],
        ["GEN 018", [85]],
        ["GEN 008", [88]]
    ]],
    ["02-2526-678990", "Runolo", "BSIT 1-A", [
        ["GEN 001", [88]],
        ["GEN 018", [80]],
        ["GEN 008", [89]]
    ]],
    ["02-2526-576879", "Jarius", "BSIT 1-B", [
        ["GEN 001", [88]],
        ["GEN 018", ["Missing"]],
        ["GEN 008", [70]]
    ]]
]

teachers = []

def enter_name(message):
    while True:
        name = input(message).strip()

        if name == "":
            print("Name cannot be empty.")
        elif any(character.isdigit() for character in name):
            print("Names cannot contain numbers.")
        else:
            return name

def teacher_registration():
    print("\n===== TEACHER REGISTRATION =====")
    name = enter_name("Enter Teacher Name: ")

    for teacher in teachers:
        if teacher[0].lower() == name.lower():
            print("Teacher name is already registered.")
            return

    password = input("Create Password: ")
    confirm_password = input("Confirm Password: ")

    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    teachers.append([name, password])
    print("Teacher registration successful!")

def find_student_by_name(name):
    matches = []

    for student in students:
        if student[1].lower() == name.lower():
            matches.append(student)

    if len(matches) == 1:
        return matches[0]

    return None

def find_student_by_id(student_id):
    for student in students:
        if str(student[0]) == str(student_id):
            return student

    return None

def calculate_average(student):
    total = 0
    grade_count = 0

    for subject in student[3]:
        for grade in subject[1]:
            if isinstance(grade, (int, float)):
                total += grade
                grade_count += 1

    if grade_count == 0:
        return None

    return total / grade_count

def get_student_status(student):
    has_missing = False
    has_pending = False

    for subject in student[3]:
        for grade in subject[1]:
            if grade == "Missing":
                has_missing = True
            elif grade == "Pending":
                has_pending = True

    if has_missing:
        return "MISSING ACTIVITY"
    elif has_pending:
        return "PENDING ACTIVITY"

    average = calculate_average(student)

    if average is None:
        return "NO GRADES"
    elif average >= 75:
        return "PASSING"
    else:
        return "FAILING"

def display_student(student):
    average = calculate_average(student)

    print("\n----------------------------------------")
    print("Student ID:", student[0])
    print("Student Name:", student[1])
    print("Class Section:", student[2])
    print("----------------------------------------")

    for subject in student[3]:
        print(subject[0] + ":")
        for number, grade in enumerate(subject[1], start=1):
            print("  Activity", number, ":", grade)

    if average is None:
        print("Average: N/A")
    else:
        print("Average:", round(average, 2))

    print("Status:", get_student_status(student))

def view_students():
    print("\n" + "=" * 100)
    print("ALL STUDENT RECORDS")
    print("=" * 100)

    if len(students) == 0:
        print("No students registered.")
        return

    print(f"{'Student ID':<15}{'Name':<15}{'Section':<15}{'Average':<12}{'Status':<25}")
    print("-" * 100)

    for student in students:
        average = calculate_average(student)

        if average is None:
            average_display = "N/A"
        else:
            average_display = str(round(average, 2))

        print(
            f"{str(student[0]):<15}"
            f"{student[1]:<15}"
            f"{student[2]:<15}"
            f"{average_display:<12}"
            f"{get_student_status(student):<25}"
        )

    print("=" * 100)

def register_student():
    print("\n===== REGISTER STUDENT =====")
    while True:
        student_id = input("Enter Student ID (example: 02-2526-098765): ").strip()
        id_parts = student_id.split("-")

        if (len(id_parts) == 3
                and len(id_parts[0]) == 2
                and len(id_parts[1]) == 4
                and len(id_parts[2]) == 6
                and id_parts[0].isdigit()
                and id_parts[1].isdigit()
                and id_parts[2].isdigit()):
            break
        else:
            print("Invalid Student ID. Use this format: 02-2526-098765")

    if find_student_by_id(student_id) is not None:
        print("Student ID already exists.")
        return

    name = enter_name("Enter Student Name: ")
    section = input("Enter Student Section (example: BSIT 1-A): ").strip()

    if section == "":
        print("Student section cannot be empty.")
        return

    subjects = []

    print("\nAdd subjects for this student.")
    while True:
        subject_name = input("Enter subject code/name (or type DONE): ").strip()

        if subject_name.lower() == "done":
            break

        if subject_name == "":
            print("Subject name cannot be empty.")
            continue

        already_exists = False
        for subject in subjects:
            if subject[0].lower() == subject_name.lower():
                already_exists = True

        if already_exists:
            print("This subject is already added for this student.")
            continue

        subjects.append([subject_name, ["Pending"]])
        print("Subject added with Activity 1 set to Pending.")

        more = input("Add another subject? (yes/no): ").strip().lower()
        if more not in ["yes", "y"]:
            break

    if len(subjects) == 0:
        subjects = [
            ["GEN 001", ["Pending"]],
            ["GEN 018", ["Pending"]],
            ["GEN 008", ["Pending"]]
        ]

    students.append([student_id, name, section, subjects])
    print("Student registered successfully!")

def select_student_for_grading():
    print("\n===== SELECT STUDENT =====")
    student_id = input("Enter Student ID: ").strip()
    student = find_student_by_id(student_id)

    if student is None:
        print("Student ID not found.")
        return None

    print("Student Name:", student[1])
    print("Student Section:", student[2])

    confirm_name = enter_name("Confirm Student Name: ")
    confirm_section = input("Confirm Student Section: ").strip()

    if confirm_name.lower() != student[1].lower():
        print("Student name does not match the selected ID.")
        return None

    if confirm_section.lower() != student[2].lower():
        print("Student section does not match the selected student.")
        return None

    print("Student selected successfully.")
    return student

def enter_or_edit_grade(student):
    while True:
        print("\n===== ENTER/EDIT GRADE =====")
        print("Selected Student:", student[1])
        print("Student ID:", student[0])
        print("Student Section:", student[2])
        print("\nSubjects:")

        for number, subject in enumerate(student[3], start=1):
            print(str(number) + ".", subject[0], "-", subject[1])

        print(str(len(student[3]) + 1) + ". Add a New Subject")
        print("0. Finish Editing")

        choice = input("Choose a subject or option: ").strip()

        if choice == "0":
            break

        if choice == str(len(student[3]) + 1):
            add_subject(student)
            continue

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(student[3]):
            print("Invalid choice. Please select an item from the list.")
            continue

        subject = student[3][int(choice) - 1]
        edit_subject_activities(subject)

        another = input(
            "\nWould you like to enter/edit a grade for another subject? (yes/no): "
        ).strip().lower()

        if another not in ["yes", "y"]:
            break

    display_student(student)

def edit_subject_activities(subject):
    while True:
        print("\n===== " + subject[0] + " ACTIVITIES =====")

        for number, grade in enumerate(subject[1], start=1):
            print(str(number) + ". Activity", number, "-", grade)

        print(str(len(subject[1]) + 1) + ". Add Another Activity")
        print("0. Return to Subjects")

        choice = input("Choose an activity or option: ").strip()

        if choice == "0":
            return

        if choice == str(len(subject[1]) + 1):
            subject[1].append("Pending")
            print("New activity added with status Pending.")
            continue

        if not choice.isdigit() or int(choice) < 1 or int(choice) > len(subject[1]):
            print("Invalid choice.")
            continue

        activity_index = int(choice) - 1
        print("Current status/grade:", subject[1][activity_index])
        print("1. Enter a grade")
        print("2. Mark as Missing")
        print("3. Mark as Pending")
        print("4. Cancel")

        action = input("Choose an action: ").strip()

        if action == "1":
            try:
                grade = float(input("Enter grade (0-100): "))

                if not 0 <= grade <= 100:
                    print("Grade must be between 0 and 100.")
                    continue

                subject[1][activity_index] = grade
                print("Grade updated successfully.")

            except ValueError:
                print("Invalid grade. Please enter a number.")

        elif action == "2":
            subject[1][activity_index] = "Missing"
            print("Activity marked as Missing.")

        elif action == "3":
            subject[1][activity_index] = "Pending"
            print("Activity marked as Pending.")

        elif action == "4":
            continue

        else:
            print("Invalid choice.")

def add_subject(student):
    print("\n===== ADD NEW SUBJECT =====")
    subject_name = input("Enter new subject code/name: ").strip()

    if subject_name == "":
        print("Subject name cannot be empty.")
        return

    for subject in student[3]:
        if subject[0].lower() == subject_name.lower():
            print("This student already has that subject.")
            return

    student[3].append([subject_name, ["Pending"]])
    print(subject_name, "added successfully with Activity 1 set to Pending.")

def edit_grade():
    student = select_student_for_grading()

    if student is None:
        return

    enter_or_edit_grade(student)

def mark_missing():
    student = select_student_for_grading()

    if student is None:
        return

    if len(student[3]) == 0:
        print("This student has no subjects yet.")
        return

    print("\n===== MARK MISSING ACTIVITY =====")

    for number, subject in enumerate(student[3], start=1):
        print(str(number) + ".", subject[0])

    choice = input("Choose a subject: ").strip()

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(student[3]):
        print("Invalid subject.")
        return

    subject = student[3][int(choice) - 1]

    for number, grade in enumerate(subject[1], start=1):
        print(str(number) + ". Activity", number, "-", grade)

    activity = input("Choose activity to mark Missing: ").strip()

    if not activity.isdigit() or int(activity) < 1 or int(activity) > len(subject[1]):
        print("Invalid activity.")
        return

    subject[1][int(activity) - 1] = "Missing"
    print("Activity marked as Missing.")
    display_student(student)

def passing_students():
    print("\n===== PASSING STUDENTS =====")
    found = False

    for student in students:
        average = calculate_average(student)

        if average is not None and average >= 75 and get_student_status(student) == "PASSING":
            print(
                student[1],
                "| Student ID:", student[0],
                "| Section:", student[2],
                "| Average:", round(average, 2)
            )
            found = True

    if not found:
        print("No passing students found.")

def failing_students():
    print("\n===== STUDENTS NEEDING ATTENTION =====")
    found = False

    for student in students:
        status = get_student_status(student)
        average = calculate_average(student)

        if status != "PASSING":
            if average is None:
                average_display = "N/A"
            else:
                average_display = round(average, 2)

            print(
                student[1],
                "| Student ID:", student[0],
                "| Section:", student[2],
                "| Average:", average_display,
                "| Status:", status
            )
            found = True

    if not found:
        print("No students need attention.")

def view_students_by_section():
    print("\n===== VIEW STUDENTS BY SECTION =====")
    sections = []

    for student in students:
        if student[2] not in sections:
            sections.append(student[2])

    if len(sections) == 0:
        print("No class sections available.")
        return

    for number, section in enumerate(sections, start=1):
        print(str(number) + ".", section)

    print("0. Return")

    choice = input("Choose a section: ").strip()

    if choice == "0":
        return

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(sections):
        print("Invalid choice.")
        return

    selected_section = sections[int(choice) - 1]
    print("\n===== " + selected_section + " =====")

    for student in students:
        if student[2] == selected_section:
            display_student(student)

def student_view():
    student_id = input("Enter your Student ID: ").strip()
    student = find_student_by_id(student_id)

    if student is None:
        print("Student ID not found.")
    else:
        print("\n===== STUDENT GRADE VIEW =====")
        display_student(student)
def teacher_login():
    if len(teachers) == 0:
        print("No registered teachers. Please register first.")
        return

    while True:
        print("\n===== TEACHER LOGIN =====")
        print("Enter 0 to return to Main Menu.")

        name = input("Enter Teacher Name: ")

        if name == "0":
            break

        password = input("Enter Password: ")
        found = False

        for teacher in teachers:
            if teacher[0].lower() == name.strip().lower() and teacher[1] == password:
                found = True
                break

        if found:
            print("Login successful!")
            teacher_menu()
            break
        else:
            print("Incorrect name or password. Please try again.")

def teacher_menu():
    while True:
        print("\n================================")
        print("          TEACHER MENU")
        print("================================")
        print("1. View All Students")
        print("2. Register Student")
        print("3. Enter/Edit Grade")
        print("4. Mark Missing Activity")
        print("5. View Passing Students")
        print("6. View Failing Students")
        print("7. View Students by Section")
        print("8. Return to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_students()
        elif choice == "2":
            register_student()
        elif choice == "3":
            edit_grade()
        elif choice == "4":
            mark_missing()
        elif choice == "5":
            passing_students()
        elif choice == "6":
            failing_students()
        elif choice == "7":
            view_students_by_section()
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please try again.")

while True:
    print("\n================================")
    print("      GRADE MONITORING SYSTEM")
    print("================================")
    print("1. Teacher Login")
    print("2. Student View")
    print("3. Teacher Registration")
    print("4. Exit")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        teacher_login()
    elif choice == "2":
        student_view()
    elif choice == "3":
        teacher_registration()
    elif choice == "4":
        print("Thank you for using the Grade Monitoring System.")
        break