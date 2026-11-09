"""
Codomax Digital Internship - Module 02
Functions, Files & Exception Handling

Project: Student Record Management System
Topics demonstrated:
- Functions, parameters and return values
- Lambda functions and list comprehensions
- File handling
- CSV and JSON handling
- Exception handling and basic debugging
- CRUD operations: Create, Read, Update, Delete

Run with:
    python Module_02_Functions_Files_Exception_Handling.py

No external packages are required.
"""

import csv
import json
from pathlib import Path

JSON_FILE = Path("students.json")
CSV_FILE = Path("students.csv")


# -------------------- FUNCTIONS --------------------

def get_non_empty_input(prompt):
    """Ask until the user enters a non-empty value."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def get_valid_age():
    """Get a positive integer age from the user."""
    while True:
        try:
            age = int(input("Enter age: "))
            if age > 0:
                return age
            print("Age must be greater than zero.")
        except ValueError:
            print("Invalid input. Enter age as a whole number.")


def load_students():
    """Read student records from JSON. Return an empty list if unavailable."""
    if not JSON_FILE.exists():
        return []

    try:
        with JSON_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            print("The JSON file format is not a student list.")
            return []
    except json.JSONDecodeError as error:
        print(f"Could not read JSON file: {error}")
        return []
    except OSError as error:
        print(f"File error while reading: {error}")
        return []


def save_students(students):
    """Write all student records to a JSON file."""
    try:
        with JSON_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
        return True
    except OSError as error:
        print(f"File error while saving: {error}")
        return False


def add_student():
    """Create a new student record."""
    students = load_students()
    student_id = get_non_empty_input("Enter student ID: ")

    # List comprehension: check whether this ID already exists.
    existing_ids = [student["student_id"] for student in students]
    if student_id in existing_ids:
        print("A student with this ID already exists.")
        return

    student = {
        "student_id": student_id,
        "name": get_non_empty_input("Enter student name: "),
        "age": get_valid_age(),
        "course": get_non_empty_input("Enter course: ")
    }

    students.append(student)
    if save_students(students):
        print("Student added successfully.")


def view_students():
    """Display all student records."""
    students = load_students()
    if not students:
        print("No student records found.")
        return

    print("\\n--- Student Records ---")
    for student in students:
        print(
            f"ID: {student['student_id']} | "
            f"Name: {student['name']} | "
            f"Age: {student['age']} | "
            f"Course: {student['course']}"
        )


def search_student():
    """Find a student by ID and demonstrate a lambda function."""
    students = load_students()
    student_id = input("Enter student ID to search: ").strip()

    # Lambda function: a small anonymous function used as a search condition.
    match = next(
        filter(lambda student: student["student_id"] == student_id, students),
        None
    )

    if match:
        print("Student found:", match)
    else:
        print("Student not found.")


def update_student():
    """Update an existing student record."""
    students = load_students()
    student_id = input("Enter student ID to update: ").strip()

    for student in students:
        if student["student_id"] == student_id:
            print("Press Enter to keep the existing value.")
            new_name = input(f"Name [{student['name']}]: ").strip()
            new_age = input(f"Age [{student['age']}]: ").strip()
            new_course = input(f"Course [{student['course']}]: ").strip()

            if new_name:
                student["name"] = new_name

            if new_age:
                try:
                    age = int(new_age)
                    if age <= 0:
                        raise ValueError("Age must be positive.")
                    student["age"] = age
                except ValueError:
                    print("Invalid age. Update cancelled.")
                    return

            if new_course:
                student["course"] = new_course

            if save_students(students):
                print("Student updated successfully.")
            return

    print("Student not found.")


def delete_student():
    """Delete a student record by ID."""
    students = load_students()
    student_id = input("Enter student ID to delete: ").strip()

    # List comprehension: keep every student except the selected ID.
    remaining_students = [
        student for student in students
        if student["student_id"] != student_id
    ]

    if len(remaining_students) == len(students):
        print("Student not found.")
    elif save_students(remaining_students):
        print("Student deleted successfully.")


# -------------------- CSV FILE HANDLING --------------------

def export_to_csv():
    """Export JSON student records into a CSV file."""
    students = load_students()
    fieldnames = ["student_id", "name", "age", "course"]

    try:
        with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
        print(f"Records exported to {CSV_FILE}.")
    except OSError as error:
        print(f"Could not export CSV file: {error}")


# -------------------- MAIN PROGRAM --------------------

def main():
    """Display the menu and run the selected operation."""
    while True:
        print("\\n===== STUDENT RECORD MANAGEMENT SYSTEM =====")
        print("1. Add student")
        print("2. View all students")
        print("3. Search student")
        print("4. Update student")
        print("5. Delete student")
        print("6. Export records to CSV")
        print("7. Exit")

        choice = input("Choose an option (1-7): ").strip()

        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                view_students()
            elif choice == "3":
                search_student()
            elif choice == "4":
                update_student()
            elif choice == "5":
                delete_student()
            elif choice == "6":
                export_to_csv()
            elif choice == "7":
                print("Thank you for using the program.")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")
        except (KeyboardInterrupt, EOFError):
            print("\\nProgram stopped safely.")
            break


if __name__ == "__main__":
    main()
