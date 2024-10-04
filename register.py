import hashlib

Register = [
    {"id": 66011162, "name": "Phuwadon Somboonsaengarun", "section": 1, "email": "66011162@kmitl.ac.th", "username": "Pooh", "password": "Pooh"},
    {"id": 66011174, "name": "Poonavee Boonjong", "section": 2, "email": "66011174@kmitl.ac.th", "username": "Ges", "password": "Ges"},
    {"id": 66011173, "name": "Poonavat Boonjong", "section": 2, "email": "66011173@kmitl.ac.th", "username": "Gus", "password": "Gus"},
    {"id": 66110104, "name": "Theerasat Bureesettakorn", "section": 3, "email": "66110104@kmitl.ac.th", "username": "Tonnam", "password": "Tonnam"},
    {"id": 66011544, "name": "Kris Suwanyothin", "section": 2, "email": "66011544@kmitl.ac.th", "username": "Pleum", "password": "Pleum"},
    {"name": "Jirat Susu", "email": "jirat.su@kmitl.ac.th", "username": "jirat", "password": "jirat"},
    {"name": "Oat Realman", "email": "oat.re@kmitl.ac.th", "username": "oat", "password": "oat"}
]

grouped_students = {}
grouped_teachers = []

for person in Register:
    if "id" in person:  
        section = person["section"]
        if section not in grouped_students:
            grouped_students[section] = []
        grouped_students[section].append(person)
    else:
        grouped_teachers.append(person)

def sort_students(students):
    n = len(students)
    i = 0
    while i < n - 1:
        j = 0
        while j < n - i - 1:
            if students[j]["name"] > students[j + 1]["name"]:
                students[j], students[j + 1] = students[j + 1], students[j]
            j += 1
        i += 1

print("\nStudents:")
for section, students in grouped_students.items():
    sort_students(students)
    print(f"Section {section}:")
    for student in students:
        print(f"ID: {student['id']}, Name: {student['name']}, Section: {student['section']}, Email: {student['email']}")

print("\nTeachers:")
for teacher in grouped_teachers:
    print(f"Name: {teacher['name']}, Email: {teacher['email']}")

login_data = []
for user in Register:
    if "email" in user and "password" in user:
        hashed_password = hashlib.sha256(user["password"].encode()).hexdigest()
        login_data.append({"email": user["email"], "password": hashed_password})

def login(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    for user in login_data:
        if user["email"] == email and user["password"] == hashed_password:
            return True
    return False
