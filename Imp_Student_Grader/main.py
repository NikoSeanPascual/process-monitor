students = {}

print("Don't know any commands? Type (help)")
def add_student():
    input2 = input("What the name of the student that will be added? ").title().strip()
    input3 = float(input("What is the grade of the student? "))
    students[input2] = input3
def check_students():
    counter = 1
    print(f"===== STUDENTS AND GRADES =====")
    for input2, input3 in students.items():
        print(f"{counter}. {input2}: {input3}")
        counter += 1
def remove_student():
    try:
        print(f"===== STUDENTS AND GRADES =====")
        counter = 1
        for input2, input3 in students.items():
            print(f"{counter}. {input2}: {input3}")
            counter += 1
        student_num = int(input("Enter the number of the student to remove: "))


        student_to_remove = list(students.keys())[student_num - 1]

        del students[student_to_remove]
        print(f"{student_to_remove} has been removed.")

    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number corresponding to a student.")

def lowest_grades():
    if students:
        lowest_student = min(students, key=students.get)
        print(f"The student with the lowest grade is {lowest_student} with a grade of {students[lowest_student]}")
    else:
        print("No students to check.")

def highest_grades():
    if students:
        highest_student = max(students, key=students.get)
        print(f"The student with the highest grade is {highest_student} with a grade of {students[highest_student]}")
    else:
        print("No students to check.")

def avg_grade():
    if students:
        total_grades = sum(students.values())
        num_students = len(students)
        average = total_grades / num_students
        print(f"The average grade of all students is {average:.2f}")
    else:
        print("No students to calculate average.")

input1 = ""
while input1 != 'x':
    input1 = input("Enter a command you want to do: ").lower().strip()

    if input1 == "help":
        print("===COMMANDS===\n"
              "Add Student: (1)\n"
              "Remove Student: (2)\n"
              "Check students: (3)\n"
              "Check Lowest Grades: (4)\n"
              "Check Highest Grades: (5)\n"
              "Overall Average Grades: (6)\n"
              "quit: (x)")
    elif input1 == "1":
        add_student()
    elif input1 == "2":
        remove_student()
    elif input1 == "3":
        check_students()
    elif input1 == "4":
        lowest_grades()
    elif input1 == "5":
        highest_grades()
    elif input1 == "6":
        avg_grade()
    elif input1 == "x":
        print("Goodbye, see you soon =).")
    else:
        print("\nInvalid Command type (help) to see all the commands..")