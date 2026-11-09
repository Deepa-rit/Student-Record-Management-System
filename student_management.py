import csv
from pathlib import Path

FILE_NAME = Path("students.csv")
FIELDS = ["student_id", "name", "age", "course"]


def load_students():
    if not FILE_NAME.exists():
        return []
    try:
        with FILE_NAME.open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except (OSError, csv.Error) as error:
        print(f"Error reading file: {error}")
        return []


def save_students(students):
    try:
        with FILE_NAME.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(students)
        return True
    except (OSError, csv.Error) as error:
        print(f"Error saving file: {error}")
        return False


def add_student():
    students = load_students()
    student_id = input("Student ID: ").strip()
    if not student_id or any(s["student_id"] == student_id for s in students):
        print("ID is empty or already exists.")
        return
    name = input("Name: ").strip()
    course = input("Course: ").strip()
    try:
        age = int(input("Age: "))
        if age <= 0:
            raise ValueError
    except ValueError:
        print("Enter a valid positive age.")
        return
    students.append({"student_id": student_id, "name": name,
                     "age": str(age), "course": course})
    if save_students(students):
        print("Student added.")


def view_students():
    students = load_students()
    if not students:
        print("No records found.")
        return
    for s in students:
        print(f"ID: {s['student_id']} | Name: {s['name']} | "
              f"Age: {s['age']} | Course: {s['course']}")


def search_student():
    student_id = input("Enter ID to search: ").strip()
    for s in load_students():
        if s["student_id"] == student_id:
            print(s)
            return
    print("Student not found.")


def update_student():
    students = load_students()
    student_id = input("Enter ID to update: ").strip()
    for s in students:
        if s["student_id"] == student_id:
            name = input(f"Name [{s['name']}]: ").strip()
            age = input(f"Age [{s['age']}]: ").strip()
            course = input(f"Course [{s['course']}]: ").strip()
            if name:
                s["name"] = name
            if age:
                try:
                    if int(age) <= 0:
                        raise ValueError
                    s["age"] = age
                except ValueError:
                    print("Invalid age; update cancelled.")
                    return
            if course:
                s["course"] = course
            if save_students(students):
                print("Student updated.")
            return
    print("Student not found.")


def delete_student():
    students = load_students()
    student_id = input("Enter ID to delete: ").strip()
    updated = [s for s in students if s["student_id"] != student_id]
    if len(updated) == len(students):
        print("Student not found.")
    elif save_students(updated):
        print("Student deleted.")


def main():
    while True:
        print("\\n--- Student Record Management System ---")
        print("1 Add  2 View  3 Search  4 Update  5 Delete  6 Exit")
        choice = input("Choose 1-6: ").strip()
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
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except KeyboardInterrupt:
            print("\\nOperation cancelled.")


if __name__ == "__main__":
    main()
