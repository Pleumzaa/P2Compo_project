import hashlib
from register import Register

login_data = []
user_data = {}
student_login_records = []

def prepare_login_data():
    for user in Register:
        if "email" in user and "password" in user:
            hashed_password = hashlib.sha256(user["password"].encode()).hexdigest()
            login_data.append({"email": user["email"], "password": hashed_password})
            user_data[user["email"]] = user

def login(email, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    for user in login_data:
        if user["email"] == email and user["password"] == hashed_password:
            return True
    return False

def remove_existing_student_record(email):
    global student_login_records
    student_login_records = [record for record in student_login_records if record['email'] != email]

def display_sorted_student_login_records():
    sorted_records = sorted(student_login_records, key=lambda record: record['user_details']['name'])
    for record in sorted_records:
        print(f"Email: {record['email']}, User Details: {record['user_details']}")

def is_student(user_info):
    return "id" in user_info

def login_process():
    MAX_ATTEMPTS = 3
    failed_attempts = 0

    while True:
        email_input = input("\nEnter email: ")
        if email_input.lower() == 'exit':
            break

        password_input = input("Enter password: ")

        if not email_input or not password_input:
            print("Email and password cannot be empty!")
            continue

        if login(email_input, password_input):
            print("Login successful!")
            user_info = user_data[email_input]

            if is_student(user_info):
                remove_existing_student_record(email_input)
                student_login_records.append({
                    "email": email_input,
                    "user_details": {
                        "id": user_info.get('id', 'N/A'),
                        "name": user_info['name'],
                        "section": user_info.get('section', 'N/A'),
                        "email": user_info['email']
                    }
                })
                print("----------Student record----------")
                display_sorted_student_login_records()

            print(f"\nUser Data:\nID: {user_info.get('id', 'N/A')}\nName: {user_info['name']}\nSection: {user_info.get('section', 'N/A')}\nEmail: {user_info['email']}")
            failed_attempts = 0
        else:
            failed_attempts += 1
            print("Login failed! Please check your email and password.")
            if failed_attempts >= MAX_ATTEMPTS:
                print("Too many failed attempts. Exiting...")
                break

prepare_login_data()
login_process()
